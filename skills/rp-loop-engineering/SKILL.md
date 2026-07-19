---
name: rp-loop-engineering
description: "Універсальний rp-ce loop-engineering флоу для нетривіальних задач: investigate → oracle-дизайн → deep-plan → bounded pair review плану → orchestrate → bounded pair review коду → frozen evidence → pair nuclear+ponytail → optimize → rp-capstone-review. Змістовна робота делегується RepoPrompt-сабагентам; фінальний capstone виконується host-level за власним contract, коміт після кожної адекватної зміни; після трьох remediation-циклів — Investigate + Oracle."
---

# rp-ce Loop-Engineering — універсальний runbook

Задача: $ARGUMENTS

Ти — оркестратор повного інженерного циклу через RepoPrompt-CE (MCP `RepoPromptCE`).
Уся змістовна робота (дослідження, план, імплементація, ревʼю) виконується **в окремих
RepoPrompt-сабагентах**, не в головній сесії. Головна сесія: координує, стерить, **незалежно
верифікує**, комітить, веде трек-лист (TaskCreate/TaskUpdate — по таску на фазу).

## Фаза 0 — Прив'язка (перед будь-чим)
`bind_context op=bind working_dirs=[<repo>]`; якщо кілька кандидатів — додай `window_id`.
⚠ `agent_run op=start` вимагає tab-контекст: якщо старт падає з "requires explicit tab
context" — `bind_context op=list` → `op=bind context_id=<активний таб>`. Якщо пізніше
"cannot inherit the explicit-tab worktree" — перебиндись на window-only і повтори.

Initialize exactly one task-scoped ledger at
`.tmp/rp-loop-engineering/<task-slug>/gate-ledger.md`. Its disposition and contents are
governed only by the canonical ledger rule in the freeze section below.

## Пайплайн (7 фаз)

| # | Фаза | Чим запускати | Вихід | Цикл? |
|---|------|---------------|-------|-------|
| 1 | Дослідження | RP workflow **`Investigate`**; вузькі probes — `explore` | file:line edit-site inventory / root cause; Investigate звітує шлях report (default convention `docs/investigations/`), conductor записує його | — |
| 2 | Дизайн (якщо є відкриті дизайн-рішення) | **`oracle_send`** (chat), за bounded Oracle contract нижче | converged design або escalation/blocker | за bounded Oracle contract нижче |
| 3 | Детальний план | RP workflow **`Deep Plan`** → `docs/plans/`; потім bounded **design-critique** (agent_run `model_id=design`, max-1-page, ТІЛЬКИ прогалини/суперечності/порядок — НЕ переписування дизайну) → зафолдити | executable по-кроковий план | — |
| 4 | Ревʼю плану | RP workflow **`Review`** як `pair`: звірити план проти critique+inventory; явно вказати: review only plan file as a document artifact, do not ask for git comparison scope | 0 P0-P1 у плані | до 3 qualifying plan-remediation cycles; далі Investigate + Oracle |
| 5 | Імплементація | RP workflow **`Orchestrate`** (`agent_run workflow_name="Orchestrate"`) | код, коміт+DoD після КОЖНОГО кроку | — |
| 6 | Ревʼю коду | RP workflow **`Review`** як `pair` на діффі імплементації | 0 P0-P1 на immutable candidate identity | до 3 qualifying code-remediation cycles; далі Investigate + Oracle |
| 7 | Якість + капстон | після promotion: canonical **nuclear** + **ponytail** skills як `pair` (паралельно) → RP workflow **`Optimize`** (запускати завжди: виконати Phase-1 scouting; повний performance loop продовжувати лише за наявності вимірюваної метрики або hot path, інакше зафіксувати explicit N/A verdict) → verified host-level **`rp-capstone-review`** integrated entry point | фінальний gate на тій самій promoted frozen identity | будь-яка gate-driven мутація → DoD, новий candidate, повна фаза 6, promotion і всі gates фази 7 |

Після Investigation прийняти бінарне рішення про small-task compression і записати
eligibility та reason у ledger; невизначеність завжди обирає повний шлях. Фази 2-4 можна
обʼєднати в один стислий plan/critique/review pass лише коли немає open design decision,
external/public contract, concurrency, security, persistence, migration risk або
cross-module ownership change. Compression зменшує лише ceremony й нічого не auto-pass:
будь-який P0/P1 входить у повний звичайний remediation loop. **Фази 1 і 5-7 залишаються
обовʼязковими**. Не вводити Small/Standard/Critical lanes. Для trivial tasks використовувати
інший lightweight workflow, а не послаблювати цей conductor.

## Bounded Oracle contract
Oracle convergence у фазі 2 та в remediation escalation: після initial
answer провести щонайменше один і максимум три **substantive critique-response rounds**.
Раунд рахується лише коли critique містить новий argument/evidence, а Oracle відповідає по
суті; clarification або acknowledgement не рахуються substantive rounds, але кожен споживає
окремий guard максимум двох consecutive non-substantive exchanges; його exhaustion завершує
contract за тим самим terminal правилом нижче. Unresolved behavior/scope негайно
ескалювати, не вичерпуючи round budget. Якщо після третього substantive round лишається
material disagreement, звертатися до користувача лише коли його рішення здатне розвʼязати
питання; інакше завершити як explicit blocker. Намір користувача не може waive
`CONFIRMED` P0/P1.

## Контракт реального виклику
У фазі 0 один раз виконати `agent_manage op=list_workflows` і
`agent_manage op=list_agents`; зберегти exact workflow та role names verbatim без case
normalization і без висновків із подібних назв. Required workflow identities:
`Investigate`, `Deep Plan`, `Review`, `Orchestrate`, `Optimize`.

Для кожного workflow-backed leaf:
1. Launch each registered `Investigate`, `Deep Plan`, `Review`, `Orchestrate`, or `Optimize`
   workflow as `agent_run op=start workflow_name="<verbatim name>"` without `model_id`,
   intentionally accepting RepoPrompt's default `pair` role; reserve explicit `explore` and
   `design` for non-workflow probes and critiques, and leave `engineer` dispatch to `Orchestrate`.
2. Якщо workflow відсутній — знайти в active host або repository inventory повний,
   читабельний `SKILL.md` відповідної capability і перевірити його. Host-registered skill
   name, спільне походження або подібна назва не доводять workflow/skill equivalence.
3. For a verified-`SKILL.md` fallback, launch a fresh RepoPrompt agent as `pair` unless
   the complete leaf contract explicitly requires another role returned by `list_agents`; if
   that role is unavailable, record a blocker and stop. Наказати агенту прочитати весь
   перевірений файл і виконати його verbatim для explicit scope. Це alternate implementation,
   не доведений workflow alias; conductor перевіряє очікуваний output і stop gate фази.
4. Якщо повний skill contract або launch surface недоступні — записати explicit blocker
   і зупинитися. Не переносити змістовну роботу в host conductor і не
   заміняти відсутній contract довільним переказом.

Для кожного conductor-launched RepoPrompt leaf launch misfire означає zero tool uses або immediate exit. Після першого
misfire виконати **рівно один** fresh relaunch і передати повний verified leaf contract
verbatim разом з тим самим scope та всіма binding/Git/`context_builder` requirements.
Другий misfire блокує leaf і всю його фазу. Цей budget окремий від stall retries та діє
per leaf per gate run; нова promoted freeze identity починає новий gate run і новий
misfire budget.

Same-named host skill може бути лише джерелом contract після знаходження й перевірки його
повного файла; host-side invocation за ім'ям не є fallback для змістовної роботи.

Skill files шукати лише в реально доступних для active host місцях:
- addressable cookbook checkout;
- host symlink views: `$HOME/.agents/skills/<name>/SKILL.md`;
- `$HOME/.claude/skills/<name>/SKILL.md`.
Перед передачею RP-агенту або host-level invocation шлях має бути абсолютним, читабельним і вказувати на повний файл.
Прив'язка unrelated target repo не робить cookbook-relative `skills/<name>/SKILL.md`
доступним.

`rp-ponytail-review` і `rp-thermo-nuclear-code-quality-review` — individual skill leaves.
Composite workflow, що містить їх, не задовольняє жодну з цих leaf capabilities.

У фазі 0 знайти `rp-capstone-review/SKILL.md` в addressable cookbook checkout,
`$HOME/.agents/skills/rp-capstone-review/SKILL.md` або
`$HOME/.claude/skills/rp-capstone-review/SKILL.md` за тими самими verified-skill rules і
вибрати рівно один contract. Його absolute logical discovery path перетворити на absolute,
фізично resolved canonical target; довести, що target — читабельний regular file; рівно один
раз прочитати всі bytes в immutable buffer і записати їх SHA-256 та byte length. Якщо target
перебуває в accessible Git checkout і path tracked at HEAD, додатково записати canonical repo
root, repo-relative path, object format, tree mode/type, `HEAD:path` blob OID і доказ, що
фактичні bytes тотожні цьому blob. Не pin-ити source-repo HEAD: unrelated commit зі сталим
blob лишається valid. Сукупність цих полів є immutable `capstone_contract_record` і
authoritative in-session state; ledger — лише audit mirror. Відсутній, нечитабельний або
неповний capstone contract — explicit blocker. Host-registered name, походження чи схожа
capability не є заміною перевіреного файла.

## Правила циклів (loop-engineering)
- Вести два незалежні лічильники, початково `0`: `plan_remediation_count` для фази 4 та
  `code_remediation_count` для фаз 6-7. Plan-цикл не споживає code-бюджет і навпаки.
  Кожен лічильник належить поточній remediation epoch відповідного artifact.
- Before counters or stop rules apply, the parent conductor adjudicates every child/leaf
  finding into P0/P1/P2 by impact and evidence, never by leaf section or tag. Nuclear and
  Ponytail are not expected to emit P0/P1/P2. After this mapping, the existing
  CONFIRMED/PLAUSIBLE/REFUTED adjudication applies.
- For the single bounded finding-bearing child output currently under adjudication, no next
  patch or Oracle/reviewer scope is authorized until every material finding has a latest
  disposition in the append-only finding table below. This covers Review, critique, Oracle,
  nuclear/ponytail, Optimize-scouting, and capstone-retained findings; an Investigate inventory
  is an input, not an unbounded historical finding set. The exact next Oracle/reviewer input
  must enumerate every still-open latest `finding_id` and its disposition evidence; reuse an
  existing manifest hash when that input is already governed by one, without new hash or
  manifest machinery. Original child output and parent in-session adjudication stay
  authoritative; ledger rows are required audit proof, and disposition alone is non-counting.
- **Qualifying remediation cycle** — рівно одна завершена послідовність: adjudicated
  `CONFIRMED` або `PLAUSIBLE` P0/P1 → один coherent fix → applicable DoD → свіжий незалежний
  `Review` resulting exact identity. Лише завершення всієї послідовності споживає відповідний
  лічильник; P0/P1 з gate фази 7 споживає `code_remediation_count`.
- Не рахуються: baseline reviews; `REFUTED`; duplicate findings; збір, дедуплікація чи
  класифікація; P2; read-only verification; запит або очікування користувача; stalls,
  waits/steers, retries та misfires; supplemental adversarial verify; no-op proposal, patch
  або інша подія без зміни identity. Зміна лише candidate surface, що вимагає нового
  Phase-6 Review, але не містить adjudicated P0/P1 patch, не споживає
  `code_remediation_count`. Незавершена qualifying послідовність не дозволяє
  partial-attempt loop: до її незалежного `Review` не починати інший patch, а при
  interruption/blocker зупинитися як blocker, не авторизувати replacement patch і не
  обходити межу лічильника.
- **Conditional temporal-authority matrix.** Deep Plan — або compressed phases 2–4 pass —
  включає компактну матрицю `authority grant/use | intervening boundary | independent
  invalidation | required revalidation/compensation/terminal action | test/proof` лише коли
  одночасно виконуються всі чотири умови:
  1. verified fact/reference/token/proof authorizes publication, mutation, submit, cleanup,
     or attribution;
  2. authority is consumed after an `await`, RPC/process boundary, timeout race, cancellation
     point, or separate irreversible dispatch;
  3. the object or authority conditions can independently change; and
  4. stale consumption can harm correctness, ownership, finality, or non-replayability.
  Every row maps to at least one planned deterministic transition or fault-injection test. If
  deterministic testing is genuinely impossible, that row records why and cites a concrete
  evidence-backed non-testable proof. The conductor checks row coverage before Phase-4 launch,
  and Phase-4 Review checks it as plan completeness. The matrix lives inside the plan artifact
  or an existing design-authority document and is covered by that existing manifest member/hash,
  never a new artifact or member. If plausible temporal-authority work is evaluated but the
  matrix is not required, record one compact ledger reason naming the first failed condition;
  do not require per-function/per-`await` N/A records for ordinary async I/O, local immutable
  values, idempotent reads, or mandatory immediate revalidation.
- **Phase-4 Review identity** — at launch, the conductor creates one manifest of content
  hashes for every input it passes to Phase-4 Review: the plan, folded critique, inventory,
  and design-authority inputs. The verdict binds to that manifest; any member content change
  invalidates it and requires a fresh Review. Code identity before Phase 6 is the immutable
  candidate identity on the future freeze surface; after successful read-only Phase 6, that
  exact identity becomes the promoted Phase-7 frozen identity under the rules below. A normal
  patch changes its artifact identity but does not reset the counter.
- Initial remediation epoch may consume at most three qualifying cycles. Before each P0/P1
  patch check its counter: `0..2` authorizes one qualifying sequence, counted only after the
  fresh independent `Review`; at `3`, a fourth patch in that epoch is forbidden.
- After the initial epoch is exhausted, at most **one** new remediation epoch may open. It
  requires a full divergence summary (current identity, three attempts, findings, DoD/re-review
  outcomes, unresolved/regressed items, contradictions, assumptions), completed `Investigate`,
  and converged Oracle under the bounded contract. Immediately before its first patch, reset
  the relevant counter to `0` and record old identity, reset reason, and new plan/design
  authority; immediately after that patch record the new identity.
- If this second epoch exhausts its three-cycle budget, no further reset, epoch, or local patch
  is allowed. Use the user only when an intent/scope/classification decision can resolve it;
  otherwise stop as an explicit blocker. User intent can never waive a confirmed P0/P1.
- Фаза 4 завершується лише явним `"no P0-P1"`, привʼязаним до recorded Phase-4 Review
  input manifest above. Після plan patch створити новий manifest і повторити Review. Після
  третьої невдалої remediation застосувати одноразове second-epoch правило вище.
- Для code patch у фазі 6 або 7: застосувати межу epoch вище, виконати DoD і сформувати
  новий candidate за повними правилами surface нижче. Після явного `"no P0-P1"` і доказу,
  що candidate не змінився, promote exact same identity без recapture, потім повторити
  **всі** gates фази 7 у canonical order: nuclear, ponytail, `Optimize` з новим Phase-1
  scouting (і, якщо обґрунтовано, новим explicit N/A), `rp-capstone-review`.
- Discretionary P2 changes, які вирішено робити, обовʼязково згрупувати й завершити до
  candidate capture. P2 можна відкласти без patch; будь-який P2 patch після promotion
  інвалідовує frozen identity і вимагає повного шляху DoD → новий candidate → фаза 6 →
  promotion exact same identity → усі gates фази 7.
- Знахідки, що змінюють поведінку/скоуп, негайно передавати користувачу з рекомендацією,
  не patchити автономно. Без рішення це explicit blocker. Вибір користувача не може waive
  `CONFIRMED` P0/P1: його треба виправити й отримати `"no P0-P1"` на новій exact identity
  або завершити процес як blocker; так само не можна waive обовʼязковий gate.
- **Normative-conflict advancement gate.** When governing rules require incompatible outcomes
  for the same state, before patching dependent logic use the existing bounded Oracle/user
  authority to record the sources, precedence, affected semantics, and a
  scenario→expected-outcome test matrix. Dependent or uncertain exact slices remain blocked
  pending that resolution. A proven-disjoint exact slice may continue to severity, patch, and
  review only when no qualifying remediation sequence is open and a new finding transition
  records that exact slice plus evidence-backed disjointness rationale showing it chooses
  neither outcome. This transition creates no waiver, precedence, counter event, or exception
  to partial-attempt, DoD, commit, candidate-invalidation, re-review, or counter rules.
- **Global repository-candidate promotion gate.** Immediately before `PROMOTED`, require across
  the governed repository release-candidate scope both zero unresolved safety-semantic
  contradictions and zero accepted-unfixed or deferred-blocking P0/P1. A proven-disjoint
  transition never satisfies, bypasses, resolves, or waives either promotion blocker and never
  permits promotion of a dependent slice.

## Candidate identity, freeze surface і фінальні докази
The **canonical freeze actor/input universe** is authoritative resolved DoD commands,
Phase-6 `Review` including every nested `context_builder` invocation, and Phase-7 gates.
Before candidate capture, record one **closed allowed input/scope manifest** containing every
repo/worktree/submodule/external path and the permitted traversal/discovery bounds for all
actors in that universe. A covered path is within those bounds or otherwise directly consumed.
Include the complete immutable known-context record set consumed by Phase-7 gates and its
canonical digest before capture; derive the digest under the verified capstone contract without
silently widening or recapturing this frozen input later. Before candidate capture, include the
complete Phase-0 `capstone_contract_record` in this closed manifest; its canonical manifest
digest is therefore bound into candidate and promoted identity.
Before candidate capture, detect every base-to-head changed gitlink. For each, require the
immutable already-reviewed exact transition contract defined by the verified `rp-capstone-review`
skill and bind its record and digest into the closed manifest; otherwise block before Phase 6.
Reference that contract for the record schema rather than duplicating it here.

Before every Phase-6 `Review`, capture an immutable candidate identity over the closed surface
defined by this manifest. The canonical generic **EXCLUDED** predicate is:
`((the exact path is outside every permitted traversal/discovery bound in the closed manifest)
OR (every applicable command, Review/context_builder invocation, and gate explicitly ignores
it)) AND (the path is not directly consumed by any actor in the canonical universe)`.
Record enough path/type/content metadata to detect create/delete/modify:
- full base/head OIDs, clean staged/unstaged tracked states, and the closed manifest with
  permitted working directories/bounds/ignore rules and each submodule's OIDs/status;
- each non-ignored untracked path as **included** with a recursive path/type/content
  manifest/hash, **excluded** only under the canonical predicate, or **cleaned** before capture;
- inspect ignored paths when covered or potentially relevant as generated input, cache/config,
  or discovery target; use the same predicate for exclusion and otherwise include their state.

### Canonical ledger rule
The exact mutable ledger path is
`.tmp/rp-loop-engineering/<task-slug>/gate-ledger.md`. Keep it uncommitted by default and
non-authoritative; Git state and original agent outputs remain authoritative. After resolving
the canonical freeze universe, scopes, and generic EXCLUDED predicate above, this
ledger-specific exception has exactly two viable modes:
- **PROVEN EXCLUDED** — the exact ledger path satisfies the full canonical generic EXCLUDED
  predicate above. Ledger updates remain outside the candidate/frozen surface.
- **CLEAN GATE WORKTREE** — all actors in the canonical universe operate against the same
  recorded isolated clean materialized worktree/frozen identity; the ledger is absent there
  and no actor reads it from the external orchestration worktree. Ledger updates remain outside
  that gate worktree/surface.
If neither mode is proved, stop with an explicit blocker before candidate capture. The ledger
never receives an `included` or standalone `cleaned` disposition; the general
include/clean/clean-materialized-worktree fallback remains available only for other inputs.

Record artifact identities, tracked/index/submodule evidence, untracked dispositions, phase
states, remediation counters, adjudicated findings, blockers, required gate outcomes, and
deferred decisions with rationale/revisit triggers. Never store secrets, full transcripts,
prompt dumps, token accounting, or optional telemetry/session IDs unless a gate explicitly
consumes the field. The ledger supplements `TaskCreate`/`TaskUpdate`; it never replaces the
task tracker.

Only the finding table inside this otherwise mutable ledger is append-only. For every material
finding in the current bounded finding-bearing output, append:
`finding_id | source/anchor | raw severity if supplied → parent severity |
CONFIRMED/PLAUSIBLE/REFUTED | evidence/rationale | next scope/owner and exact next
Oracle/reviewer input | resolution identity/status`. Corrections append a superseding row;
never edit or delete finding-table history. A resumed run closes only the latest still-active
bounded output before advancing. The latest rows must prove the closure/input binding above;
the original output and parent in-session adjudication remain authoritative.

The actual invocation/read log is post-factum evidence only, not new candidate identity
membership. Every Phase-6 `Review` and nested `context_builder` invocation must stay within
the closed manifest. Out-of-manifest access aborts Phase 6, forbids promotion, and requires a
new candidate/manifest; this surface-only restart does not consume `code_remediation_count`.
When the generic EXCLUDED predicate fails, include the input, clean it, or run all actors in
the canonical universe against the same recorded isolated clean materialized worktree/frozen
identity, with no external-orchestration-worktree reads of excluded inputs.

A clean submodule is represented by its recorded OID/status. A dirty submodule is a blocker
unless a recursive materialized-content identity sufficient to detect create/delete/modify is
captured and included in both the candidate identity and authoritative final report.

Phase-6 reviewer отримує immutable candidate identity та перевіряє саме її. Review має бути
read-only та in-manifest. Після його явного `"no P0-P1"` повторно обчислити всі складові
identity лише для
доказу незмінності та порівняти з recorded candidate. Якщо вони тотожні, promote **цей самий**
candidate record як Phase-7 frozen identity без нового capture або зміни identity. Phase-7
reviewers отримують саме promoted frozen identity.

Будь-яка зміна candidate surface до promotion — tracked worktree, index, commit/HEAD,
submodule, included input, новий undisposed non-ignored path або релевантний ignored input —
скасовує результат поточного Phase-6 Review і запускає **повну** фазу 6 на новій candidate
identity. Такий surface-only restart без adjudicated P0/P1 patch не споживає
`code_remediation_count`.

Будь-яка post-promotion зміна frozen surface інвалідовує докази фаз 6-7. Після invalidation
виконати DoD для зміни shipping artifact, створити новий candidate, повторити повну фазу 6,
promote exact same identity після доказу незмінності та повторити nuclear, ponytail,
`Optimize` і `rp-capstone-review`. Adversarial verify може лише доповнювати ці докази,
але ніколи не замінює жоден required gate.

## DoD кожного кроку імплементації (не торгується)
До імплементації визначити exact commands і записати їх у ledger. Пріоритет джерел:
`AGENTS` → repository CI → documented Make/package scripts → ecosystem-standard defaults.
CI configs без explicit required markers означають усі default jobs, релевантні зміненим
components і shared/public surface.

Нередукований floor:
- build та/або typecheck, де застосовно;
- scoped static analysis;
- relevant deterministic tests;
- final gate, що покриває affected components і shared/public surface.

Відсутня або недоступна категорія потребує explicit evidence-backed N/A; мовчазне
вилучення заборонене. Go-приклад, не універсальний contract:
```
go build ./...                                  # build
go vet <ТІЛЬКИ змінені пакети>                  # scoped static analysis
go test <змінені області> ./... (relevant)       # relevant deterministic tests/final gate
go test -race .                                 # де застосовно
```
- ⚠ **vet/lint скоупити на змінені пакети.** Передіснуючий шум репозиторію (напр. protobuf
  copylocks) — НЕ gate; вкажи це явно в промпті orchestrate, інакше він зупиниться хибно.
- Коміт після кожної адекватної зміни, conventional-стиль (`fix(scope): …`, `feat(…): …`).
- Тест, що асертить значення, яке зовнішня система парсить (ES-таймаути, SQL, формати дат) —
  має пінити **wire-формат**, а не лише «мок отримав щось» (мок ігнорує значення → P0 проскочить).
- Behavior-preserving рефакторинг верифікується на **override/edge-кейсах**, не лише дефолтах.

## Нагляд за orchestrate (обов'язково)
- Моніторити через `agent_run op=wait` (він може ставити питання → `op=respond`). Два повні
  long-poll windows з незмінним cursor, без unanswered interaction і без in-flight progress
  дозволяють лише steer. Тиша сама не дозволяє cancellation, якщо її не можна відрізнити
  від здорового reasoning.
- Cancel/retry дозволено лише за позитивного доказу idle/no-progress після steer. Тоді
  дозволений рівно один fresh, вужчий retry; передати йому повний workflow або leaf contract
  verbatim разом з усіма binding, Git і `context_builder` requirements — не стислий переказ.
  Якщо після steer позитивного idle evidence немає, не cancel: записати blocker. Другий
  позитивно доведений stall retry-запуску — blocker. Пізнє валідне завершення оригінального
  запуску supersede-ить ще unresolved blocker після звичайної перевірки output та identity.
- **Out-of-scope зміни від orchestrate**: якщо зміна коректна — steer: «окремим комітом, і це
  єдиний виняток; далі строго скоуп»; якщо ні — revert. Ніколи не дозволяй бандлити її в
  крок-коміт.
- **Після завершення — незалежна верифікація**: сам прожени DoD, подивись `git log --stat`
  per-commit (санітарна перевірка скоупу), спот-чекни найризикованіші кроки. Build+тести
  можуть бути зелені при зламаному консюмері (класика: Unmarshal повернув pointer, а консюмер
  асертить value → метод тихо повертає nil).
- Sentinel/error-identity: аліаси (`var Err… = pkg.Err…`, `type X = pkg.X`), НЕ нові значення;
  текст повідомлення не міняти, якщо на нього є string-bridge (`strings.Contains`).

## Ролі агентів (agent_run model_id)
- `explore` — ТІЛЬКИ вузькі read-only розвідки (1 конкретне питання), не review і не
  імплементація; сесії прибирати одразу.
- `pair` — усі review-проходи: `rp-review`, **nuclear**, **ponytail**, адверсарна
  перевірка знахідок; може питати → відповідай.
- `engineer` — виконання чітко обмежених implementation-підзадач, коли їх делегує
  orchestrate.
- `design` — bounded critique плану (критик, не співавтор).
- `workflow_name="Orchestrate"` — імплементація по кроках та делегування `engineer`-агентам.
- **nuclear** (структура/maintainability) і **ponytail** (видалення/over-engineering) —
  individual skill leaves; запускати як `pair`-агентів з відповідною лінзою, ПАРАЛЕЛЬНО,
  на діффі через перевірений absolute `SKILL.md` path. Для їх misfire застосовувати загальний
  one-relaunch-per-leaf-per-gate-run contract вище; це launch failure, окремий від stall
  evidence та stall-retry budget.
- **rp-capstone-review** — host-level final gate. Immediately before its integrated entry
  point, re-resolve the original logical discovery path and require the same canonical target;
  open that target, require a regular file, read all bytes exactly once into a new immutable
  buffer, and recheck byte length, SHA-256 та, коли pinned, tracked path/tree mode/type/blob OID
  and byte equality to that blob. Виконати integrated contract з exact щойно перевірених bytes:
  без третього path read, skill-name registry lookup або path-only invocation. Будь-яка
  невідповідність — BLOCKED для поточного frozen run; replacement не можна re-pin/reverify
  in-run, новий contract вимагає нового Phase-0 run. Parent conductor робить цю перевірку й
  викликає повний verified contract після nuclear, ponytail та `Optimize`.
  Не запускати capstone як RepoPrompt child, не обгортати й не повторювати externally його
  internal leaves: capstone сам володіє їхнім lifecycle, а вся змістовна finding work лишається
  в його fresh `pair` children. Capstone blocker блокує release; retained P0/P1 проходять
  чинний code-remediation accounting, а будь-який patch інвалідовує Phase 6/7 і запускає
  всі gates на новій identity за canonical loop rules.
- Housekeeping: `agent_manage op=cleanup_sessions` після фіксації результату.

## Чому фазу 7 не можна пропускати (перевірено практикою)
Кожен шар ловить СВІЙ клас дефектів, які інші пропускають:
- **ponytail** ловить консистентність типу value↔pointer/assertion і мертвий код, який
  correctness-ревʼю і тести пропускають;
- **nuclear** ловить over-engineering (спекулятивні абстракції, мертві policy-механізми) —
  видаляй одразу, код має ЗМЕНШУВАТИСЬ після цієї фази;
- **rp-capstone-review** ловить те, що всі попередні проходи пропустили (wire-format
  баги, крос-системні контракти) через незалежні domain leaves і verification. Це фінальний
  release gate.
- **rp-optimize**: повний перф-цикл запускати лише коли є метрика/гарячий шлях; для
  структурних змін чесно виконати Phase-1 scouting (пошук внесених неефективностей) і, якщо
  чисто, зафіксувати N/A — не імітувати цикл.

## Політика моделей
- RepoPrompt-ролі використовують свої зареєстровані дефолти (`agent_manage op=list_agents`);
  concrete agent або model ID не пінити. Внутрішні ролі capstone визначає його verified contract.

## Промпт-гігієна для ревʼюерів
- Known-intentional, backward-compat винятки та deferred known-minor передавати як complete
  immutable known-context records; вони є evidence, а не waiver findings або governing rules.
- Reviewer фази 6 передавай full base/head OID та повний опис immutable candidate identity.
  Integrated capstone передавай exact canonical root, full base/head OIDs, complete promoted
  Phase-6 record і digest, complete promoted closed-input manifest і digest та complete immutable
  known-context records і digest. Capstone-required canonical structured-record digests виводь
  з уже frozen/promoted material за canonicalization verified capstone contract, без recapture,
  звуження surface або зміни identity; його schema тут не дублюй. Evidence чинний лише для
  переданої identity.
- Verify-фаза адверсарна: вердикти CONFIRMED/PLAUSIBLE/REFUTED, REFUTED відкидається.
  Supplemental adversarial verify не замінює required review чи gate.
- Диагностика LSP/IDE може бути спурйозною (стейл-індекс) — ground truth лише build/тести.

## Анти-патерни (виключено з практики як неефективні)
- 🚫 Писати план без фаз 1-2 (investigate/oracle) — план буде з дірками, які критик знайде пізніше й дорожче.
- 🚫 Виконувати роботу built-in агентами, коли домовлено про rp-ce — усе через RepoPrompt-сабагентів.
- 🚫 Запускати nuclear, ponytail або будь-який інший review через `explore`; review-роль — `pair`.
- 🚫 Підміняти реальний RP workflow або skill переказом його інструкцій у довільному prompt.
- 🚫 DoD-гейт на репо-wide vet/lint із передіснуючим шумом.
- 🚫 Довіряти звіту orchestrate без власної верифікації.
- 🚫 Приймати першу відповідь Oracle без критики.
- 🚫 Пропускати required review-lens без доказу, що та сама lens уже виконана на тому самому effective diff; будь-яка зміна review surface інвалідує цей доказ.
- 🚫 Порушувати two-epoch cap: відкривати третю remediation epoch, скидати exhausted second
  epoch або робити заборонений local patch; user intent не може waive confirmed P0/P1.
- 🚫 Після invalidated freeze продовжувати фазу 7 чи підміняти повний re-run малим diff або
  adversarial verify.
- 🚫 Cancel через саму тишу без positive idle/no-progress evidence; у вужчому retry скорочувати
  workflow/leaf contract або губити binding, Git чи `context_builder` requirements.
- 🚫 Спекулятивна загальність (політики/абстракції «на майбутнє», не підключені зараз) — MVP; додаси, коли підключиш.
- 🚫 Фіксити знахідки, що міняють поведінку/скоуп, без рішення користувача.
- 🚫 Лишати процес-артефакти (repro, investigation-доки) у shipping-гілці без явного рішення — зберігай на scratch-гілці (`git branch <name>-artifacts HEAD`).

## Фінальний звіт
Таблиця комітів по кроках; starting SHA; повні фінальні base/head OID; Phase-4 Review input manifest;
фінальні `plan_remediation_count` і `code_remediation_count`; candidate/promotion summary
для cleanliness, submodules та untracked dispositions; усі recursive dirty-submodule identities,
використані як proof; статус кожного gate фаз 6-7 саме на promoted frozen identity;
що знайшов кожен шар ревʼю; divergence/escalation та stall/retry/blocker outcomes, якщо були;
verification і фінальний clean/dirty status; known-latent/deferred список (щоб наступні ревʼю
не ре-флагали); відкриті питання користувачу; посилання на summary у canonical ledger.
