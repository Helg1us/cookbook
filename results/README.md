# Agent Change and Outcome Registry

`results/` is the durable longitudinal registry and index for governed agent-instruction and workflow changes. It is not raw evidence storage, a telemetry database, or a replacement for Git or task-local `.tmp` ledgers. Git remains the version authority; `.tmp` ledgers remain uncommitted and non-authoritative. Store immutable references to sanitized evidence, not secrets, credentials, PII, customer payloads, raw prompt exports, or third-party full content. Do not create a new storage, versioning, or instrumentation system here.

English governance is canonical in [the process document](../docs/agent-model-self-improvement.md); its [Ukrainian localization](../docs/agent-model-self-improvement.uk.md) MUST remain semantically identical.

## Compact Change Record

Editorial changes do not require a record. Each Compact observational or High-assurance change record MUST be append-only and contain, directly or by stable reference:

- **Identity/status:** `change_id`, `retry_of` when applicable, `revision_identity`, current lifecycle state, timestamps, and record revision.
- **Lane/scope:** lane, `mechanism_scope`, task classes, projects/environments, versions, exclusions, and risk rationale.
- **Motivation/hypothesis:** `motivation_status`, evidence-linked problem or opportunity, expected mechanism, intended outcome, and possible regressions.
- **Evidence:** immutable evidence IDs/references with `DEVELOPMENT`, `REGRESSION`, or `OUTCOME` roles; each item directly records or stably references its source/project/task, relevant version, time, collection context, provenance, and sanitization.
- **Challenge/adjudication:** independent challenge, Design Critic and Oracle dispositions when required, disagreements, confounders raised, and their human adjudication.
- **Human decision:** named author, evaluation owner when required, approver, activator/operator, decision, conditions, time, expiry, exact approved identities, and an immutable `approval_record_identity` covering the complete approved payload.
- **Activation/runtime identity:** content/revision, activation mechanism, model and host/orchestrator versions, and relevant toolset, configuration, permissions, and environment references; use `UNKNOWN` or `MISSING` explicitly.
- **Rollback/compensation:** deployable `rollback_target`, owner, verification, and `compensating_action` for irreversible residual effects. Mandatory rollback/deactivation triggers include guardrail breach, observability loss, and post-activation `revision_identity`, `activation_identity`, or approved-payload drift; record drift time, invalid evidence interval, and remediation.
- **Soak/guardrails:** eligibility, observation window, guardrails, stop conditions, review date, `extension_limit`, extensions, overlaps, and emergency actions.
- **Coverage/outcome:** coverage-tally reference, `evidence_strength`, `effect_direction`, claim scope, metrics actually claimed, uncertainty, missingness, and explicit confounder review.
- **Closure/supersession:** terminal decision, rationale, closure time, `closure_reason`, and successor/superseded IDs. Supersession uses `SUNSET` with `closure_reason=SUPERSEDED`.

Keep rejected, insufficient, inconclusive, harmful, rolled-back, and sunset records. Corrections append a new record revision linked to the superseded entry; they never overwrite history. Outcome evidence MUST postdate activation and use an identity distinct from motivating or development evidence; the same evidence ID cannot serve both roles. Detailed event records are required only for relevant failures, retries, interventions, sampled successes, costs, or other evidence events. Each event records its evidence identity, change/task reference, time, role, collection context, sanitization, and outcome; do not copy raw sensitive evidence into Git.

## Coverage Tally

Every eligible soak task MUST appear in a committed append-only coverage tally, individually or through a reproducible aggregate. The tally supplies the denominator needed to distinguish absence of evidence from success.

Core fields:

- `tally_id`
- `change_id`
- `record_revision` and `recorded_at`
- immutable aggregate source identity/reference
- `unit_of_analysis`
- `eligibility_definition`
- `observation_window`
- `deduplication_key`
- `eligible_count`
- `observed_count`
- `excluded_count` and reasons
- `missing_count`
- `counting_rule_version` and source reference

Conditional fields when applicable:

- `retry_counting_policy`
- `late_arrival_policy`
- `sampling_rule`
- `segmentation`
- `minimum_observed_count`
- `maximum_missing_rate`
- `decision_rule`

`observed_count`, `excluded_count`, and `missing_count` are mutually exclusive and MUST reconcile as `eligible_count = observed_count + excluded_count + missing_count`; exclusions retain reasons. `MISSING` and `UNKNOWN` never count as success. Rate or trend claims MUST identify unit, eligibility, window, deduplication, denominator, and missingness. Cost fields are required only for cost or efficiency claims. Generalization fields are required only for claims beyond directly observed scope. Measure what you claim.

A planned simultaneous soak for the same `mechanism_scope` is forbidden. Only unplanned or technically unavoidable overlap may be classified as forced. Forced unresolved overlap requires a human incident disposition, reason, time bounds, all relevant `change_id` values, and safe stop or rollback of one soak when possible; cap outcome `evidence_strength` at `OBSERVATIONAL`. Loss of observability requires rollback and an `INSUFFICIENT` / `UNKNOWN` outcome.

## Reconstructed Schema Examples

These examples illustrate record shape only. They are not observations and MUST NOT be copied as efficacy results.

```yaml
label: RECONSTRUCTED_SCHEMA_EXAMPLE
evidence_notice: NOT_EFFICACY_EVIDENCE
change:
  change_id: CHG-EXAMPLE-001
  revision_identity: git:<exact-object-id>
  state: SOAKING
  lane: Compact observational
  mechanism_scope: task-finalization instruction
  motivation_status: OBSERVED_RECURRING
  evidence_refs:
    DEVELOPMENT: [EVID-EXAMPLE-DEV]
    REGRESSION: [EVID-EXAMPLE-REG]
    OUTCOME: []
  challenge_ref: REVIEW-EXAMPLE-1
  human_decision:
    approver: human:<name>
    approved_identity: git:<exact-object-id>
    approval_record_identity: digest:<approved-payload>
  activation_identity:
    mechanism: config:<ref>
    model: UNKNOWN
    host_orchestrator: host:<version>
    toolset_config_permissions_environment: [config:<ref>]
  rollback_target:
    artifact_revision: git:<restorable-object-id>
    activation_mechanism: config:<prior-ref>
    runtime_identity: runtime:<prior-ref>
  soak:
    review_date: 2099-01-15
    extension_limit: 1
    guardrails: [guardrail:<ref>]
  coverage_tally_ref: COVERAGE-EXAMPLE-001
  outcome:
    evidence_strength: UNASSESSED
    effect_direction: UNKNOWN
    claim_scope: pending
```

```yaml
label: RECONSTRUCTED_SCHEMA_EXAMPLE
evidence_notice: NOT_EFFICACY_EVIDENCE
coverage_tally:
  tally_id: COVERAGE-EXAMPLE-001
  change_id: CHG-EXAMPLE-001
  record_revision: 1
  recorded_at: 2099-01-15T00:00:00Z
  aggregate_source_identity: digest:<source-snapshot>
  unit_of_analysis: eligible task
  eligibility_definition: rule:<versioned-ref>
  observation_window: 2099-01-01/2099-01-14
  deduplication_key: project+task_id
  eligible_count: 12
  observed_count: 10
  excluded_count: 1
  exclusion_reasons: {unsupported_environment: 1}
  missing_count: 1
  counting_rule_version: v1
  counting_rule_source: git:<exact-object-id>
  retry_counting_policy: first eligible attempt
  late_arrival_policy: append to next record revision
  decision_rule: rule:<predeclared-ref>
```

## Workflow Boundaries

Existing `rp-loop-engineering` and `rp-capstone-review` may be referenced for their own execution and release contracts. They are not efficacy graders, and their procedures are not duplicated in this registry. Existing backups are activation-safety inputs only when applicable.
