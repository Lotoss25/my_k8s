# 🗺️ Карта прогресу: Python → AI Agent Orchestration

## Контекст для AI (прочитай це першим!)

**Хто я:** IT-ениикей зі стажем, переходжу в AI Agent Orchestration Engineer.
**Фон:** DevOps (Linux, Docker, K8s, Terraform, Ansible, Git), базовий Python.
**Мета:** CrewAI + Python на рівні production через 12-тижневий план.
**Стиль навчання:** НЕ писати код за мене! Я пишу сам, AI — наставник/перевіряє.
**Методологія:** Recall кожну сесію (перевірка знань без підглядання), gamification (Diablo-аналогії: суммонер, скелети, данжони).
**Моя проблема:** Раніше вчив з AI і все відклалось на 20%, тому тепер пишу руками.

### Дати сесій
- 12.04.2026 — Тижні 1 (ООП: class, self, __init__, наслідування)
- 13.04.2026 — Тиждень 1 продовження (OrchestratorAgent, super(), list comprehension)
- 14.04.2026 — Тиждень 2 (.env, logging, try/except, custom exceptions)
- 19.04.2026 — Тиждень 2-3 (logging fix, async/await, asyncio.gather)
- 21.04.2026 — Тиждень 3-4 (async recall, pytest, assert, if __name__)
- 23.04.2026 — Тиждень 5 (CrewAI source code, Agent(BaseAgent), Pydantic intro)
- 26.04.2026 — Тиждень 5 (переписали agent.py на Pydantic, оновили тести)
- 27.04.2026 — Recall Тижнів 1-5, створення PROGRESS.md
- 09-10.05.2026 — Recall після 12 днів, повтор super() і Pydantic, старт Тижня 6
- 12-13.05.2026 — Recall, Custom Tools (@tool, psutil, docstring)
- 17.05.2026 — Recall після 4 днів, crew_monitor (2 агенти + tools конвеєр)

### Recall результати (відстежуй прогрес!)
- Тиждень 1 recall: 3/3 ✅ (self, super, наслідування)
- Тиждень 2-3 recall: 4/6 (await і async def — часткові відповіді)
- Тиждень 4 recall: 3/3 ✅ (assert, test_ naming, __name__)
- Тиждень 5 recall: 6/7 (сплутав Pydantic з if __name__)
- 09-10.05 recall: 3/8 → після повтору super() закрито ✅, Pydantic Field частково
- 13.05 recall: 6/8 ✅ (BaseModel і Field нарешті стабільно!)
- 17.05 recall: 5/7 (Agent поля ⚠️, async ❌ знову)

### Слабкі місця (перевіряй частіше!)
- async await vs time.sleep — КОЖЕН раз плутає напрямки! "await = відпусти"
- Agent поля — плутає role/goal/backstory з tools/description
- super() — розуміє приблизно, деталі плаваючі
- ✅ ЗАКРИТО: BaseModel, Field, Task поля, Process регістр

---

## Що вже знаю (і де це в коді)

### Тиждень 1: ООП ← файл `agent.py`
- `class`, `self`, `__init__` — створення класів
- `__str__`, `__repr__` — як об'єкт виглядає при print
- Наслідування (`AuditorAgent(Agent)`) — щоб не копіпастити
- `super().__init__()` — виклик батьківського методу
- `isinstance()` — перевірка типу
- List comprehension — `[x.name for x in list]`

### Тиждень 2: Безпека і помилки ← файл `zabbix_daily_reports.py`
- `.env` + `load_dotenv()` — секрети окремо від коду
- `logging` замість `print` — логи в файл з часом
- `try/except` з **конкретними** помилками (не Exception)
- Custom Exception — `class ZabbixError(Exception): pass`
- `encoding="utf-8"` в logging на Windows

### Тиждень 3: Async ← файл `async_learn.py`
- `async def`, `await` — неблокуюче очікування
- `asyncio.gather()` — запуск всіх одночасно
- Час = найповільніший, не сума
- Обмеження: `await` тільки в `async def`
- aiohttp — async версія requests (не використовуємо в CrewAI tools)

### Тиждень 4: Тести ← файл `test_agent.py`
- `pytest` — автоматична перевірка коду
- `assert` — "я стверджую що це правда"
- Файли і функції починаються з `test_`
- `if __name__ == "__main__":` — щоб при імпорті не виконувався зайвий код
- 5 тестів проходять (creation, level_up, audit, orchestrator, wrong_type)

### Тиждень 5: CrewAI зсередини + Pydantic ← файл `agent.py` (оновлений)
- CrewAI Agent — звичайний клас з `BaseModel` + Pydantic `Field()`
- Pydantic замінює `__init__`, але **не методи і не self**
- Keyword args: `Agent(name="Orion")` замість `Agent("Orion")`
- Не можна додавати поля яких нема в класі (помилка з audited)
- Наслідування без super() — просто додаєш нові поля

---

## Де зараз (Тиждень 6+)
- [x] Як `Crew.kickoff()` запускає агентів
- [x] `Process.sequential` vs `Process.hierarchical` (знає різницю)
- [x] Custom Tools (`@tool`, docstring, psutil)
- [x] Кілька tools + агент сам вибирає
- [x] Два агенти з різними ролями (інженер + аналітик)
- [ ] Memory і Knowledge в CrewAI
- [ ] MCP (Model Context Protocol)
- [ ] Production-grade проєкт (Тижні 9-12)

## Файли проєкту
```
Agents/Learning/
├── agent.py              ← класи Agent, Auditor, Orchestrator (Pydantic)
├── test_agent.py         ← 5 тестів
├── async_learn.py        ← async/await приклади
├── zabbix_daily_reports.py ← реальний проект (.env, logging, exceptions)
├── crew_basics.py        ← CrewAI: Agent, Task, Crew, Process.sequential
├── tool_basics.py        ← Custom Tools: @tool, psutil, 3 tools
├── crew_monitor.py       ← 2 агенти (інженер+аналітик), tools конвеєр
├── crewai_learn.py       ← старий CrewAI код (reference, не підглядувати)
├── python_cheatsheet.md  ← шпаргалка з усіма концепціями
├── PROGRESS.md           ← цей файл
└── .env                  ← секрети (НЕ пушити в git!)
```

## Як продовжити в новій розмові
Скажи AI:
> Я вчу Python + CrewAI. Прочитай файли PROGRESS.md і python_cheatsheet.md
> в папці Agents/Learning/. Там весь мій контекст і прогрес. Продовжуй звідти.
> Стиль: ти навчаєш мене, я пишу код сам, ти перевіряєш. Роби recall кожну сесію.
> Не підігрувай, не пропускай теми. Якщо пройшли дні — перевір що я ще пам'ятаю.
