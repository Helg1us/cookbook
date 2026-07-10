---
name: rp-capstone-review
description: Runs a RepoPrompt-powered, read-only final capstone over an explicit committed base-to-current-clean-HEAD range. Use for a release gate on committed changes, not for general working-copy review.
---

# RP Capstone Review

Run this protocol in the host-level orchestrator, never inside a RepoPrompt child. Fail closed: any required source, tool, session, or audit fact that cannot be observed yields `BLOCKED / BLOCK`.

## Prerequisites and boundaries

Require RepoPrompt MCP, ordinary read-only local Git, and a registered `pair` role discovered with `agent_manage list_agents`; never use a fixed agent ID.

Accept exactly an explicit base revision and repository root. Do not review an arbitrary head or working-copy overlay. This is not a general, maintainability/structure, deletion/YAGNI, or measured-performance review; consider performance only when it directly causes correctness or security impact.

All participants are read-only. Do not write, fix, create worktrees, commit, publish externally, or invoke recursive agents.

## Establish the run

1. Canonicalize the supplied repository root.
2. Resolve `<base>^{commit}` and `HEAD^{commit}` to full OIDs and require base to be an ancestor of head.
3. Observe a clean index and tracked working tree plus no non-ignored untracked files. Inspect submodules and fail on any observed conflict, dirtiness, unavailable checkout/object, or HEAD/gitlink mismatch.
4. Define the immutable run identity as contract version, canonical root, and full endpoint OIDs; display it as `v1:<base-oid>..<head-oid>` with root reported separately.
5. Compare the endpoint trees. If they have no changes, report `NO REVIEWABLE CHANGES / BLOCK`.

Use ordinary read-only Git for these checks. Recheck the original HEAD OID and the same observed cleanliness/submodule conditions before reviewer fanout, after fanout completes, before verifier or adjudicator launch, and immediately before the terminal report. Any observed mutation yields `BLOCKED / BLOCK`; do not restart or salvage the run.

## Build bounded evidence

Use read-only Git and RepoPrompt reads to create one bounded `EvidenceIndex` for the exact base/head pair. Include changed areas and applicable contracts, instructions, specifications, tests, history, and dependency boundaries needed for review. Give entries stable IDs and exact current `file:line` references, or `base:<path>:line` for deleted content. Record known gaps explicitly.

Git OIDs identify endpoints; do not claim byte, frame, transport, log, or operating-system completeness. `context_builder` may discover pointers, but the host orchestrator must reopen and reground every retained claim in available source evidence. Freeze the index before fanout and give every child the same identity and evidence.

## Parallel reviewer barrier

Launch four fresh independent `pair` agents in parallel as read-only leaves with no cross-visibility:

1. **Contract/integration:** APIs, wiring, configuration, schemas, protocols, compatibility, defaults, and encoding.
2. **Temporal/failure:** ordering, concurrency, lifecycle, cancellation, retry, idempotency, partial failure, cleanup, and leaks.
3. **Specifications/tests:** tracked requirements, comments, tests, edge/failure assertions, and misleading mocks.
4. **Security/trust:** authentication, authorization, validation, injection, paths, deserialization, secrets, integrity, confidentiality, and abuse.

Children must not spawn agents, write, create worktrees, fix, commit, publish, or inspect another child's state. Each returns zero or more `LeafCandidate` records. A `LeafCandidate` intentionally has no verdict or severity and contains exactly:

- `id`;
- `category`;
- `invariant`;
- exact current `file:line`, or `base:<path>:line` only for deletions;
- `evidence_refs`;
- `impact`;
- `fix_direction`.

A `ReviewedFinding` is a `LeafCandidate` plus `verdict` and `severity`. When `verdict=PLAUSIBLE`, it also requires exactly one `missing_material_fact`; otherwise that field is absent.

Require terminal RepoPrompt session state and an available audit log for every attempt. Immediately BLOCK on unauthorized mutation, scope or identity mutation, a missing source or audit fact, an unresolved session, or a non-recoverable error. Allow exactly one fresh relaunch only for malformed child identity/output or an explicitly transient launch/tool failure; BLOCK if the retry is invalid or fails. Never loop indefinitely. Do not claim process-tree cancellation/reaping or unseen transport/log properties, and leave no observed active child before returning. The barrier requires four valid lens results.

## Verify and adjudicate

After the barrier and checkpoint, always launch one fresh `pair` verifier. It must reopen available evidence, audit coverage, deduplicate by `invariant + location`, and judge every leaf candidate into a `ReviewedFinding`. It may identify materially missed candidates, but emits those additions only as `LeafCandidate` records and must not judge its own additions.

If the verifier adds candidates, checkpoint and launch exactly one fresh `pair` adjudicator for the full verifier-added set. The adjudicator judges every addition into a `ReviewedFinding` and cannot create candidates.

Verdicts:

- `CONFIRMED`: positive evidence establishes the invariant violation and impact.
- `PLAUSIBLE`: positive evidence establishes a concrete invariant and causal chain, exactly one identified missing material fact prevents confirmation, and the conditional impact is P0 or P1.
- `REFUTED`: contradicted, duplicate, out of scope, or speculative.

A tool, log, citation, coverage, or source failure is `BLOCKED`, never `PLAUSIBLE`.

Severities:

- `P0`: catastrophic corruption, data loss, security compromise, or widespread outage.
- `P1`: material correctness, security, or compatibility defect that must be fixed before release.
- `P2`: bounded non-blocking defect, hardening issue, or test gap.

Retain only `CONFIRMED` and `PLAUSIBLE` findings. Sort deterministically by severity, verdict, path, line, and invariant. Cap displayed findings at 10 and report overflow; hidden P0/P1 findings still block.

## Decide and report

Outcomes are `NO REVIEWABLE CHANGES`, `CLEAN`, `FINDINGS`, or `BLOCKED`. Gate is `PASS` only for `CLEAN`, or `FINDINGS` with no retained P0/P1; otherwise it is `BLOCK`.

`CLEAN` means only that required phases completed, available evidence and logs were checked, and no findings or known material gaps remain. It does not prove undeclared transport or operating-system properties. For `CLEAN`, emit exactly:

`RP-CAPSTONE CLEAN run=v1:<full-base-oid>..<full-head-oid>`

Produce a deterministic terminal report containing:

- canonical root, full base/head OIDs, and run identity;
- scope and EvidenceIndex summary, including known gaps;
- child attempts and observed log-audit status;
- retained findings, displayed count, and overflow count;
- outcome and gate;
- the exact clean sentinel only for `CLEAN`;
- an exact blocker only when gate is `BLOCK`; `FINDINGS / PASS` reports normal reviewed findings without a fabricated blocker.
