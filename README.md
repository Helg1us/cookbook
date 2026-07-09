# Cookbook

Private source of truth for agent skills, RepoPrompt CE workflows, workflow documentation, and future workflow evaluation results.

## Purpose

This repository keeps RepoPrompt CE workflow files under Git history instead of treating the copies in `~/Library/Application Support/RepoPrompt CE/Workflows` as the long-term source of truth.

The active RepoPrompt CE workflow files are stored in:

```text
workflows/repoprompt-ce/
```

The local RepoPrompt CE AppSupport workflow files should be symlinks to those repository files. Updating a workflow in this repository updates the workflow that RepoPrompt CE reads locally.

## Layout

```text
skills/                         Canonical user-owned agent skills (Agent Skills format).
workflows/repoprompt-ce/        Active RepoPrompt CE workflow definitions.
docs/workflows/repoprompt-ce/   Matching Mermaid workflow documentation.
archive/repoprompt-ce/          Historical backups and migration snapshots.
results/                        Future evaluation outcomes, scores, domains, and version comparisons.
```

## Skills

`skills/` is the canonical store for user-owned skills shared across agent CLIs
(Claude Code, Codex). Each skill is a directory with a `SKILL.md` (Agent Skills
format; cross-agent metadata may live in `agents/openai.yaml`).

Discovery is wired via per-skill directory symlinks — run `skills/install.sh`
(idempotent) on a new machine after cloning:

```text
~/.agents/skills/<name>  -> skills/<name>   # Codex reads ~/.agents/skills natively
~/.claude/skills/<name>  -> skills/<name>   # Claude Code supports dir symlinks
```

Rules learned the hard way:
- symlink the skill DIRECTORY, never the `SKILL.md` file (Codex skips file links)
  and never the whole `skills/` parent dir (unsupported in both CLIs);
- RepoPrompt STOCK skills (`repoprompt_managed: true` + `repoprompt_skills_version`
  frontmatter — rp-build/deep-plan/investigate/optimize/oracle-export/orchestrate/
  refactor/reminder/review) are NOT stored here — RepoPrompt regenerates them from
  its versioned bundle on app launch;
- do NOT put `repoprompt_managed: true` on skills stored here (it hands ownership
  to RepoPrompt); `rp-ponytail-review` and `rp-thermo-nuclear-code-quality-review`
  carried that flag by mistake — it was stripped when they moved in;
- if any tool ever replaces one of the symlinks with a real directory, `install.sh`
  prints `SKIP` — reconcile manually (git history here is the source of record).

## Workflow Documentation Rule

Every active workflow under `workflows/repoprompt-ce/` must have a matching diagram document under `docs/workflows/repoprompt-ce/`.

When a workflow change modifies phases, gates, Oracle usage, validation behavior, review loops, artifact policy, or commit/next-slice behavior, update the matching diagram document in the same change.

Localized documentation is allowed when it already exists or is intentionally created. Use a locale suffix such as `.uk.md`; for example:

```text
workflows/repoprompt-ce/autonomous-slice-loop-specialist-reviews.md
docs/workflows/repoprompt-ce/autonomous-slice-loop-specialist-reviews.uk.md
```

## Local Symlink Model

Expected active symlinks:

```text
~/Library/Application Support/RepoPrompt CE/Workflows/autonomous-slice-loop.md
  -> workflows/repoprompt-ce/autonomous-slice-loop.md

~/Library/Application Support/RepoPrompt CE/Workflows/autonomous-slice-loop-specialist-reviews.md
  -> workflows/repoprompt-ce/autonomous-slice-loop-specialist-reviews.md
```

Only active workflow files are symlinked into AppSupport. Documentation, archives, and results remain repository-only.

## Results

Use `results/` for future records of:

- workflow versions;
- evaluation outcomes;
- domains or task classes tested;
- scores and rationale;
- comparisons between workflow variants.
