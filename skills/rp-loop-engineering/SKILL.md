---
name: rp-loop-engineering
description: "Універсальний rp-ce loop-engineering флоу для нетривіальних задач: investigate → oracle-дизайн → deep-plan → pair review-цикл плану → orchestrate → pair review-цикл коду → pair nuclear+ponytail → optimize → /code-review капстон. Усе в RepoPrompt-сабагентах, коміт після кожної адекватної зміни, цикли до 0 P0-P1."
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
| 2 | Дизайн (якщо є відкриті дизайн-рішення) | **`oracle_send`** (chat): запропонуй → критикуй відповідь по суті → ітеруй **до збіжності** (звич. 2-3 раунди) | погоджений дизайн | ♾ до збіжності |
| 3 | Детальний план | RP workflow **`Deep Plan`** → `docs/plans/`; потім bounded **design-critique** (agent_run `model_id=design`, max-1-page, ТІЛЬКИ прогалини/суперечності/порядок — НЕ переписування дизайну) → зафолдити | executable по-кроковий план | — |
| 4 | Ревʼю плану | RP workflow **`Review`** як `pair`: звірити план проти critique+inventory; явно вказати: review only plan file as a document artifact, do not ask for git comparison scope | 0 P0-P1 у плані | ♾ доки 0 P0-P1 |
| 5 | Імплементація | RP workflow **`Orchestrate`** (`agent_run workflow_name="Orchestrate"`) | код, коміт+DoD після КОЖНОГО кроку | — |
| 6 | Ревʼю коду | RP workflow **`Review`** як `pair` на діффі імплементації | 0 P0-P1 у коді | ♾ доки чисто |
| 7 | Якість + капстон | canonical **nuclear** + **ponytail** skills як `pair` (паралельно) → RP workflow **`Optimize`** (якщо є перф-поверхня) → built-in **`/code-review`** | фінальний gate | re-run капстону, якщо його знахідки щось змінили |

Малі задачі: фази 2-4 можна стиснути (дизайн тривіальний → одразу план + critique), але
**фази 1, 5-7 не пропускати ніколи**.

## Контракт реального виклику
У фазі 0 один раз виконати `agent_manage op=list_workflows` і
`agent_manage op=list_agents`; зберегти exact workflow та role names verbatim без case
normalization і без висновків із подібних назв. Required workflow identities:
`Investigate`, `Deep Plan`, `Review`, `Orchestrate`, `Optimize`.

Для кожної фази:
1. Якщо exact workflow identity зареєстрована — запускати її через
   `agent_run op=start workflow_name="<verbatim name>" model_id=<required role>`.
2. Якщо workflow відсутній — знайти в active host або repository inventory повний,
   читабельний `SKILL.md` відповідної capability і перевірити його. Host-registered skill
   name, спільне походження або подібна назва не доводять workflow/skill equivalence.
3. Запустити свіжого RepoPrompt-агента потрібної ролі, наказати йому прочитати весь
   перевірений файл і виконати його verbatim для explicit scope. Це alternate implementation,
   не доведений workflow alias; conductor перевіряє очікуваний output і stop gate фази.
4. Якщо required role, повний skill contract або launch surface недоступні — записати
   explicit blocker і зупинитися. Не переносити змістовну роботу в host conductor і не
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

`rp-loop-engineering`, `Autonomous Slice Loop` і
`Autonomous Slice Loop + Specialist Reviews` — взаємовиключні top-level conductors.
Не запускати Autonomous Slice Loop workflows усередині цього runbook і не підміняти
specialist composite-ом окремий ponytail або thermo-nuclear review.

У фазі 0 capability-check обов'язкового built-in `/code-review` gate. Цей runbook визнає
його Claude Code-only capability. Якщо active host його не надає, продовжувати можна лише
коли заздалегідь узгоджено explicit supported-host handoff із поверненням результату цьому
conductor; інакше записати explicit blocker і зупинитися. Ніколи не пропускати gate мовчки
й не вигадувати еквівалент.

## Правила циклів (loop-engineering)
- **rp-review циклиться** окремо на плані (фаза 4) і на коді (фаза 6): збери P0-P1 → виправ →
  ре-ревʼю. Вихід із циклу — ТІЛЬКИ явний вердикт "no P0-P1".
- **Oracle-дизайн циклиться до збіжності**: не приймай першу відповідь — знайди 3-4 слабких
  місця і пуш-бекни з доказами з коду; зупиняйся, коли обидві сторони прийняли позиції.
- **Капстон-цикл**: якщо `/code-review` знайшов щось і ти пофіксив — закрий петлю: малий
  фікс-діфф → 1 адверсарний verify-агент; великий → повний re-run капстону на фінальному стані.
- Знахідки типу «рішення користувача» (зміна поведінки/скоупу) — НЕ фіксити самому:
  AskUserQuestion з рекомендацією.

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
- Моніторити через `agent_run op=wait` (він може ставити питання → `op=respond`).
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
  миттєвий вихід) — перезапусти.
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
- Verify-фаза адверсарна: вердикти CONFIRMED/PLAUSIBLE/REFUTED, REFUTED відкидається.
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
- 🚫 Спекулятивна загальність (політики/абстракції «на майбутнє», не підключені зараз) — MVP; додаси, коли підключиш.
- 🚫 Фіксити знахідки, що міняють поведінку/скоуп, без рішення користувача.
- 🚫 Лишати процес-артефакти (repro, investigation-доки) у shipping-гілці без явного рішення — зберігай на scratch-гілці (`git branch <name>-artifacts HEAD`).

## Фінальний звіт
Таблиця комітів по кроках; що знайшов кожен шар ревʼю; verification-статус; known-latent/
deferred список (щоб наступні ревʼю не ре-флагали); відкриті питання користувачу.
