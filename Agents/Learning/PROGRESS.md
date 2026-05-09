# 🗺️ Карта прогресу: Python → AI Agent Orchestration

## Що ти вже знаєш (і де це в коді)

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

### Тиждень 3: Async ← файл `async_learn.py`
- `async def`, `await` — неблокуюче очікування
- `asyncio.gather()` — запуск всіх одночасно
- Час = найповільніший, не сума
- Обмеження: `await` тільки в `async def`

### Тиждень 4: Тести ← файл `test_agent.py`
- `pytest` — автоматична перевірка коду
- `assert` — "я стверджую що це правда"
- Файли і функції починаються з `test_`
- `if __name__ == "__main__":` — щоб при імпорті не виконувався зайвий код

### Тиждень 5: CrewAI зсередини + Pydantic ← файл `agent.py` (оновлений)
- CrewAI Agent — звичайний клас з `BaseModel`
- Pydantic `Field()` — валідація замість ручних перевірок
- Pydantic замінює `__init__`, але **не методи і не self**
- Keyword args: `Agent(name="Orion")`
- Не можна додавати поля яких нема в класі

---

## Де зараз (Тиждень 6+)
- [ ] Як `Crew.kickoff()` запускає агентів
- [ ] `Process.sequential` vs `Process.hierarchical`
- [ ] Memory і Knowledge в CrewAI
- [ ] Custom Tools
- [ ] MCP (Model Context Protocol)

## Файли проєкту
```
Agents/Learning/
├── agent.py              ← класи Agent, Auditor, Orchestrator (Pydantic)
├── test_agent.py         ← 5 тестів
├── async_learn.py        ← async/await приклади
├── zabbix_daily_reports.py ← реальний проект (.env, logging, exceptions)
├── python_cheatsheet.md  ← шпаргалка з усіма концепціями
└── .env                  ← секрети (НЕ пушити в git!)
```
