---
name: goland-mcp
description: Use GoLand's integrated MCP server for IDE-aware code navigation, semantic search, inspections, project structure, builds, run configurations, formatting, and refactoring. Use when working with a project open in GoLand and the task benefits from GoLand indexes or IDE analysis.
---

# GoLand MCP

Use the tools exposed by the active GoLand MCP server. Treat the live tool
catalog as authoritative because available tools depend on the GoLand version,
installed plugins, and the user's Exposed Tools settings.

Pass the absolute project root as `projectPath` whenever supported.

Prefer GoLand MCP for:

- Finding files, text, regular-expression matches, and symbols.
- Reading symbol information and indexed dependency sources.
- Inspecting file errors and warnings with `get_file_problems`.
- Discovering project modules, dependencies, repositories, and run
  configurations.
- Renaming symbols with `rename_refactoring`.
- Reformatting files with the IDE formatter.
- Building the project with `build_project`.
- Running an existing configuration with `execute_run_configuration`.

Use `get_run_configurations` before executing a configuration. Use
`get_symbol_info` when the declaration, signature, type, documentation, or
source location of a symbol matters.

For implementation work:

1. Locate the relevant code with indexed search and navigation tools.
2. Inspect symbols and file problems before changing code.
3. Apply the requested edit or refactoring.
4. Re-run inspections and validate with the appropriate build or run
   configuration.

If the GoLand MCP server or a required tool is unavailable, report that
limitation and continue with other available project tools when appropriate.
