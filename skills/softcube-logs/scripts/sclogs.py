#!/usr/bin/env python3
"""Fetch Softcube production logs from the Graylog Elasticsearch cluster.

Stdlib only. The cluster is reachable over the office VPN without auth.
Examples:
    sclogs.py --list-services
    sclogs.py --service go-consumer-products --level error --since 2h
    sclogs.py --service files-models --grep "timeout" --since 1d --limit 100
    sclogs.py --service files-models --stats --since 1d
    sclogs.py --request-id abc-123 --since 6h --full
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

ES_URL = "http://elasticsearch-graylog.svc.softcube.com:9200"
INDEX = "softcube__*"

# Syslog numeric levels used by Graylog.
LEVEL_NAMES = {0: "EMERG", 1: "ALERT", 2: "CRIT", 3: "ERROR", 4: "WARN",
               5: "NOTICE", 6: "INFO", 7: "DEBUG"}
# --level flag -> upper bound on the numeric level (lower = more severe).
LEVEL_BOUNDS = {"error": 3, "warn": 4}

BASE_FIELDS = ["timestamp", "level", "service_name", "source", "message"]
FULL_FIELDS = ["full_message", "error_message", "error_code", "request_id"]

DURATION_RE = re.compile(r"^\d+[smhdw]$")
# The timestamp field uses the strict format `uuuu-MM-dd HH:mm:ss.SSS`;
# anything else (ISO-T, missing millis) is rejected by ES with a 400.
ABSOLUTE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})(?:[T ](\d{2}:\d{2})(:\d{2})?(\.\d{1,3})?)?$")


def parse_time(value, flag):
    """Normalize --since/--until input to ES date math or the index's
    exact timestamp format."""
    if value.startswith("now"):
        return value
    if DURATION_RE.match(value):
        return f"now-{value}"
    m = ABSOLUTE_RE.match(value)
    if m:
        date, hm, sec, ms = m.groups()
        millis = (ms or ".000").ljust(4, "0")
        return f"{date} {hm or '00:00'}{sec or ':00'}{millis}"
    sys.exit(f"{flag} expects a duration (30m, 2h, 3d) or an absolute UTC time "
             f"(2026-06-11, 2026-06-11 08:00, 2026-06-11T08:00:00.123), got: {value}")


def search(es_url, index, body, timeout=30):
    req = urllib.request.Request(
        f"{es_url}/{index}/_search",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        sys.exit(f"Elasticsearch returned HTTP {e.code}: {detail}")
    except (urllib.error.URLError, TimeoutError) as e:
        sys.exit(
            f"Cannot reach Elasticsearch at {es_url} ({e}).\n"
            "The cluster is only reachable over the office VPN — is the VPN up? "
            "If running in an agent sandbox, retry with network access enabled."
        )


def build_filters(args):
    filters = [{"range": {"timestamp": {"gte": args.since,
                                        **({"lte": args.until} if args.until else {})}}}]
    if args.service:
        filters.append({"term": {"service_name": args.service}})
    if args.facility:
        filters.append({"term": {"facility": args.facility}})
    if args.pod:
        # `source` is text with the keyword analyzer -> exact term match works
        filters.append({"term": {"source": args.pod}})
    if args.request_id:
        filters.append({"term": {"request_id": args.request_id}})
    if args.level in LEVEL_BOUNDS:
        filters.append({"range": {"level": {"lte": LEVEL_BOUNDS[args.level]}}})
    for f in args.field or []:
        key, _, value = f.partition("=")
        if not value:
            sys.exit(f"--field expects key=value, got: {f}")
        filters.append({"term": {key: value}})
    if args.grep:
        filters.append({"simple_query_string": {
            "query": args.grep,
            "fields": ["message", "full_message"],
            "default_operator": "and",
        }})
    return filters


def fmt_total(total):
    return f"{total['value']}{'+' if total.get('relation') == 'gte' else ''}"


def cmd_list_services(args):
    # honors the other filters too: `--list-services --grep timeout --level error`
    # answers "which services log timeout errors"
    body = {
        "size": 0,
        "query": {"bool": {"filter": build_filters(args)}},
        "aggs": {"svc": {"terms": {"field": "service_name", "size": 100}},
                 "fac": {"terms": {"field": "facility", "size": 100}}},
    }
    resp = search(args.es_url, args.index, body)
    aggs = resp["aggregations"]
    print(f"service_name values (window: {args.since.removeprefix('now-')}):")
    for b in aggs["svc"]["buckets"]:
        print(f"  {b['key']:<40} {b['doc_count']}")
    fac_only = [b for b in aggs["fac"]["buckets"]
                if b["key"] not in {s["key"] for s in aggs["svc"]["buckets"]}]
    if fac_only:
        print("facility-only emitters (use --facility):")
        for b in fac_only:
            print(f"  {b['key']:<40} {b['doc_count']}")


def cmd_stats(args):
    body = {
        "size": 0,
        "track_total_hits": True,
        "query": {"bool": {"filter": build_filters(args)}},
        "aggs": {
            "levels": {"terms": {"field": "level"}},
            "errors_per_hour": {
                "filter": {"range": {"level": {"lte": 3}}},
                "aggs": {"hist": {"date_histogram": {
                    "field": "timestamp", "calendar_interval": "hour"}}},
            },
        },
    }
    resp = search(args.es_url, args.index, body)
    aggs = resp["aggregations"]
    print(f"total: {fmt_total(resp['hits']['total'])}")
    print("by level:")
    for b in sorted(aggs["levels"]["buckets"], key=lambda b: b["key"]):
        name = LEVEL_NAMES.get(b["key"], str(b["key"]))
        print(f"  {name:<7} {b['doc_count']}")
    buckets = [b for b in aggs["errors_per_hour"]["hist"]["buckets"] if b["doc_count"]]
    if buckets:
        print("errors (level<=3) per hour:")
        for b in buckets:
            print(f"  {b['key_as_string'][:16]}  {b['doc_count']}")


def cmd_fetch(args):
    extra_fields = [f.strip() for f in (args.fields or "").split(",") if f.strip()]
    fields = BASE_FIELDS + (FULL_FIELDS if args.full else []) + extra_fields
    body = {
        "size": max(1, min(args.limit, 500)),
        "track_total_hits": True,
        "_source": fields,
        "query": {"bool": {"filter": build_filters(args)}},
        "sort": [{"timestamp": {"order": "desc"}}],
    }
    resp = search(args.es_url, args.index, body)
    hits = resp["hits"]["hits"]
    print(f"total: {fmt_total(resp['hits']['total'])} (showing {len(hits)}, newest first)")
    for h in hits:
        src = h["_source"]
        level = LEVEL_NAMES.get(src.get("level"), "?")
        # collapse multiline messages (stack traces, GraphQL queries) into one line
        message = " ".join(str(src.get("message", "")).split())
        line = (f"{src.get('timestamp', '?')}  {level:<5} "
                f"{src.get('source', src.get('service_name', '?'))}  {message}")
        print(line)
        extras = dict.fromkeys(f for f in (FULL_FIELDS if args.full else []) + extra_fields
                               if f not in BASE_FIELDS)
        for extra in extras:
            value = src.get(extra)
            # request_id is noise when it was the filter itself
            if value and not (extra == "request_id" and args.request_id):
                print(f"    {extra}: {value}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--service", help="exact service_name (see --list-services)")
    p.add_argument("--facility", help="filter by facility instead of service_name")
    p.add_argument("--pod", help="exact pod name (the `source` field)")
    p.add_argument("--since", default=None,
                   help="window start: 30m / 2h / 3d or absolute UTC time "
                        "(2026-06-11 08:00). Default 1h (24h for --list-services)")
    p.add_argument("--until", help="window end (same formats)")
    p.add_argument("--level", choices=["error", "warn", "all"], default="all",
                   help="error -> level<=3, warn -> level<=4 (default all)")
    p.add_argument("--grep", help="text search in message/full_message "
                                  "(simple query syntax: +word \"phrase\" -excluded)")
    p.add_argument("--request-id", help="filter by request_id")
    p.add_argument("--field", action="append", metavar="KEY=VALUE",
                   help="extra exact-match filter, repeatable")
    p.add_argument("--limit", type=int, default=50, help="max lines (default 50, cap 500)")
    p.add_argument("--full", action="store_true",
                   help="include full_message/error_message/error_code/request_id")
    p.add_argument("--fields", help="comma-separated extra _source fields to show")
    p.add_argument("--list-services", action="store_true",
                   help="list service_name values seen in the window (default window 24h)")
    p.add_argument("--stats", action="store_true",
                   help="per-level counts + hourly error histogram instead of log lines")
    p.add_argument("--es-url", default=ES_URL, help="override Elasticsearch URL")
    p.add_argument("--index", default=INDEX, help="override index pattern")
    args = p.parse_args()

    if args.since is None:
        args.since = "24h" if args.list_services else "1h"
    args.since = parse_time(args.since, "--since")
    if args.until:
        args.until = parse_time(args.until, "--until")

    if args.list_services:
        cmd_list_services(args)
    elif args.stats:
        cmd_stats(args)
    else:
        if not (args.service or args.facility or args.pod or args.request_id
                or args.field or args.grep):
            p.error("give at least --service / --facility / --pod / --request-id / "
                    "--grep / --field (or --list-services)")
        cmd_fetch(args)


if __name__ == "__main__":
    main()
