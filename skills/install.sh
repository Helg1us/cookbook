#!/usr/bin/env bash
# Idempotently symlink cookbook skills into the agent CLIs' discovery paths.
#
# Canonical store: this repo's skills/ (Agent Skills format: <name>/SKILL.md).
#  - Codex reads ~/.agents/skills natively (Agent Skills convention).
#  - Claude Code reads ~/.claude/skills; per-skill directory symlinks are
#    officially supported. Do NOT symlink the whole skills dir (unsupported
#    in both CLIs) and do NOT symlink SKILL.md files (Codex skips file links).
#
# RepoPrompt-managed skills (frontmatter `repoprompt_managed: true`) are NOT
# handled here — RepoPrompt regenerates its own copies on app launch.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGETS=("$HOME/.agents/skills" "$HOME/.claude/skills")

for dir in "${TARGETS[@]}"; do
  mkdir -p "$dir"
  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"
    link="$dir/$name"
    if [ -L "$link" ]; then
      [ "$(readlink "$link")" = "${skill%/}" ] && { echo "ok      $link"; continue; }
      rm "$link"
    elif [ -e "$link" ]; then
      echo "SKIP    $link exists and is not a symlink — resolve manually" >&2
      continue
    fi
    ln -s "${skill%/}" "$link"
    echo "linked  $link -> ${skill%/}"
  done
done
