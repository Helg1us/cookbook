---
name: commit
description: Create safe, atomic git commits with Conventional Commit messages and gitmoji-style emoji. Use when the user explicitly asks to commit changes, split work into commits, write a commit message, or prepare local git changes for committing.
disable-model-invocation: true
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git add:*)
  - Bash(git apply:*)
  - Bash(git restore:*)
  - Bash(git commit:*)
  - Bash(git show:*)
disallowed-tools:
  - Bash(git commit -a:*)
  - Bash(git commit --amend:*)
  - Bash(git commit --no-verify:*)
  - Bash(git commit -n:*)
---

# Commit

Create focused git commits from the current repository state. Optimize for preserving user work, matching repository conventions, and leaving a clean, reviewable history.

## Ground Rules

- Commit only after the user explicitly asks for a commit or invokes this skill.
- Never run destructive git commands such as `git reset --hard`, `git checkout --`, or force-push unless the user explicitly requests that exact operation.
- Never use `git commit -a`, `git commit --amend`, `git commit --no-verify`, `git commit -n`, or any option that rewrites history or bypasses hooks unless the user explicitly requests that exact operation.
- Never add assistant signatures, co-author trailers, generated-by lines, or tool branding to commits.
- Preserve user staging. If any changes are already staged, commit exactly the staged content unless the user asks to change staging.
- Do not use `git add .`, `git add -A`, or broad globs. Stage explicit paths or hunks only.
- Do not stage secrets, `.env` files, local credentials, private keys, large dumps, or unrelated generated files.
- If the repository clearly enforces a commit format, follow the repository format over this skill's default format and mention that choice.

## Workflow

1. Inspect repository state:
   - `git status --short`
   - `git diff --cached --stat`
   - `git diff --cached`
   - If nothing is staged: `git diff --stat` and `git diff`
   - Optionally inspect recent style with `git log -5 --oneline`
2. Determine whether staged changes exist.
   - If staged changes exist, treat them as the commit boundary.
   - If no staged changes exist, group unstaged changes by logical purpose and stage one group at a time with explicit pathspecs.
   - For untracked files and directories, inspect the exact file list and contents before staging; `git diff` does not show untracked content.
3. Split commits when changes are unrelated, use different commit types, touch clearly separate subsystems, or combine implementation with independent docs/tests/tooling changes.
4. If only part of a file belongs in the current commit, avoid interactive `git add -p` unless the environment supports it reliably. Prefer a non-interactive patch flow: create a minimal patch for the intended hunks outside the repository, run `git apply --cached --check <patch>`, then `git apply --cached <patch>`. Remove the temporary patch afterwards and never stage it.
5. Before each commit, review `git diff --cached --stat` and `git diff --cached` to confirm the exact staged content. Use `git restore --staged <path>` to remove accidental staging without touching the worktree.
6. Ask before committing if staging is ambiguous, a file looks risky to include, conflicts are present, tests fail, or the requested commit would mix unrelated work that cannot be split safely.
7. Run fast, relevant verification when it is obvious and proportional, or reuse verification already run in the current task. At minimum, consider `git diff --cached --check` before committing. Do not invent expensive test runs. If verification is skipped, note that after committing.
8. Commit each group with `git commit -m "<subject>"`. Use `git commit -m "<subject>" -m "<body>"` when the change needs rationale, migration notes, or breaking-change detail.
9. After each commit, inspect `git show --stat --oneline --no-ext-diff HEAD`.
10. After committing, report commit SHA(s), subject(s), and any verification performed or skipped.

## Default Message Format

Use this format unless the repository has a stricter convention:

```text
<type>(<scope>): <emoji> <imperative summary>
```

Rules:

- Keep the subject at or under 72 characters when practical.
- Use imperative mood: "add", "fix", "update", not "added" or "fixed".
- Prefer a precise scope when it improves scanability.
- Omit the scope when it does not add useful information.
- Use `!` after the type or scope for breaking changes.
- Add a commit body for non-obvious why, compatibility notes, migrations, or breaking changes.
- If the repository already uses leading gitmoji subjects, match that local convention instead.

## Type And Emoji Map

- `feat`: ✨ user-visible feature
- `fix`: 🐛 bug fix
- `docs`: 📝 documentation
- `style`: 💄 formatting or presentation-only change
- `refactor`: ♻️ restructuring without behavior change
- `perf`: ⚡ performance improvement
- `test`: ✅ tests
- `chore`: 🔧 maintenance, dependencies, config, generated assets
- `build`: 🏗️ build system or packaging
- `ci`: 🚀 CI/CD workflow change
- `revert`: ⏪ revert

Use the closest standard Conventional Commits type. Express finer categories as scopes when useful, such as `fix(security): 🔒 validate token`, `chore(deps): 📌 pin runtime`, `refactor(db): 🗃️ rename migration`, or `fix(a11y): ♿ label menu button`.

For reverts, prefer `revert: ⏪ <original subject>` and include body context such as `This reverts commit <hash>.` when a specific commit is being reverted.

## Split Heuristics

Prefer multiple commits when:

- Different changes would be reviewed by different owners.
- A revert of one change should not revert the others.
- Code, tests, docs, and tooling are independent rather than one coherent unit.
- The diff contains both feature work and unrelated cleanup.
- A generated artifact can be committed separately from its source change.

Prefer one commit when:

- Tests or docs are directly coupled to the implementation.
- A migration and code change must ship together.
- Splitting would create an intermediate broken state.

## Final Response

Keep the response concise:

- List each commit as `<sha> <subject>`.
- Mention verification, including "not run" with the reason when applicable.
- Mention any remaining uncommitted changes.
