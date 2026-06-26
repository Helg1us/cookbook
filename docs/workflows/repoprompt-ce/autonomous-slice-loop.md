# Autonomous Slice Loop Workflow

This document summarizes the RepoPrompt CE workflow defined in `workflows/repoprompt-ce/autonomous-slice-loop.md`.

Update this document whenever the workflow changes phases, gates, Oracle usage, validation behavior, review loops, commit behavior, or next-slice behavior.

## End-to-End Flow

```mermaid
flowchart TD
  A["Start: raw request"] --> B["Phase 0: workspace verification"]
  B --> C["Phase 0.5: resume scan"]

  C --> D{"Prior autonomous state exists?"}
  D -->|No usable artifacts| E["Phase 1: identify next slice"]
  D -->|Plan exists, not approved| I["Phase 4: plan review loop"]
  D -->|Plan approved, no engineer spec| J["Phase 5: engineer Oracle spec"]
  D -->|Engineer spec exists, no orchestration row| K["Phase 6: orchestrate implementation"]
  D -->|Uncommitted implementation, no clean Oracle verdict| L["Phase 7: implementation review loop"]
  D -->|Clean Oracle verdict, no commit hash| M["Phase 8: commit"]
  D -->|Commit exists, no next-slice verdict| N["Phase 9: next-slice gate"]
  D -->|NEXT_SLICE with complete contract| G["Create next slice scoreboard"]
  D -->|NEXT_SLICE name only or incomplete| E

  E --> E1["Translate request into repo nouns"]
  E1 --> E2["Run explore scouts"]
  E2 --> E3["Choose smallest dependency-correct slice"]
  E3 --> E4["Create append-only scoreboard"]

  E4 --> F["Phase 2: exa-cli checkpoint"]
  F --> F1{"External facts required?"}
  F1 -->|Yes| F2["Run exa-cli docs and code-examples"]
  F1 -->|No| F3["Record repo-local checkpoint"]
  F2 --> H["Phase 3: Deep Plan"]
  F3 --> H

  H --> H1["Normalize plan artifact"]
  H1 --> H2["Design critique"]
  H2 --> H3["Oracle plan readiness"]
  H3 --> H4{"Ready for formal Review?"}
  H4 -->|No| H5["Fix highest-priority planning gap"]
  H5 --> H3
  H4 -->|Yes| I

  I --> I1["Standard Review of plan"]
  I1 --> I2["Oracle plan approval + design critique"]
  I2 --> I3{"Plan approved?"}
  I3 -->|No| I4["Patch highest-priority plan blocker"]
  I4 --> I1
  I3 -->|Yes| J

  J --> J1["Oracle produces implementation spec"]
  J1 --> J2["Save normalized engineer spec"]
  J2 --> J3["Oracle spec consistency gate"]
  J3 --> J4{"Spec consistent?"}
  J4 -->|No| J5["Regenerate or patch spec"]
  J5 --> J3
  J4 -->|Plan insufficient| I
  J4 -->|Yes| K

  K --> K1["Orchestrate approved slice"]
  K1 --> K2["Run validation commands"]
  K2 --> K3["Append implementation and validation evidence"]
  K3 --> L

  L --> L1["Survey git status and diff"]
  L1 --> L2["Run standard implementation Review"]
  L2 --> L3["Oracle implementation cleanliness gate"]
  L3 --> L4{"Clean enough?"}
  L4 -->|No, blocker| L5["Fix single highest-priority blocker"]
  L5 --> L6["Rerun validation and Review"]
  L6 --> L3
  L4 -->|Cannot tell| L7["Gather targeted evidence"]
  L7 --> L6
  L4 -->|Yes| M

  M --> M1["Stage only slice-intended files"]
  M1 --> M2["Commit with Conventional Commit style"]
  M2 --> M3["Append commit hash to scoreboard"]
  M3 --> N

  N --> N1["Oracle checks original goal completion"]
  N1 --> N2{"Oracle verdict"}
  N2 -->|COMPLETE| O["Final rollup"]
  N2 -->|NO_SAFE_UNBLOCKED_SLICE| P["Final rollup with blocker"]
  N2 -->|NEXT_SLICE with complete contract| G
  N2 -->|NEXT_SLICE incomplete| E

  G --> F
```

## Review And Stop Rules

```mermaid
flowchart TD
  A["Review or Oracle finding"] --> B{"Blocking?"}
  B -->|Yes| C["Fix single highest-priority blocker"]
  C --> D["Rerun relevant validation"]
  D --> E["Rerun Review"]
  E --> F["Ask Oracle again"]
  F --> B

  B -->|No blockers| G["Commit current slice"]
  G --> H["Ask Oracle for next slice or completion"]
  H --> I{"Stop verdict?"}
  I -->|COMPLETE| J["Final rollup"]
  I -->|NO_SAFE_UNBLOCKED_SLICE| K["Final rollup with blocker"]
  I -->|NEXT_SLICE| L["Continue immediately"]
```

The workflow has no hidden iteration caps for blocking issues. A committed slice is not a stop condition when Oracle says the original goal is not complete.

## Oracle Parallelism

Oracle calls are encouraged, but the workflow keeps them scheduled. At most two independent Oracle conversations or Oracle-export-producing calls should be active at once. Dependent gates stay serial: do not ask for an implementation spec before plan approval, do not ask for commit readiness before implementation review is clean, and do not choose the next slice before the current slice is committed.

```mermaid
flowchart TD
  A["Oracle work queue"] --> B{"Independent requests?"}
  B -->|Yes, max 2 active| C["Run safe parallel pair"]
  B -->|No, dependent gate| D["Run serially"]

  C --> E["Summarize each answer into scoreboard"]
  D --> E
  E --> F["Route verdict into next workflow action"]

  F --> G{"Gate dependency"}
  G -->|Plan approved| H["Engineer spec may start"]
  G -->|Implementation review clean| I["Commit readiness may start"]
  G -->|Commit complete| J["Next-slice gate may start"]
```

## Generated Artifact Policy

The baseline workflow treats `prompt-exports/` orchestration artifacts as workflow state, not implementation code. Scoreboards, normalized plans, and engineer specs may be used as context for resume, planning, validation evidence, and Oracle gates, but they should not pollute implementation review or commit scope unless the current slice explicitly edits workflow artifacts.

```mermaid
flowchart TD
  A["Changed file"] --> B{"Under prompt-exports/?"}
  B -->|No| C["Review and commit by normal slice rules"]
  B -->|Yes| D{"Slice explicitly edits workflow artifacts?"}
  D -->|Yes| E["Review as first-class deliverable"]
  D -->|No| F["Exclude from implementation Review and commit scope"]
  F --> G["Use as read-only workflow context"]
  E --> C
```
