---
name: softcube-db
description: Read/inspect the Softcube production databases (Postgres "softcube"; kubeflow MySQL) through the read-only MCP server. Use whenever the user wants anything from the Softcube database — "query the softcube db", "show tables/schemas", tenant data, row counts, look up values, explore the schema. Never use psql, mysql, shell clients, or raw connection strings.
---

# Softcube database access (read-only, via MCP)

When the user wants to read anything from a Softcube database, use the **MCP
server tool**, not a shell or SQL client.

## Which tool
- **Postgres** (`softcube`, the main prod DB): MCP server `softcube-postgres-ro`
  (named `softcube_postgres_ro` in Codex) → tool `execute_sql`.
- **kubeflow MySQL** (only some users have it): MCP server `kubeflow-mysql-ro`
  (`kubeflow_mysql_ro` in Codex).

If the request says "the Softcube database" without more detail, use the
Postgres server. Do not ask which tool to use — just use the MCP.

## Hard rules
- **Never** use `psql`, `mysql`, the shell, a raw connection string, or any
  client other than the MCP server. The MCP is the only sanctioned path
  (auth is AWS IAM tokens; there are no passwords to use anyway).
- **Read-only.** SELECT only. Never attempt INSERT/UPDATE/DELETE/DDL — the
  database rejects them at the grant level.
- For schema/table discovery use **`pg_catalog`** (`pg_tables`, `pg_class`,
  `pg_namespace`, `pg_views`, `pg_matviews`) — **not broad `information_schema`
  scans**, which are slow under the read-only role and hit the statement
  timeout. A single narrowly-filtered `information_schema.columns` lookup for
  one table is fine.

## Where the data is
- Accessible schemas: `sc`, `public`, `reporting`, `segmentation`, `vb`.
  Most business data (tenants, campaigns, accounts) lives in `sc`.
- Not accessible (by design): `django`, `staging`, `public_admin`.
- Statement timeout for the LLM role: 60s. Connection limit: 10.

## Examples
- Find tenant tables:
  `SELECT schemaname, tablename FROM pg_tables WHERE tablename ILIKE '%tenant%' ORDER BY 1,2;`
- List schemas:
  `SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname <> 'information_schema';`
- Columns of one table:
  `SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='sc' AND table_name='tenant';`

## Setup (once per machine)
The MCP server itself is configured per the team guide in the `sc-autamation`
repo: `docs/rds-iam-access.uk.md` (wrapper `tools/rds-mcp-postgres.sh`, an
`AWS_PROFILE=<name>-llm` assume-role profile). This skill only teaches the
agent to route DB requests to that server.
