# Developer/Architect/DevOps

## Code Organization

- Whenever you create or edit a source or test file, organize the entire file before finishing. Apply this in every language and repository. Follow the project's import grouping and declaration conventions. Group related types, constructors, functions, methods, and tests by purpose, and place constants and helpers with the code they support.
- Preserve ordering that affects execution or public contracts, including side-effect imports, initialization, field layout, enum values, and registration order. Run the project's formatter and verify that reordering alone preserves behavior.

## Project Instructions

- Response Language: Ukrainian.
- Repository documentation language: English by default.
- Existing localized workflow documentation may be preserved with a locale suffix, for example `.uk.md`.

## Repository Rules

- Active RepoPrompt CE workflow files live under `workflows/repoprompt-ce/`.
- Local files in `~/Library/Application Support/RepoPrompt CE/Workflows` should be symlinks to the active workflow files in this repository.
- Do not treat AppSupport workflow files as the long-term source of truth after symlinks are installed.
- Do not symlink documentation, archives, or results into AppSupport.

## Workflow Documentation Rules

- Every workflow in `workflows/repoprompt-ce/` must have a matching Mermaid diagram document in `docs/workflows/repoprompt-ce/`.
- The documentation filename should match the workflow slug, optionally with a locale suffix such as `.uk.md`.
- Update the matching diagram document whenever a workflow change modifies phases, gates, Oracle usage, validation behavior, review loops, artifact policy, commit behavior, or next-slice behavior.
- Keep workflow diagrams detailed enough to show the complete lifecycle, major decision gates, review/fix loops, and stop conditions.

## Change Safety

- Before replacing AppSupport workflow files, create timestamped backups.
- Verify symlinks with `readlink` and content hashes after installation.
- Keep archived workflow backups under `archive/repoprompt-ce/workflow-backups/`.
- Do not commit secrets, local debug dumps, prompt exports, or unrelated generated artifacts.
