---
name: rp-capstone-review
description: Run a host-level, read-only final review of an exact committed release range with independent domain leaves, verification, and a deterministic release gate.
---

# RP Capstone Review v2

Execute this protocol only in the host orchestrator. Preflight RepoPrompt availability and a registered `pair` role; never pin a concrete agent or model ID. Treat RepoPrompt children as read-only leaves: they never spawn, retry, write, or control lifecycle. Fail closed as `BLOCKED / BLOCK` whenever required identity, evidence, authority, audit, or cleanup facts are unavailable.

This is a practical local adaptation of finder-to-verifier review behavior. Do not claim prompt, model, transport, operating-system, or publication parity.

## Select one entry point

- **Integrated review:** require an explicit canonical root, full base and head OIDs, immutable promoted Phase-6 record and digest, promoted closed-input manifest and digest, and immutable known-context records and digest.
- **Standalone review:** require an explicit canonical root and base; derive the current clean `HEAD`; accept optional immutable known-context records, using a canonical empty record set and digest when absent. Require no loop ledger.
- **Discovery-only:** report the skill name and v2 boundary, then stop. Perform no acquisition, child launch, review outcome, gate, sentinel, or loop-satisfaction claim.

Reject ambiguous modes or missing inputs. Reject a request for only selected paths, hunks, or change units as `BLOCKED / BLOCK`. Review the full exact release scope. Treat invocation focus and context as additive only: they may prioritize or add evidence but never remove a path, hunk, or change unit; override governing instructions; waive a finding; or waive a gate.

## Pin identity and preconditions

1. Physically canonicalize the root. Resolve `<base>^{commit}` and `<head>^{commit}` to full OIDs and require base ancestry. In integrated mode, before reading index, worktree, untracked, or checked-out-submodule state, require current `HEAD` to equal promoted `<head>` and all endpoints and supplied digests to match the promoted record. In standalone mode, derive head from current `HEAD`.
2. In standalone mode only, require a clean index and tracked worktree, no non-ignored untracked paths, and clean checked-out submodules matching gitlinks. In integrated mode, compare actual index, tracked-worktree, untracked, and checked-out-submodule state exactly with the promoted record and closed-input manifest; allow only included state whose identity is captured there. Record paths, types, identities, gitlink and checked-out OIDs, and observed status.
3. For any base-to-head gitlink change, immediately return `BLOCKED / BLOCK` unless an immutable, already-reviewed contract names the exact superproject path and gitlink transition, exact submodule base/head OIDs, its contract digest, `PASS`, and zero retained P0/P1. Bind the contract record and digest into the closed-input manifest, submodule-contract-set digest, run identity, and every checkpoint. Never treat pointer-only review as submodule-content coverage.
4. Verify the complete promoted record and digest in integrated mode, including endpoints, captured repository state, submodules, and manifest fields. Reserve identity components now; finalize identity only after closed-input and evidence digests are frozen.
5. Re-resolve and compare root, current HEAD, endpoints, ancestry, mode-specific Git state, submodules and their contract set, supplied records, manifests, and digests before fanout, after the leaf barrier, before verifier launch, before adjudicator launch when needed, and immediately before reporting. Any mutation or mismatch blocks without salvage.

Require an integrated promoted diff to be non-empty.

## Close the input surface

In integrated mode, consume the promoted closed-input manifest and digest without widening it silently. In standalone mode, build and freeze a closed manifest covering every review actor, permitted traversal/discovery root, potentially consumed repository, submodule, ignored, and external input, and each disposition.

For every potentially consumed ignored or external input, include path, type, and content identity sufficient to detect create/delete/modify, or prove it excluded and not consumed by every actor. Record negative searches and `NOT_APPLICABLE` dispositions. Block on an unresolved material input, out-of-manifest access, digest mismatch, or incomplete disposition.

For every structured record digest, encode RFC 8785 canonical JSON as UTF-8 and apply SHA-256; represent an empty record set as `[]`. Record the digest schema/version and reject non-canonical or differently encoded inputs.

## Acquire the exact range

1. Run `LC_ALL=C git rev-parse --show-object-format`. Set `oid_hex_length=40` for `sha1`, `64` for `sha256`, and block every unknown format.
2. Capture these byte streams from the pinned endpoints:
```text
LC_ALL=C git -c diff.algorithm=myers -c core.quotePath=false diff --no-color --default-prefix --src-prefix=a/ --dst-prefix=b/ -O/dev/null --no-renames --no-ext-diff --no-textconv --full-index --abbrev=<oid_hex_length> --raw -z <base> <head> --
LC_ALL=C git -c diff.algorithm=myers -c core.quotePath=false diff --no-color --default-prefix --src-prefix=a/ --dst-prefix=b/ -O/dev/null --no-renames --no-ext-diff --no-textconv --full-index --patch --binary --unified=0 <base> <head> --
```
3. Assign Git-emitted raw records, in order, `G0001...`. Assign each textual hunk header under its record `G0001/H0001...`. Preserve mode, type, full OIDs, status, and paths for text, binary, symlink, gitlink, and mode/type-only units. With rename detection disabled, treat moves as endpoint-specific additions and deletions.
4. Define a scope group deterministically as one `Gxxxx` raw record plus all of its `Hxxxx` units. Map every G/H unit exactly once to that group. Compute the diff digest as SHA-256 of the raw stream bytes immediately followed by the patch stream bytes, in that order, with no delimiter or transformation. Freeze it and the structural inventory of records, hunks, paths, types, and group mappings. Never let focus reduce this inventory.
5. Record the exact acquisition argv and environment profile above in the acquisition manifest and bind it into the evidence digest. The diff digest is defined only from the raw and patch byte streams produced by those two exact recorded invocations. Every replay must use a byte-for-byte identical profile; any profile mismatch is incomparable and must fail closed as `BLOCKED / BLOCK`. The verifier must detect and block any raw or patch byte change between the frozen acquisition and replay. Block if the installed Git does not support the complete profile. This profile neutralizes ambient `diff.noprefix`, `diff.srcPrefix`, `diff.dstPrefix`, `diff.mnemonicPrefix`, forced color, and `diff.orderFile`; determinism is claimed only for repeated acquisition with the same Git executable/version, repository/object database, pinned endpoints, filesystem-visible attributes and filters, locale, residual configuration, operating system, and recorded profile. No universal determinism is claimed across even stable residual configuration, attributes or filters, Git executables or versions, operating systems, platforms, repositories, or mutable external diff/textconv behavior.

Only after this complete canonical inventory, allow a standalone empty endpoint range to return `NO REVIEWABLE CHANGES / BLOCK`; require empty G/H inventory, launch no children, and emit no sentinel.

## Resolve authority

Discover governing instructions only from tracked `AGENTS.md` and `CLAUDE.md` chains read from commit trees. Apply the HEAD chain to added, modified, and current units; apply the BASE chain to deleted units. Treat A/D move halves at their respective endpoints.

Record `{endpoint_oid,path,blob_oid,scope,precedence}` for every applicable chain member at its governing endpoint. For every changed instruction file, additionally record both endpoint blob identities, using null for absence, and recompute applicability at both endpoints. Resolve conflicts by endpoint-specific scope, then deeper-file precedence within its subtree, and record every resolved override. Freeze the sorted endpoint/path/blob/scope/precedence records. The host and verifier must independently derive and compare them. Block on any missing or extra record, or conflict or ambiguity still unresolved after those rules.

Apply authority in this order:
1. host and skill safety/lifecycle;
2. applicable repository governing instructions, with deeper scope overriding only conflicting clauses in its subtree;
3. non-conflicting invocation context;
4. tracked contracts, specifications, and tests;
5. code comments;
6. history, prior reviewed intent, and known context.

Never let invocation or known context override governing rules or waive a P0/P1.

## Freeze the acquisition manifest

Cover every exact unit and scope group. Record search roots and methods; instruction chains and decisions; relevant comments; scoped history and blame; prior tracked or supplied reviewed intent; known context; stable evidence IDs; negative and `NOT_APPLICABLE` dispositions; attempted overrides or waivers; and all gaps. Freeze the evidence snapshot and digest. Treat known context as evidence, never authority to waive governing rules or P0/P1.

Finalize the exact mode identity only now:
- `v2:integrated:<base>..<head>:p=<promoted-digest>:c=<closed-input-digest>:s=<submodule-contract-set-digest>:e=<evidence-digest>:k=<known-digest>`
- `v2:standalone:<base>..<head>:c=<closed-input-digest>:s=<submodule-contract-set-digest>:e=<evidence-digest>:k=<known-digest>`

Give every child identical run identity, endpoints, object format, frozen diff digest and G/H inventory, group mapping, authority records, acquisition manifest, evidence, and known-context records/digests. Give each leaf the applicable traversal bounds and input dispositions required for its read-only scope. In integrated mode, additionally give the verifier the complete canonical promoted record and complete promoted closed-input manifest, not only their digests. Require every leaf, verifier, and adjudicator to echo the exact run identity, endpoints, and applicable promoted, closed-input, evidence, and known-context digests.

## Run four independent leaves

Launch four fresh `pair` leaves in parallel:

1. **Contract/integration:** APIs, wiring, configuration, schemas, protocols, compatibility, defaults, encoding, and a shallow obvious-bug scan.
2. **Temporal/failure:** ordering, concurrency, lifecycle, cancellation, retry, idempotency, partial failure, cleanup, and leaks.
3. **Specifications/tests:** tracked requirements, comments, tests, edge/failure assertions, and misleading mocks.
4. **Security/trust:** authentication, authorization, validation, injection, paths, deserialization, secrets, integrity, confidentiality, and abuse.

Require each leaf to echo the frozen identity and digests, state its authority override/waiver disposition, and disposition every scope group as `CHECKED` or evidence-backed `NOT_APPLICABLE`. For every group return per-domain attestations for `INSTRUCTIONS`, `COMMENTS`, `HISTORY`, `PRIOR_INTENT`, `KNOWN_CONTEXT`, and `CAUSALITY`, with evidence refs, candidate IDs, rationale, and instruction precedence/conflict details. Any `GAP` blocks. Contract/integration also attests `SHALLOW_BUG_SCAN` for every group.

Require every `LeafCandidate` to contain:
- `id`, `origin`, `category`, and `invariant`;
- `primary_location`: `HEAD file:line`, a BASE deletion location, or `git:Gxxxx` for a non-line unit;
- `related_locations`, `evidence_refs`, `instruction_refs`, `history_refs`, and `known_context_refs`, using explicit empty arrays;
- `causality: INTRODUCED | REGRESSED | MATERIALLY_EXPOSED` and `causal_rationale`;
- `base_disposition: ABSENT | DIFFERENT_BEHAVIOR | PRESENT_BUT_UNEXPOSED`;
- `impact` and `fix_direction`.

Require `INTRODUCED -> ABSENT`, `REGRESSED -> DIFFERENT_BEHAVIOR`, and `MATERIALLY_EXPOSED -> PRESENT_BUT_UNEXPOSED` with changed reachability, input, frequency, privilege, or blast radius.

## Verify and adjudicate

After the barrier and checkpoint, launch one fresh `pair` verifier. Require it to independently rerun the canonical diff with the recorded byte-for-byte identical acquisition argv and environment profile, compare both the recomputed raw-plus-patch byte digest and full G/H inventory/mapping with the frozen values, and rediscover governing instructions from the pinned commit trees. It must:

- block missing, extra, duplicate, unmapped, or multiply mapped units and every authority gap;
- in integrated mode, audit exact equality and no narrowing between the complete canonical promoted record and promoted closed-input manifest and the acquisition, evidence, and access dispositions, including traversal bounds, included ignored or external inputs, and per-actor dispositions;
- audit acquisition completeness and every leaf × scope-group disposition and attestation, not merely leaf-union coverage; treat every `GAP` as blocking;
- report `exact_diff_coverage: COMPLETE | MISMATCH` and `authority_precedence: SATISFIED | GAP`;
- only after `COMPLETE + SATISFIED`, judge every leaf candidate, deduplicate by invariant, location, and causality, and perform a gap sweep;
- emit any verifier additions only as unjudged `LeafCandidate` records.

Proceed only with `COMPLETE + SATISFIED`; otherwise return `BLOCKED / BLOCK`. If additions exist, checkpoint and launch one fresh `pair` adjudicator to judge exactly those additions. It cannot add candidates. With no additions, record `adjudicator=NOT_REQUIRED additions=0`.

A `ReviewedFinding` adds `reviewer: VERIFIER | ADJUDICATOR`, `verdict: CONFIRMED | PLAUSIBLE | REFUTED`, and `verification_evidence_refs`. Add `severity: P0 | P1 | P2` only to retained findings. Add exactly one `missing_material_fact` only for `PLAUSIBLE`; add `refutation_reason` for `REFUTED`. Never allow P2 to be plausible.

Use `CONFIRMED` only when positive evidence establishes the invariant violation, causality, and impact. Use `PLAUSIBLE` only when positive evidence establishes a concrete invariant and causal chain, conditional impact is P0/P1, and exactly one non-source/non-tool/non-audit/non-identity material fact prevents confirmation. Use `REFUTED` when evidence contradicts the candidate or the false-positive rules apply. Treat source, tool, identity, evidence, coverage, or audit gaps as blockers, never findings.

Refute speculative, nitpick/style, automated-gate-owned, out-of-range, duplicate, test-gap-only, compliant-intentional, or pre-existing defects not materially exposed by this range. Do not use generic quality to refute an instruction-mandated issue or a direct material correctness or security defect. Retain confirmed findings and plausible P0/P1 findings only.

Use severities:
- `P0`: catastrophic corruption, data loss, security compromise, or widespread outage.
- `P1`: material correctness, security, or compatibility defect requiring a pre-release fix.
- `P2`: bounded non-blocking defect or hardening issue.

Sort retained findings by severity, verdict, path, line, causality, invariant, and ID. Display at most 10 and report overflow; hidden P0/P1 findings still block.

## Own child lifecycle

The capstone host owns start, wait/poll, cancel, terminal-state confirmation, and audit for every internal child. Before each launch, record a finite attempt deadline and a finite post-cancel terminalization/cleanup deadline, plus attempt number. Cancel only on observed attempt-deadline exhaustion or positive no-progress evidence, then wait/poll to terminal and audit within the cleanup deadline.

Permit at most two attempts per child, with one fresh retry only for malformed or missing required identity/schema/output, or an explicit transient launch/tool failure. Never retry evidence/source gaps, mutation, unauthorized behavior, missing audit, or substantive review failure; never repair format in the same session. Cleanup-deadline exhaustion stops all further launches and returns `BLOCKED / BLOCK` naming every unresolved observed child; never claim cleanup completeness while one remains observed active. Do not claim unobserved process-tree or transport completeness.

## Remain read-only

Do not build, typecheck, run tests, fix code, create worktrees, commit, publish, comment externally, or create repository artifacts. Keep permitted audit state external. At barriers and terminal reporting, check observed repository writes and declared process-artifact locations; any unauthorized mutation blocks.

## Decide and report

Use only `NO REVIEWABLE CHANGES`, `CLEAN`, `FINDINGS`, or `BLOCKED`. After the standalone empty-range rule has returned `NO REVIEWABLE CHANGES / BLOCK`, decide in this order: any protocol or `GAP` blocker yields `BLOCKED / BLOCK`; otherwise any retained finding yields `FINDINGS`; otherwise yield `CLEAN`. Set gate `PASS` only for `CLEAN`, or `FINDINGS` without retained P0/P1. Every other outcome uses `BLOCK`.

Require complete exact diff coverage, satisfied authority, and non-waiver evidence for `CLEAN`, its sentinel, or any `PASS`. Emit this exact sentinel only for `CLEAN`:

`RP-CAPSTONE CLEAN run=<full-v2-run-identity>`

Report deterministically:
- canonical root, mode, full run identity, and full base/head OIDs;
- promoted, closed-input, submodule-contract-set, evidence, and known-context digests, marking non-applicable values;
- object format and OID length; G/H inventory and group-mapping summary;
- instruction, history, prior-intent, comment, known-context, override/waiver, and gap dispositions;
- child attempts, terminal states, cancellations, retries, and audits;
- exact-diff coverage and authority-precedence statuses;
- retained findings, displayed count, overflow, and refuted count;
- outcome, gate, blockers, and the sentinel only when allowed;
- observed repository-write and process-artifact checks.
