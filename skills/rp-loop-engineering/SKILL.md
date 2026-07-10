---
name: rp-loop-engineering
description: "Універсальний rp-ce loop-engineering флоу для нетривіальних задач: investigate → oracle-дизайн → deep-plan → bounded pair review плану → orchestrate → bounded pair review коду → frozen evidence → pair nuclear+ponytail → optimize → /code-review капстон. Усе в RepoPrompt-сабагентах, коміт після кожної адекватної зміни; після трьох remediation-циклів — Investigate + Oracle."
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

## Пайплайн (7 фаз)

| # | Фаза | Чим запускати | Вихід | Цикл? |
|---|------|---------------|-------|-------|
| 1 | Дослідження | RP workflow **`Investigate`**; вузькі probes — `explore` | file:line edit-site inventory / root cause; Investigate звітує шлях report (default convention `docs/investigations/`), conductor записує його | — |
| 2 | Дизайн (якщо є відкриті дизайн-рішення) | **`oracle_send`** (chat): запропонуй → критикуй відповідь по суті → ітеруй **до збіжності** (звич. 2-3 раунди) | погоджений дизайн | Oracle design iterates до збіжності; unresolved behavior/scope decision → escalation до користувача; без рішення фаза завершується як explicit blocker |
| 3 | Детальний план | RP workflow **`Deep Plan`** → `docs/plans/`; потім bounded **design-critique** (agent_run `model_id=design`, max-1-page, ТІЛЬКИ прогалини/суперечності/порядок — НЕ переписування дизайну) → зафолдити | executable по-кроковий план | — |
| 4 | Ревʼю плану | RP workflow **`Review`** як `pair`: звірити план проти critique+inventory; явно вказати: review only plan file as a document artifact, do not ask for git comparison scope | 0 P0-P1 у плані | до 3 qualifying plan-remediation cycles; далі Investigate + Oracle |
| 5 | Імплементація | RP workflow **`Orchestrate`** (`agent_run workflow_name="Orchestrate"`) | код, коміт+DoD після КОЖНОГО кроку | — |
| 6 | Ревʼю коду | RP workflow **`Review`** як `pair` на діффі імплементації | 0 P0-P1 на immutable candidate identity | до 3 qualifying code-remediation cycles; далі Investigate + Oracle |
| 7 | Якість + капстон | після promotion: canonical **nuclear** + **ponytail** skills як `pair` (паралельно) → RP workflow **`Optimize`** (запускати завжди: виконати Phase-1 scouting; повний performance loop продовжувати лише за наявності вимірюваної метрики або hot path, інакше зафіксувати explicit N/A verdict) → built-in **`/code-review`** | фінальний gate на promoted frozen identity | будь-яка gate-driven мутація → DoD, новий candidate, повна фаза 6, promotion і всі gates фази 7 |

Малі задачі: фази 2-4 можна стиснути (дизайн тривіальний → одразу план + critique), але
**фази 1, 5-7 не пропускати ніколи**.

## Контракт реального виклику
У фазі 0 один раз виконати `agent_manage op=list_workflows` і
`agent_manage op=list_agents`; зберегти exact workflow та role names verbatim без case
normalization і без висновків із подібних назв. Required workflow identities:
`Investigate`, `Deep Plan`, `Review`, `Orchestrate`, `Optimize`.

Для кожної фази:
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

Same-named host skill може бути лише джерелом contract після знаходження й перевірки його
повного файла; host-side invocation за ім'ям не є fallback для змістовної роботи.

Skill files шукати лише в реально доступних для active host місцях:
- addressable cookbook checkout;
- Codex: `$HOME/.agents/skills/<name>/SKILL.md`;
- Claude Code: `$HOME/.claude/skills/<name>/SKILL.md`.
Перед передачею RP-агенту шлях має бути абсолютним, читабельним і вказувати на повний файл.
Прив'язка unrelated target repo не робить cookbook-relative `skills/<name>/SKILL.md`
доступним.

`rp-ponytail-review` і `rp-thermo-nuclear-code-quality-review` — individual skill leaves.
Composite workflow, що містить їх, не задовольняє жодну з цих leaf capabilities.

У фазі 0 capability-check обов'язкового built-in `/code-review` gate. Цей runbook визнає
його Claude Code-only capability. Якщо active host його не надає, продовжувати можна лише
коли заздалегідь узгоджено explicit supported-host handoff із поверненням результату цьому
conductor; інакше записати explicit blocker і зупинитися. Ніколи не пропускати gate мовчки
й не вигадувати еквівалент.

## Правила циклів (loop-engineering)
- Вести два незалежні лічильники, початково `0`: `plan_remediation_count` для фази 4 та
  `code_remediation_count` для фаз 6-7. Plan-цикл не споживає code-бюджет і навпаки.
  Кожен лічильник належить поточній remediation epoch відповідного artifact.
- Before counters or stop rules apply, the parent conductor adjudicates every child/leaf
  finding into P0/P1/P2 by impact and evidence, never by leaf section or tag. Nuclear and
  Ponytail are not expected to emit P0/P1/P2. After this mapping, the existing
  CONFIRMED/PLAUSIBLE/REFUTED adjudication applies.
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
  scouting (і, якщо обґрунтовано, новим explicit N/A), built-in `/code-review`.
- Discretionary P2 changes, які вирішено робити, обовʼязково згрупувати й завершити до
  candidate capture. P2 можна відкласти без patch; будь-який P2 patch після promotion
  інвалідовує frozen identity і вимагає повного шляху DoD → новий candidate → фаза 6 →
  promotion exact same identity → усі gates фази 7.
- Знахідки, що змінюють поведінку/скоуп, негайно передавати користувачу з рекомендацією,
  не patchити автономно. Без рішення це explicit blocker. Вибір користувача не може waive
  `CONFIRMED` P0/P1: його треба виправити й отримати `"no P0-P1"` на новій exact identity
  або завершити процес як blocker; так само не можна waive обовʼязковий gate.

## Candidate identity, freeze surface і фінальні докази
The **canonical freeze actor/input universe** is authoritative resolved DoD commands,
Phase-6 `Review` including every nested `context_builder` invocation, and Phase-7 gates.
Before candidate capture, record one **closed allowed input/scope manifest** containing every
repo/worktree/submodule/external path and the permitted traversal/discovery bounds for all
actors in that universe. A covered path is within those bounds or otherwise directly consumed.

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
`Optimize` і built-in `/code-review`. Adversarial verify може лише доповнювати ці докази,
але ніколи не замінює жоден required gate.

## DoD кожного кроку імплементації (не торгується)
```
go build ./...                                  # (або еквівалент стеку)
go vet <ТІЛЬКИ змінені пакети>                  # scoped! див. нижче
go test <змінені області> ./... (relevant)
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
  на діффі через перевірений absolute `SKILL.md` path. Якщо агент misfire (0 tool-uses,
  миттєвий вихід) — перезапусти. Це окремий launch failure, не stall evidence і не витрачає
  єдиний retry для позитивно доведеного stall.
- Housekeeping: `agent_manage op=cleanup_sessions` після фіксації результату.

## Чому фазу 7 не можна пропускати (перевірено практикою)
Кожен шар ловить СВІЙ клас дефектів, які інші пропускають:
- **ponytail** ловить консистентність типу value↔pointer/assertion і мертвий код, який
  correctness-ревʼю і тести пропускають;
- **nuclear** ловить over-engineering (спекулятивні абстракції, мертві policy-механізми) —
  видаляй одразу, код має ЗМЕНШУВАТИСЬ після цієї фази;
- **`/code-review` капстон** ловить те, що всі внутрішні проходи пропустили (wire-format
  баги, крос-системні контракти). Це фінальний gate перед push.
- **rp-optimize**: повний перф-цикл запускати лише коли є метрика/гарячий шлях; для
  структурних змін чесно виконати Phase-1 scouting (пошук внесених неефективностей) і, якщо
  чисто, зафіксувати N/A — не імітувати цикл.

## Політика моделей
- **Built-in `/code-review` (є лише в Claude Code): усі сабагенти (finder/verifier/sweep)
  запускати з моделлю `opus` — максимальна, НЕ Fable.** У Workflow-скрипті: `agent(prompt,
  {model: 'opus', …})`; через Agent tool: параметр `model: "opus"`.
- Решта фаз — RepoPrompt-ролі використовують свої дефолти (`agent_manage op=list_agents`).

## Промпт-гігієна для ревʼюерів
- У КОЖЕН finder/verifier передавай **KNOWN-INTENTIONAL список** (свідомі рішення, backward-compat
  винятки, відкладені known-minor) — інакше ревʼю нескінченно ре-флагає те саме.
- Reviewer фази 6 передавай full base/head OID та повний опис immutable candidate identity;
  reviewer фази 7 — exact promoted frozen identity. Evidence чинний лише для переданої identity.
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
не ре-флагали); відкриті питання користувачу.
