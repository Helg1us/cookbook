---
name: softcube-logs
description: Fetches production logs of Softcube services from Graylog/Elasticsearch by service_name. Use when investigating errors, incidents, crashes or recent behavior of a deployed Softcube service — e.g. "show logs of X", "why does X fail", "what errors does X throw". Requires VPN connectivity.
---

# Softcube logs

Production logs live in a Graylog Elasticsearch cluster, keyed by the service
name (= k8s deployment name). The Elasticsearch endpoint is reachable directly
over the office VPN — no SSH, no auth. A connection error almost always means
the VPN is down.

## Quick start: logs

Run the bundled script (python3 stdlib only):

```bash
# Discover exact service names (when unsure how the project is named in logs)
python3 scripts/sclogs.py --list-services

# Recent errors of a service
python3 scripts/sclogs.py --service go-consumer-products --level error --since 2h

# Search message text (Lucene simple query syntax: +word, "phrase", -excluded)
python3 scripts/sclogs.py --service segment-worker-v2 --grep "timeout" --since 1d

# Error volume overview: counts per level + hourly error histogram
python3 scripts/sclogs.py --service files-models --stats --since 1d

# Trace one request across log lines
python3 scripts/sclogs.py --request-id abc-123 --since 6h --full
```

Useful flags: `--limit N` (default 50), `--full` (adds full_message /
error_message), `--pod NAME` (logs of one pod), `--field key=value` (extra
exact-match filter, repeatable), `--facility NAME` (alternative selector for
emitters that don't set service_name), `--until` (end of time window).
`--since/--until` accept durations (`30m`, `2h`, `3d`) or absolute UTC times
(`2026-06-11 08:00`).

## Log fields cheat-sheet

| Field | Type | Notes |
|---|---|---|
| `service_name` | keyword | primary selector, matches k8s deployment name |
| `level` | number | syslog: 2=crit, 3=error, 4=warning, 6=info |
| `message` | text | analyzed — search with `--grep`, not exact match |
| `full_message` | text | `message` is cut at the first newline (stack traces, queries) — when a line looks truncated, rerun with `--full` |
| `error_message`, `error_code` | keyword | mostly ai-softcube-com(-campaigns); error_message is often the sentinel `NO_DATA` — ignore that value |
| `source` | text (keyword analyzer) | pod name; exact match works (`--pod`) |
| `env` | keyword | only `prod` exists |
| `timestamp` | date | UTC, strict format `yyyy-MM-dd HH:mm:ss.SSS` |
| `request_id`, `tenant`, `component`, `duration_ms`, `response_code`, … | — | populated by FEW services each — availability matrix in [references/elasticsearch.md](references/elasticsearch.md) |

Retention is ~7 days. Indices rotate every few hours (`softcube__NNNN`);
the script always queries the `softcube__*` pattern with a timestamp filter,
which keeps searches under a second.

## Service discovery

If the user names a project rather than an exact service: run
`--list-services` and fuzzy-match. One repo may ship several services
(e.g. a `-campaigns` sibling). If a known emitter is missing from the list,
retry with `--facility <name>` — a few background jobs set `facility`
instead of `service_name`.

## Custom queries

When the script's flags are not enough (aggregations, grouping by error_code,
percentiles over duration_ms), query Elasticsearch directly with curl —
recipes and the full field list: [references/elasticsearch.md](references/elasticsearch.md).
