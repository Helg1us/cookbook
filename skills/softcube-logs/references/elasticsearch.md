# Elasticsearch (Graylog) — direct query reference

## Contents
- Cluster facts
- Field availability by service (what lies where)
- Full field list
- Recipe: errors grouped by error_code
- Recipe: trace a request_id
- Recipe: error volume over time
- Recipe: top services by log volume
- Recipe: duration_ms percentiles
- Operational checks (retention, indices)

## Cluster facts

- Endpoint: `http://elasticsearch-graylog.svc.softcube.com:9200` — ES **7.10**,
  no auth, VPN required.
- Always query the `softcube__*` pattern WITH a `range` filter on `timestamp`;
  the filter lets ES skip non-matching indices, keeping searches <1 s.
- `timestamp` has the STRICT format `uuuu-MM-dd HH:mm:ss.SSS` (UTC). Absolute
  values in range queries must match it exactly — `2026-06-11 08:00:00.000`;
  ISO-T or missing millis ⇒ HTTP 400. Date math (`now-2h`) works.
- Always set `"track_total_hits": true` — otherwise totals cap at `10000+`.
- Use `bool.filter` (not `must`) for term/range clauses — no scoring needed.
- `message` / `full_message` are standard-analyzed text without a `.keyword`
  subfield: full-text search only, no terms aggregation. Aggregate on
  `error_code` / `error_message` (keywords) instead.
- `source` (pod name) is text with the **keyword analyzer** + fielddata:
  exact `term` filters AND terms aggregations on it work.
- `error_message` uses the sentinel **`NO_DATA`** on non-error lines
  (>1M docs/day) — exclude it in aggregations (see recipe below).

## Field availability by service (what lies where)

Structured fields are populated by FEW services (verified 2026-06-11, 24h
window — re-check with the exists recipe below):

| Field | Populated by |
|---|---|
| `request_id` | `ai-softcube-com`, `ai-softcube-com-campaigns` only |
| `duration_ms` | `ai-load-balancer` only |
| `error_code` | `ai-softcube-com(-campaigns)`, `consumer-distribution(-contacts)`, `products-triggers`; values are coarse: `ERROR`, `TIMEOUT`, `INVALID_CLIENT` |
| `error_message`, `response_code` | `ai-softcube-com(-campaigns)` (error_message mostly = `NO_DATA`) |
| `component` | `go-consumer-products`, `model-manager`, `gocrawl-manager` |
| `tenant` | widely populated (segment-*, files-models, go-consumer-products, …) |

Who populates a field right now:

```bash
curl -s ".../softcube__*/_search" -H 'Content-Type: application/json' -d '{
  "size": 0,
  "query": {"bool": {"filter": [
    {"exists": {"field": "FIELD"}},
    {"range": {"timestamp": {"gte": "now-24h"}}}
  ]}},
  "aggs": {"svc": {"terms": {"field": "service_name", "size": 30}}}
}'
```

## Full field list

Keyword (exact match, aggregatable): `service_name`, `facility`, `env`,
`error_code`, `error_message`, `request_id`, `tenant`, `tenant_division`,
`component`, `function`, `path`, `method`, `response_code`, `status`,
`task_name`, `taskName`, `trigger_name`, `process_name`, `thread_name`,
`project`, `db`, `entity`, `event`, `layer`, `scope`, `session`, `type`,
`query`, `query_params`, `client_ip`, `user_agent`, `file`, `device`,
`reason`, `result`, `raw`, `errors`, `alias`, `ab`, `block_id`, `check_mode`,
`guid`, `nn_models`, `processed`, `active_tasks`, `failing_dependencies`,
`final_error`, `streams`.

Numeric: `level`, `duration_ms`, `line`, `pid`, `date_new`,
`aliases_requested`, `aliases_returned`, `free_workers`, `running_workers`,
`timeout_alias_errors`, `non_timeout_alias_errors`.

Text (analyzed, full-text search only): `message`, `full_message`, `response`.

Special: `source` (pod name) — text with keyword analyzer: behaves like a
keyword (exact term match + aggregations work).

Date: `timestamp`, `gl2_processing_timestamp`, `gl2_receive_timestamp`.

Graylog internals (rarely useful): `gl2_message_id`, `gl2_source_input`,
`gl2_source_node`, `gl2_remote_ip`, `gl2_remote_port`,
`gl2_accounted_message_size`.

## Recipe: errors grouped by error_code

```bash
curl -s "http://elasticsearch-graylog.svc.softcube.com:9200/softcube__*/_search" \
  -H 'Content-Type: application/json' -d '{
  "size": 0,
  "query": {"bool": {
    "filter": [
      {"term": {"service_name": "SERVICE"}},
      {"range": {"level": {"lte": 3}}},
      {"range": {"timestamp": {"gte": "now-24h"}}}
    ],
    "must_not": [{"term": {"error_message": "NO_DATA"}}]
  }},
  "aggs": {
    "codes": {"terms": {"field": "error_code", "size": 20}},
    "messages": {"terms": {"field": "error_message", "size": 20}}
  }
}'
```

## Recipe: trace a request_id

```bash
curl -s ".../softcube__*/_search" -H 'Content-Type: application/json' -d '{
  "size": 200,
  "_source": ["timestamp","level","service_name","source","message","duration_ms"],
  "query": {"bool": {"filter": [
    {"term": {"request_id": "REQUEST_ID"}},
    {"range": {"timestamp": {"gte": "now-24h"}}}
  ]}},
  "sort": [{"timestamp": {"order": "asc"}}]
}'
```

## Recipe: error volume over time

```bash
curl -s ".../softcube__*/_search" -H 'Content-Type: application/json' -d '{
  "size": 0,
  "query": {"bool": {"filter": [
    {"term": {"service_name": "SERVICE"}},
    {"range": {"level": {"lte": 3}}},
    {"range": {"timestamp": {"gte": "now-3d"}}}
  ]}},
  "aggs": {"hist": {"date_histogram": {"field": "timestamp", "fixed_interval": "1h"}}}
}'
```

## Recipe: top services by log volume

```bash
curl -s ".../softcube__*/_search" -H 'Content-Type: application/json' -d '{
  "size": 0,
  "query": {"range": {"timestamp": {"gte": "now-24h"}}},
  "aggs": {"svc": {"terms": {"field": "service_name", "size": 50}}}
}'
```

## Recipe: duration_ms percentiles

Only for services that log `duration_ms` — currently `ai-load-balancer` alone
(check the availability matrix above):

```bash
curl -s ".../softcube__*/_search" -H 'Content-Type: application/json' -d '{
  "size": 0,
  "query": {"bool": {"filter": [
    {"term": {"service_name": "SERVICE"}},
    {"range": {"timestamp": {"gte": "now-6h"}}},
    {"exists": {"field": "duration_ms"}}
  ]}},
  "aggs": {"latency": {"percentiles": {"field": "duration_ms",
                                       "percents": [50, 90, 95, 99]}}}
}'
```

## Operational checks (retention, indices)

```bash
# Current write index + rotation cadence
curl -s ".../_cat/aliases/softcube*?v"
curl -s ".../_cat/indices/softcube__*?h=index,docs.count,pri.store.size&s=index" | tail -5

# Oldest available data (retention boundary, ~7 days)
curl -s ".../softcube__*/_search" -H 'Content-Type: application/json' \
  -d '{"size":0,"aggs":{"min":{"min":{"field":"timestamp"}}}}'
```
