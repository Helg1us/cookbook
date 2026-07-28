#!/usr/bin/env bash
# Idempotently symlink cookbook skills into the agent CLIs' discovery paths.
#
# Canonical store: this repo's skills/ (Agent Skills format: <name>/SKILL.md).
#  - Codex reads ~/.agents/skills natively (Agent Skills convention).
#  - Claude Code reads ~/.claude/skills; per-skill directory symlinks are
#    officially supported. Do NOT symlink the whole skills dir (unsupported
#    in both CLIs) and do NOT symlink SKILL.md files (Codex skips file links).
#  - RepoPrompt CE uses build-separated Codex homes. Link into homes that
#    already exist, but do not create RepoPrompt CE state on machines without it.
#
# RepoPrompt-managed skills (frontmatter `repoprompt_managed: true`) are NOT
# handled here — RepoPrompt regenerates its own copies on app launch.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGETS=("$HOME/.agents/skills" "$HOME/.claude/skills")
REPOPROMPT_CODEX_HOMES=(
  "$HOME/Library/Application Support/RepoPrompt CE/Codex/Debug/home"
  "$HOME/Library/Application Support/RepoPrompt CE/Codex/Release/home"
)

linked_count=0
existing_count=0
conflict_count=0
unavailable_target_count=0

install_into() {
  local dir="$1"
  mkdir -p "$dir"
  echo "target  $dir"

  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"
    link="$dir/$name"
    if [ -L "$link" ]; then
      if [ "$(readlink "$link")" = "${skill%/}" ]; then
        echo "ok      $link"
        ((existing_count += 1))
        continue
      fi
      rm "$link"
    elif [ -e "$link" ]; then
      echo "conflict $link exists and is not a symlink — resolve manually" >&2
      ((conflict_count += 1))
      continue
    fi
    ln -s "${skill%/}" "$link"
    echo "linked  $link -> ${skill%/}"
    ((linked_count += 1))
  done
}

for dir in "${TARGETS[@]}"; do
  install_into "$dir"
done

for home in "${REPOPROMPT_CODEX_HOMES[@]}"; do
  if [ -d "$home" ]; then
    install_into "$home/skills"
  else
    echo "skip    RepoPrompt CE Codex home is unavailable: $home"
    ((unavailable_target_count += 1))
  fi
done

echo "summary linked=$linked_count existing=$existing_count conflicts=$conflict_count unavailable_targets=$unavailable_target_count"
