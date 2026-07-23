---
name: softcube-db
description: Read/inspect the Softcube production databases (Postgres "softcube"; kubeflow MySQL) through the read-only MCP server. Use whenever the user wants anything from the Softcube database — "query the softcube db", "show tables/schemas", tenant data, row counts, look up values, explore the schema, slow queries, db health. Never use psql, mysql, shell clients, or raw connection strings.
---

# Softcube database access (read-only, via MCP)

When the user wants to read anything from a Softcube database, use the **MCP
server tools**, not a shell or SQL client.

## Which server
- **Postgres** (`softcube`, the main prod DB): MCP server `softcube-postgres-ro`
  (named `softcube_postgres_ro` in Codex).
- **kubeflow MySQL** (only some users have it): MCP server `kubeflow-mysql-ro`
  (`kubeflow_mysql_ro` in Codex).

If the request says "the Softcube database" without more detail, use the
Postgres server. Do not ask which tool to use — just use the MCP.

## Postgres server tools — pick the right one

Schema discovery (prefer these over hand-written SQL):
- `list_schemas` — all schemas.
- `list_objects` — tables/views/sequences/extensions in a schema.
- `get_object_details` — columns, constraints, indexes of one object.

Data and analysis:
- `execute_sql` — run a read-only SELECT. Use for actual data questions.
- `explain_query` — execution plan and cost of a query.
- `get_top_queries` — slowest / most resource-intensive queries
  (pg_stat_statements).
- `analyze_db_health` — index/connection/vacuum/replication health checks.
- `analyze_workload_indexes`, `analyze_query_indexes` — index recommendations.

## Hard rules
- **Never** use `psql`, `mysql`, the shell, a raw connection string, or any
  client other than the MCP server. The MCP is the only sanctioned path
  (auth is AWS IAM tokens; there are no passwords to use anyway).
- **Read-only.** SELECT only. Never attempt INSERT/UPDATE/DELETE/DDL — the
  database rejects them at the grant level.
- In `execute_sql`, when you need catalog lookups, use **`pg_catalog`**
  (`pg_tables`, `pg_views`, `pg_matviews`, `pg_namespace`) — avoid broad
  `information_schema` scans (slow under the read-only role, they hit the
  statement timeout). A narrowly-filtered `information_schema.columns` lookup
  for one table is fine, but `get_object_details` already covers that.

## Where the data is
- Accessible schemas: `sc`, `public`, `reporting`, `segmentation`, `vb`.
  Most business data (tenants, campaigns, accounts) lives in `sc`.
- Not accessible (by design): `django`, `staging`, `public_admin` — catalog
  tools may list them, but reading their data is denied.
- Statement timeout for the LLM role: 60s. Connection limit: 10.

## Examples
- "What schemas are there?" → `list_schemas`.
- "What tables are in sc?" → `list_objects` (schema `sc`).
- "Columns of sc.tenant?" → `get_object_details` (schema `sc`, object `tenant`).
- "Find tenant tables" → `execute_sql`:
  `SELECT schemaname, tablename FROM pg_tables WHERE tablename ILIKE '%tenant%' ORDER BY 1,2;`
- "How many rows / which values …" → `execute_sql` with a plain SELECT.
- "Why is this query slow?" → `explain_query`; "what is slow overall?" →
  `get_top_queries`.

## Setup (once per machine)
The MCP server itself is configured per the team guide in the `sc-autamation`
repo: `docs/rds-iam-access.uk.md` (wrapper `tools/rds-mcp-postgres.sh`, an
`AWS_PROFILE=<name>-llm` assume-role profile). This skill only teaches the
agent to route DB requests to that server.
