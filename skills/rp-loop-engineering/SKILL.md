---
name: rp-loop-engineering
description: "Seven-phase RepoPrompt engineering conductor with a WIP=1 Goal Slice Graph, deterministic event fold, integrated freeze, and closed release terminals."
---

# RepoPrompt Loop Engineering Contract

Task: $ARGUMENTS

## Authority and lifecycle

### AUTH-1 — authority and ownership

The parent conductor solely owns routing, user I/O, severity adjudication, identities, state, budgets, escalation, and release decisions. It delegates investigation, planning, implementation, and review to verified RepoPrompt leaves, never implements leaf scope in the host session, and limits children to explicit scope and immutable raw output.

Git identities and immutable raw child outputs own behavioral/evidence facts; parent adjudication events own severity/disposition; the deterministic fold of a validated event chain owns orchestration state and counters. This skill alone owns lifecycle, states, budgets, triggers, invalidation, and terminals; the localized guide is descriptive and this skill wins conflicts. Capstone internals belong only to the pinned `rp-capstone-review/SKILL.md` contract.

### TERM-1 — closed outcomes

Progress states are `PLANNED`, `CLOSURE_PROVEN`, `READY`, `IMPLEMENTING`,
`LOCAL_DOD_PASS`, `COMMITTED_CANDIDATE`, `INDEPENDENT_REVIEW_PASS`, and `ACCEPTED`.
Reroutes or resumable pauses are `RESLICE_REQUIRED`, `REDESIGN_REQUIRED`,
`HOST_RECOVERY_REQUIRED`, and `USER_DECISION_REQUIRED`. `DISCOVERY_REQUIRED` is a
closure disposition, not a state. The only goal terminals are `RELEASED` and
`BLOCKED_WITH_PROOF`.

## Seven-phase conductor

Phase 0 is bootstrap; the seven execution phases are Phases 1–7.

| Phase | Required responsibility |
|---|---|
| 0 | Bind context; verify workflows/roles; pin capstone; create an isolated run and event genesis |
| 1 | Run `Investigate` for root cause, edit sites, consumers, and discovery evidence |
| 2 | Use bounded Oracle only for unresolved behavior, authority, ownership, or graph decisions |
| 3 | Run `Deep Plan` to produce one Goal Slice Graph, closure records, DoD, and release plan |
| 4 | Fold a bounded design critique, then run document-only `Review` on the exact input manifest within `PLAN-3` until `no P0-P1` |
| 5 | Execute every graph node serially through the WIP=1 slice state machine |
| 6 | Run integrated DoD, capture the closed candidate, read-only `Review` it, and promote the unchanged identity |
| 7 | On that identity run nuclear and ponytail, `Optimize`, then the verified host-level capstone |

A small goal is a one-node graph; no alternate lifecycle or compressed lane exists.

## Verified launch and Oracle

### LAUNCH-1 — discovery and leaves

In Phase 0 call RepoPrompt workflow/role inventories once and preserve exact case-sensitive names. Required workflows are `Investigate`, `Deep Plan`, `Review`, `Orchestrate`, and `Optimize`; launch each registered workflow verbatim without a model pin, accepting its default role. Reserve `explore` for narrow read-only probes and `design` for bounded critique; `Orchestrate` owns engineer dispatch. Never pin a concrete agent or model ID.

If a workflow is absent, locate and read a complete matching `SKILL.md` in an addressable cookbook checkout or verified host symlink view; similar names/origin do not prove equivalence. A fresh `pair` may execute it verbatim unless it requires another available registered role. If the complete contract/capability is unavailable, use `RECOVERY-1`; never paraphrase a substitute or move substantive work to host.

Check every conductor-launched output against its artifact/gate. Monitor `Orchestrate` by long-poll; silence is not cancellation evidence. Require positive idle/no-progress evidence, steer first, then allow one narrower fresh recovery attempt with the entire verified contract and original binding/Git requirements. Independently run DoD, inspect commit scope, and clean up finished sessions.

### LAUNCH-2 / CAPSTONE-1 — verified gate contracts

In Phase 0 resolve and pin the full readable contracts for exact identities `rp-ponytail-review` at `skills/rp-ponytail-review/SKILL.md` and `rp-thermo-nuclear-code-quality-review` at `skills/rp-thermo-nuclear-code-quality-review/SKILL.md`. Record each logical path, physical canonical target, byte length, and SHA-256. Immediately before every ponytail, thermo-nuclear, or nuclear gate, re-read the complete same contract, reverify those fields, and launch a fresh registered RepoPrompt `pair` via `agent_run` with its absolute verified path and an instruction to execute it verbatim on the exact candidate. A same-named workflow/skill, composite, registry lookup, excerpt, or paraphrase cannot substitute; only the full verified-`SKILL.md` fallback in `LAUNCH-1` is legal, and unavailable required role/capability follows `RECOVERY-1`.

In Phase 0 resolve exactly one readable regular `rp-capstone-review/SKILL.md` to its physical canonical target and read its bytes once. The `capstone_contract_record` stores logical path, canonical target, byte length, SHA-256, and, when tracked, repository root, relative path, object format, tree mode/type, `HEAD:path` blob OID, and byte equality. Pin the blob, not unrelated repository HEAD.

Immediately before capstone, re-resolve the original logical path, require the same target, read fresh bytes once, and reverify every field. Any difference produces `BLOCKED_WITH_PROOF`; no in-run re-pin/replacement is allowed. Invoke the integrated entry point from those bytes; do not launch capstone as a RepoPrompt child, wrap its leaves, or copy its protocol.

### ORACLE-1 — bounded convergence

After an initial Oracle answer, perform at least one and at most three substantive critique-response rounds; only new argument/evidence answered on substance counts. Clarification/acknowledgement does not count, with at most two consecutive non-substantive exchanges. Unresolved user-owned behavior/scope immediately pauses at `USER_DECISION_REQUIRED`; after the bound use it only if user choice can resolve the issue, else `BLOCKED_WITH_PROOF`. Oracle cannot waive confirmed P0/P1, triggers, gates, or lifecycle rules.

## Goal Slice Graph

### GRAPH-1 — node contract

Phase 3 produces one acyclic Goal Slice Graph. Each node has exactly `slice_id`, `behavior_id`, `owned_transition`, `done_when`, `depends_on[]`, `initial_closure_record`, `validation_contract`, `risk_tags[]`, and `status`. It owns one observable behavior or authority/ownership transition and one boolean `done_when`, which may aggregate assertions but returns one result. Split independent transitions/outcomes on their dependency edge; no file/LOC cap applies. `behavior_id` is stable lineage; `slice_id` identifies a decomposition.

### GRAPH-2 — ordering and WIP

The graph is an ordering/closure device, not a parallel scheduler. It must be acyclic, have
explicit dependency edges, and assign each transition to one lineage. `READY` requires every
dependency `ACCEPTED`, current Phase-4 authority, and current `CLOSURE_PROVEN`. Exactly one
node may be active from `IMPLEMENTING` through `INDEPENDENT_REVIEW_PASS`; entering `ACCEPTED`
releases the slot, while that node's open remediation sequence or pause retains it.

### GRAPH-3 — mutation and total invalidation

Changing `owned_transition`, `done_when`, `depends_on[]`, `validation_contract`, or behavior ownership invalidates the Phase-4 manifest, affected nodes/transitive dependents, their verdicts/acceptances, and all downstream integrated freeze/release evidence. The fold retains each executed behavior's first recorded `slice_base` and ordered committed-range lineage. It recomputes `accepted_head` as the head of the maximal execution-ordered prefix whose acceptance evidence remains current, or `run_base` when empty; no later OID bridges an invalidated gap. Commits remain forward history; affected nodes return to `PLANNED`, and Phases 3–4 plus WIP=1 recertification/re-review cover the earliest invalidated/original base through current `HEAD`, including affected later commits, before the frontier crosses them. Evidence-only recertification may preserve OIDs but never substitutes a later/current `accepted_head` for that retained base. Re-slicing changes `slice_id` but preserves `behavior_id` budget. A user-approved semantic replacement creates a predecessor-linked lineage and obsoletes findings by changed goal, never waiver.

Any semantic closure-field change recomputes `closure_hash` and invalidates every proof,
candidate, verdict, acceptance, dependent, and integrated record bound to the old hash. Before
`READY`, update and prove normally. After `READY`, classify under `CLOSURE-3`, return the
node to `PLANNED`, then use normal implementation or the evidence-only recertification edge in
`SLICE-1`. A second distinct miss cannot use recertification.

## Phase 0 and Phases 1–4

### RUN-1 — isolated run

Create or verify an isolated clean worktree on a dedicated branch such as
`rp-loop/<task-slug>` with no upstream and no unrelated user changes. Record `run_id`,
full `run_base`, branch/worktree identity, repository instructions, verified inventory, and
initial status. The conductor must not push, publish, merge, or dispatch release actions before
integrated promotion.

### RUN-2 — forward-only history

Once any OID is recorded, amend, reset, rebase, force-update, or other history rewrite is
forbidden. Remediation and abandoned approaches use forward superseding or revert commits.
`accepted_head` begins at `run_base`, advances after slice acceptance, and moves back only by the fold recomputation in `GRAPH-3`, never by history rewrite. Every commit is conventional
and independently checked for scope and applicable DoD.

### PLAN-1 — exact planning authority

Phase 1 inventories root cause, edit sites, direct consumers, dynamic-discovery risks, and instructions; Phase 2 resolves only open design questions. Phase 3 produces graph/plan, closure records, validation contracts, and release plan, then folds accepted findings from one bounded design critique.

Before Phase 4, materialize a canonical manifest whose members record `member_role`, immutable path, exact byte length, and SHA-256. Include Goal Slice Graph/plan, Investigation inventory, every design-authority input, and explicit `folded_critique` exact bytes after folding. The `no P0-P1` verdict binds to the complete manifest; any omitted member, missing critique, or path/byte/hash change invalidates launch/verdict and requires fresh Phase-4 Review.

### PLAN-2 — temporal authority and conflicts

When a verified fact/reference/token/proof authorizes publication, mutation, submit, cleanup,
or attribution after an await/RPC/process/timeout/cancellation/irreversible boundary, can
independently change, and stale use can harm correctness, ownership, finality, or
non-replayability, the plan includes:
`authority grant/use | intervening boundary | independent invalidation |
required revalidation/compensation/terminal action | test/proof`.
Every row maps to a deterministic transition/fault test or an evidence-backed non-testable
proof. The matrix is part of an existing manifest member. If evaluated but not applicable,
record the first failed condition without per-function ceremony.

Before any affected node becomes `READY`, resolve incompatible governing rules through the
bounded Oracle/user authority: sources, precedence, affected semantics, and
scenario-to-expected-outcome tests. Dependent or uncertain nodes remain `PLANNED`. There is no
disjoint bypass; the global release guard still applies.

### PLAN-3 — bounded Phase-4 remediation

One stable Phase-4 plan lineage, created by the initial graph manifest and preserved across manifest hashes, permits three completed qualifying cycles per epoch and at most two epochs. A cycle is a current-manifest `CONFIRMED`/`PLAUSIBLE` P0/P1, one coherent plan/graph correction, a new canonical manifest, and independent Phase-4 Review. Baselines, duplicates, P2, host failures, incomplete sequences, and invalidation without a P0/P1 correction do not count; an incomplete sequence blocks another correction. Before epoch 2, record divergence, complete `Investigate`, and converge bounded Oracle. Exhausted epoch 2 yields `USER_DECISION_REQUIRED` only for a legitimate goal choice, otherwise `BLOCKED_WITH_PROOF`. Existing finding, remediation, and verdict events record the cycles under `scope="phase4"`; this creates no slice state machine.

## Bounded closure

### CLOSURE-1 — record and hash

Closure is bounded evidence, never a claim of full transitive completeness. Each record has:
- `expected_write_set`: bounded paths/patterns, reason, and create/modify/delete type;
- `reverse_dependency_searches`: anchor, method, roots, one-hop consumers, and disposition
  for every changed exported/public/shared contract;
- `selecting_tests_fixtures_helpers`: direct selectors/interpreters or negative evidence;
- `triggered_ci_and_generated_artifacts`: affected jobs, generators, snapshots, schemas, and
  required command/update or evidence-backed `NOT_APPLICABLE`;
- `external_consumer_search`: bounded method/results only when acceptance is external;
- `dynamic_discovery`: reflection, registry, plugin, string/config, and runtime-path signals;
- `closure_hash`: SHA-256 over RFC 8785 canonical JSON of the preceding semantic fields.

Timestamps, prose, and mutable status are excluded from `closure_hash`.

### CLOSURE-2 — discovery gate

An unresolved dynamic signal yields `DISCOVERY_REQUIRED` and forbids
`PLANNED -> CLOSURE_PROVEN`. Targeted `Investigate` must include the consumer, prove it
irrelevant, or route to re-slice/redesign. `CLOSURE_PROVEN` requires every bounded search and
disposition to be current; missing direct tests/helpers/CI/generated/external consumers fail
the proof.

### CLOSURE-3 — expansion lineage

Planning refinements before `READY` and duplicate/known-path clarifications consume nothing.
The first distinct confirmed post-`READY` closure miss per `behavior_id` permits one automatic
record expansion, new hash, applicable DoD, and independent full-range Review; it is not a
semantic cycle. A second distinct miss requires `Investigate` plus bounded Oracle and routes
to `RESLICE_REQUIRED` or `REDESIGN_REQUIRED`.

## Phase 5 — WIP=1 slice execution

### SLICE-1 — total transition relation

Only these normal transitions are legal:

```text
PLANNED
  -> CLOSURE_PROVEN | RESLICE_REQUIRED | REDESIGN_REQUIRED
CLOSURE_PROVEN
  -> READY
READY
  -> IMPLEMENTING
  -> COMMITTED_CANDIDATE only for evidence-only recertification with unchanged OIDs,
     freshly revalidated DoD, current closure hash, and current clean-status profile
IMPLEMENTING
  -> LOCAL_DOD_PASS | USER_DECISION_REQUIRED | HOST_RECOVERY_REQUIRED
LOCAL_DOD_PASS
  -> COMMITTED_CANDIDATE | IMPLEMENTING
COMMITTED_CANDIDATE
  -> INDEPENDENT_REVIEW_PASS | IMPLEMENTING | PLANNED
  -> RESLICE_REQUIRED | REDESIGN_REQUIRED
INDEPENDENT_REVIEW_PASS
  -> ACCEPTED | COMMITTED_CANDIDATE | PLANNED
ACCEPTED
  -> PLANNED | RESLICE_REQUIRED | REDESIGN_REQUIRED on later invalidating evidence
CLOSURE_PROVEN | READY | IMPLEMENTING | LOCAL_DOD_PASS | COMMITTED_CANDIDATE |
INDEPENDENT_REVIEW_PASS | ACCEPTED
  -> PLANNED on GRAPH-3 or semantic closure invalidation
```

The listed invalidation edge is legal from every named source and requires the applicable graph/closure evidence. Any nonterminal state may enter `HOST_RECOVERY_REQUIRED` or `USER_DECISION_REQUIRED`.
The pause event stores `resume_state` plus exact graph, candidate, closure, and input hashes.
Resolution returns to `resume_state` only if all hashes remain current; otherwise the
applicable invalidation edge returns the node to `PLANNED`. Resolving
`RESLICE_REQUIRED`/`REDESIGN_REQUIRED` returns replacement/affected nodes to `PLANNED` only
after current Phase-3/4 authority exists. Every transition must be a validated
`STATE_TRANSITION`; no implicit edge advances state.

### DOD-1 — portable validation floor

Before implementation, derive exact commands from repository instructions, CI, documented
scripts, then ecosystem defaults. The portable floor is build/typecheck where applicable,
scoped static analysis, relevant deterministic tests, and a final gate covering affected and
shared/public surfaces. Any unavailable category needs evidence-backed `NOT_APPLICABLE`.
Validation must pin wire formats parsed externally, exercise override/edge paths for
behavior-preserving refactors, and preserve sentinel/error identity by alias where compatibility
requires it. Each coherent change receives a forward conventional commit after applicable DoD.

### SLICE-2 — cumulative committed candidate

On first execution, `slice_base` is current `accepted_head` or `run_base`; after invalidation it is the retained earliest base required by `GRAPH-3`. `slice_head` is full current `HEAD`
after all implementation/remediation commits. `candidate_identity` covers the complete `slice_base..slice_head`, `behavior_id`, `closure_hash`, review-input hash, and a versioned
clean-status record. Every Review and repeat Review covers that full range.

Profile v1 is RFC 8785 canonical JSON containing:
- `head_oid` equal to full `slice_head`;
- `index` and `tracked_worktree`, each empty plus SHA-256 of its normalized empty result;
- `non_ignored_untracked` sorted path/type/content-hash entries, empty except exact
  orchestration paths with current `PROVEN EXCLUDED` evidence or paths absent from the
  recorded `CLEAN GATE WORKTREE`;
- `submodules_gitlinks` sorted recursive path, tree gitlink OID, checked-out OID, and status;
  missing/uninitialized, `+`, `-`, `U`, dirt, or mismatch blocks, while no submodules requires
  evidence-backed `NOT_APPLICABLE`;
- `commands_profile_version` and the exact commands/options used.

Profile v1 captures exact raw output from `git rev-parse --verify HEAD`,
`git diff --cached --binary`, `git diff --binary`,
`git status --porcelain=v2 --untracked-files=all --ignore-submodules=none`,
`git ls-files --others --exclude-standard -z`, `git ls-tree -r -z HEAD`,
`git submodule status --recursive`, and recursive submodule
`git status --porcelain=v2 --untracked-files=all`. Normalize lowercase full OIDs/SHA-256,
UTF-8 paths sorted bytewise, exact status tokens, no timestamps/prose, and content hashes for
permitted orchestration entries. `clean_status_hash` is SHA-256 of the canonical record
excluding only that field.

### REVIEW-1 — independent full-range review

Immediately before launch, verify `head_oid`, empty index/tracked worktree, allowed untracked
set, submodule/gitlink state, and `clean_status_hash`; mismatch forbids Review and invalidates
any verdict. Standard `Review` always covers correctness, contract, tests, closure, and
deletion/YAGNI over `slice_base..slice_head`.

Run `rp-ponytail-review` under `CAPSTONE-1` when the slice introduces an abstraction/factory/adapter/strategy/policy/registry, dependency/wrapper over native capability, duplicate parallel helper/path, or speculative configurability. Run `rp-thermo-nuclear-code-quality-review` as thermo-nuclear under `CAPSTONE-1` for cross-module ownership, public/shared contract, state machine, concurrency/lifecycle/cancellation, persistence/migration/security/trust, or central orchestration ownership. A triggered lens is mandatory but advisory on severity; provider failure enters `HOST_RECOVERY_REQUIRED` and Oracle cannot waive it.
If none applies, materialize the canonical all-false trigger evaluation for that identity and record one `REVIEW_VERDICT` with `verdict="NOT_APPLICABLE"`. Standard deletion review remains. No speculative generality is permitted: policy, abstraction, configurability, or mechanism not required by current `done_when` is a release-blocking P1, cannot be deferred/downgraded, and blocks `ACCEPTED` and promotion until removed and independently re-reviewed.

### SLICE-3 — remediation and acceptance

The parent maps every material finding to P0/P1/P2 by impact/evidence, then
`CONFIRMED`/`PLAUSIBLE`/`REFUTED`. Before another patch or reviewer/Oracle scope, every
material finding in the current bounded output must have a latest lossless disposition and
every open `finding_id` must appear in the exact next input. Confirmed P0/P1 cannot be waived.
P2 chosen for change completes before the next candidate; otherwise record defer/revisit.

A confirmed/plausible P0/P1 authorizes one coherent fix under `BUDGET-1`, applicable DoD,
forward commit/new `slice_head`, and independent full-range Review. Identity/closure/output
hashes must remain current when `INDEPENDENT_REVIEW_PASS -> ACCEPTED` advances
`accepted_head`. Out-of-scope changes are split into a separate authorized node/commit or
reverted forward; they never hitchhike.

## Event fold, budgets, and recovery

### EVENT-1 — append-only chain

The parent is sole writer. Each immutable chain generation has one append-only path `.tmp/rp-loop-engineering/<task-slug>/generations/<generation_id>/gate-events.jsonl`.
Chain schema v1 fixes `chain_version=1` and `event_version=1`; each event contains those fields, `generation_id`, `run_id`, `sequence`, `previous_event_hash`, `event_type`, `scope`, applicable
`slice_id`/`behavior_id`, `candidate_identity`, `evidence_refs[]`, versioned `payload`, and `event_hash`. Every v1 core/payload member is present; inapplicable scalars are JSON `null`, empty collections are `[]`, and unknown or missing members reject the event.
Each line is one RFC 8785 canonical UTF-8 object plus LF, excluded from hashing. `event_hash` is lowercase SHA-256 over that object with only `event_hash` removed.

A generation has exactly one `RUN_GENESIS` at sequence `0`, with `previous_event_hash` equal to 64 lowercase zeroes; later sequences increment by one and name the preceding full hash.
Genesis payload v1 contains `predecessor`, `reconstruction`, and `imports`: respectively `null`, `null`, and `[]` for the first native generation; otherwise immutable predecessor path/ID,
sealed byte length/SHA-256, last valid sequence/hash, failure signature, reconstruction path/SHA-256, and source path/content SHA-256 for every import.

The closed event-type catalog is `RUN_GENESIS`, `CONTRACT_PIN`, `GRAPH_MANIFEST`,
`CLOSURE_SNAPSHOT`, `CANDIDATE_SNAPSHOT`, `CHILD_OUTPUT`, `FINDING_DISPOSITION`,
`STATE_TRANSITION`, `REVIEW_VERDICT`, `REMEDIATION_SEQUENCE`, `HOST_RECOVERY`,
`INTEGRATED_FREEZE`, `RELEASE_GATE`, and `RUN_TERMINAL`.

### EVENT-2 — deterministic fold

Reducer v1 validates generation linkage, schema/version, run, sequence/chain/hash, referenced bytes, identity currency, and owning-clause prerequisites, then processes events in order.
Pin/manifest/closure/candidate/output events establish immutable records only; semantic changes also require `GRAPH-3` invalidation and `STATE_TRANSITION`. `FINDING_DISPOSITION` alone updates the latest disposition for its `finding_id`.
`STATE_TRANSITION` alone changes slice/pause state and binds `from`, `to`, nullable `resume_state`, and current graph/closure/candidate/input identities. `REVIEW_VERDICT` changes only its named gate after current `CHILD_OUTPUT` and `EVENT-3` closure.
`REMEDIATION_SEQUENCE` alone increments its named Phase-4 or behavior lineage and binds findings, epoch/cycle, pre/post identities, applicable DoD/commit evidence, and subsequent Review. `HOST_RECOVERY` changes only host-epoch evidence; pause/resume still uses `STATE_TRANSITION`.
`INTEGRATED_FREEZE`/`RELEASE_GATE` establish identity-bound records; `RUN_TERMINAL` applies only when the fold already proves `TERM-1`/`RELEASE-1`. No other event has those effects.

Duplicate output content creates no second verdict or cycle. Out-of-order, missing, tampered,
or missing-byte events cannot advance and enter recovery. Late output advances only when exact
current candidate/closure/input hashes match; otherwise retain it as stale evidence.
Corrections are superseding events, never edits. State, readiness, findings, counters, epochs,
and terminals are fold outputs; mutable summaries have no authority.

### EVENT-3 — lossless verdict evidence

Every gate-advancing child verdict references `output_path`, `output_content_sha256`,
`input_manifest_or_candidate_hash`, and `verdict`. If output is inline, before parsing,
trimming, or advancement write the exact returned bytes to a write-once content-addressed path;
for a string, use exact UTF-8 without added newline and record encoding. Re-read and verify the
bytes, then reference them in `CHILD_OUTPUT`. Parent disposition records raw severity, mapped
P0/P1/P2, adjudication, evidence, next owner/input, and resolution identity. A verdict cannot
advance while any latest material finding lacks disposition or a confirmed/plausible P0/P1
remains accepted-unfixed/deferred-blocking.

### BUDGET-1 — semantic lineage

Each stable `behavior_id` lineage permits three completed qualifying cycles per epoch and at
most two epochs. A qualifying cycle is exactly: adjudicated `CONFIRMED`/`PLAUSIBLE` P0/P1,
one coherent fix, applicable DoD, forward commit/new `slice_head`, and independent full-range
Review. Baselines, duplicates, P2, incomplete sequences, closure misses, and host failures do
not consume it. An incomplete sequence holds WIP and blocks a replacement patch.

Before epoch 2, record a divergence summary, complete `Investigate`, and converge bounded
Oracle. Exhausted epoch 2 yields `USER_DECISION_REQUIRED` only for a legitimate goal choice;
otherwise `BLOCKED_WITH_PROOF`. No third epoch, reset, or local patch exists. Re-slice,
re-attribution, integrated invalidation, and capstone rerun never reset or refund a lineage.

### BUDGET-2 — recurrence tripwires

Before another patch, goal-level `Investigate` plus bounded Oracle is mandatory when another
distinct lineage already entered epoch 2 before the current lineage opens it, a lineage needs
a second re-slice, or the same normalized invariant/authority class recurs in another slice.
The fold derives goal aggregates without creating configurable caps.

### ATTRIBUTION-1 — integrated finding lineage

Before repairing an integrated/capstone P0/P1, record `affected_lineages` deterministically:
one existing transition gets `[behavior_id]`; one inseparable fix across several transitions
gets the sorted unique IDs; a release-boundary-only defect gets `["GLOBAL"]`. `GLOBAL` is one
stable run-level lineage and cannot mix with other IDs. Ambiguity requires `Investigate` plus
bounded Oracle before patching. Superseding attribution may correct evidence but never refunds
cycles. A completed multi-lineage sequence charges every listed lineage once and requires
budget in all; `GLOBAL` follows `BUDGET-1`. Repair reopens/creates attributed graph nodes,
uses forward commits and slice Review, then repeats the whole integrated path.

### RECOVERY-1 — typed host recovery

Zero-tool, routing, transport, provider, binding, launch, event-chain, and supervision failures
open a new `host_epoch` and never change candidate/closure identity or semantic/closure budget.
For one failure signature, run each distinct action once: verify binding/inventory; fresh clean
session with exact contract; permitted rebind/context recovery; verified contract-allowed
fallback. Temporary unavailability pauses at `HOST_RECOVERY_REQUIRED`. Only proven absence of
required capability with no resumable recovery yields `BLOCKED_WITH_PROOF`.

A generation with a missing, invalid, or unverifiable event is sealed at its last validated
event; never rewrite it or append behind the failure. Recovery may start only a fresh generation
path whose genesis links the sealed predecessor and independently verified reconstruction/import
bytes under `EVENT-1`. The fold verifies that linkage before accepting successor state; uncertain
cycles are conservatively consumed and non-unique reconstruction yields `BLOCKED_WITH_PROOF`.
A late completion may append to a healthy paused generation, or enter a successor only as a
hash-verified import.

## Phases 6–7 — integrated release only

### FREEZE-1 — cumulative closed candidate

Only after all nodes are `ACCEPTED`, build the integrated candidate over
`run_base..accepted_head`. Define the canonical freeze universe as resolved DoD commands,
Phase-6 `Review` including nested context building, and every Phase-7 gate. Create one closed
allowed input/scope manifest covering every repository, worktree, submodule, external path,
actor traversal/discovery bound, immutable known-context record/digest, and the complete
`capstone_contract_record`. Detect every changed gitlink and include the exact already-reviewed
transition record/digest required by the verified capstone contract; otherwise block.

Capture full base/head OIDs, clean index/tracked state, manifest/digest, submodule OIDs/status,
and enough path/type/content identity to detect create/delete/modify. Non-ignored untracked
paths are immutably included, proven excluded, or cleaned before capture. Inspect ignored paths
when covered, directly consumed, or potentially relevant as generated input, cache/config, or
discovery target; include or exclude them under `FREEZE-2`. Dirty submodules block unless a
recursive materialized-content identity is included in candidate and final report.

### FREEZE-2 — exclusion boundary

The canonical `EXCLUDED` predicate is:
`((path is outside every permitted traversal/discovery bound) OR
(every applicable command, Review/context invocation, and gate explicitly ignores it))
AND path is not directly consumed by any actor in the freeze universe`.
Ambiguity blocks. Integrated dirt blocks capture/promotion when covered or directly consumed
and neither immutably included nor proven `EXCLUDED`.

The orchestration event/output store may be outside the surface only as `PROVEN EXCLUDED`
under that predicate, or under `CLEAN GATE WORKTREE`: all freeze-universe actors use the same
recorded isolated clean materialized worktree, the store is absent there, and no actor reads
the external orchestration worktree. If neither is proved, block before capture. Unrelated
orchestration dirt satisfying either boundary is not a blanket blocker.

### FREEZE-3 — read-only review and total invalidation

Phase 6 is read-only and in-manifest. Out-of-manifest access aborts it and requires a new
manifest/candidate. After exact `no P0-P1`, recompute identity only to prove equality; promote
that same candidate without recapture. Any identity mismatch or mutation after capture
invalidates Phase 6. Any post-promotion mutation invalidates every Phase-6/7 proof. In either
case run applicable DoD, capture a new integrated candidate, repeat full Phase 6, promote only
unchanged identity, and repeat every Phase-7 gate. Supplemental verification replaces no gate.

### RELEASE-1 — global guard and order

Immediately before promotion require zero unresolved safety-semantic contradictions and zero
accepted-unfixed/deferred-blocking P0/P1 throughout governed scope. After unchanged promotion,
run nuclear through exact `rp-thermo-nuclear-code-quality-review` and ponytail through exact `rp-ponytail-review` in parallel under `CAPSTONE-1`, then `Optimize` always: perform its Phase-1 scouting and
continue its full loop only with a measurable metric/hot path, otherwise record evidence-backed
`NOT_APPLICABLE`. Then run capstone under `RELEASE-2`. Per-slice acceptance, integrated
capture, or promotion is never `RELEASED`. Only every gate passing on one unchanged promoted
identity emits terminal `RELEASED`.

### RELEASE-2 — capstone boundary

Pass the verified capstone the canonical root, full base/head OIDs, complete promoted Phase-6
record and digest, complete promoted closed-input manifest and digest, and immutable
known-context records/digest derived without recapture. Reference its verified schema and
lifecycle; do not duplicate them. A retained capstone P0/P1 blocks release, is attributed by
`ATTRIBUTION-1`, and any repair follows slice execution plus full integrated invalidation.

## Resume, migration, and report

### MIGRATION-1 — legacy compatibility

A run begun under an older pinned contract with `.tmp/rp-loop-engineering/<task-slug>/gate-ledger.md` either finishes under those exact bytes or starts a fresh generation whose `RUN_GENESIS` reconstruction/import linkage records the legacy source path and content SHA-256 for every independently verified Git/raw-output item. The legacy ledger remains read-only historical evidence outside the candidate surface; never convert it, rewrite a chain, or synthesize missing events from mutable headings, counters, or summaries. Unresolved legacy findings remain open until a parent adjudication event binds them to verified evidence and current candidate/input identity. Ambiguous prior attempts are conservatively consumed; inability to reconstruct uniquely with source hashes and dispositions yields `BLOCKED_WITH_PROOF`.

### REPORT-1 — fold-derived handoff

The final report is derived from the validated fold and includes `run_id`; `run_base` and
full final OIDs; graph/closure/Phase-4 manifest hashes; commits and DoD; each slice range,
review, risk-lens verdict, status, and lineage budget; goal tripwires and `host_epoch` history;
integrated manifest/candidate/promotion identities; all Phase-6/7 outcomes; findings and
attribution; deferred/revisit items; blockers/pauses; and final clean/dirty status. It links
immutable evidence rather than reproducing transcripts and reports exactly one terminal.
