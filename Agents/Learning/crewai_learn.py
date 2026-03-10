from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
import os

os.environ["OPENROUTER_API_KEY"] = "your_openrouter_api_key"
os.environ["CHROMA_HUGGINGFACE_API_KEY"] = "your_huggingface_api_key"

@tool("Server Temperature")
def get_server_temperature():
    """Повертає строку з надписом скільки саме градусів температура сервера і чи вона нормальна"""
    return "Температура сервера: 95 градусів"
    

@tool("Server Temperature high")
def server_temperature_high():
    """Якщо температура сервера занадто висока, повертає строку з детальною інформацією що саме зробити вже зараз, щоб потім не було гірше"""
    return "Увімкнено аварійне живлення і сирену, вимкнено всі зайві процеси, відправлено повідомлення адміністратору"

orion = Agent(
    role = "Технічний експерт",
    goal = "Зрозуміло пояснювати технічні проблеми",
    backstory = "Ти досвідчений інженер, який вміє пояснювати складний код простими словами",
    llm = "openrouter/stepfun/step-3.5-flash:free",
    tools = [get_server_temperature]
)

security_agent = Agent(
    role = "Спеціаліст з кібербезпеки",
    goal = "Оцінювати ризики перегріву обладнання",
    backstory = "Ти досвідчений спеціаліст з кібербезпеки, який вміє оцінювати ризики перегріву обладнання",
    llm = "openrouter/arcee-ai/trinity-large-preview:free",
    tools = [server_temperature_high]
)

task1 = Task(
    description = "Дізнайся поточну температуру сервера та напиши короткий звіт",
    expected_output = "Короткий звіт про температуру сервера",
    agent = orion
)

task2 = Task(
    description=(
    "Проаналізуй звіт про температуру. "
    "Якщо температура вище 40 градусів, ти ЗОБОВ'ЯЗАНИЙ використати інструмент server_temperature_high. "
    "КРИТИЧНО ВАЖЛИВО: ЗАБОРОНЕНО вигадувати власні поради щодо охолодження або дій. "
    "Ти маєш видати ТІЛЬКИ той точний текст, який поверне тобі інструмент."
    "А тільки після цього додай ще від себе короткий звіт українською мовою з оцінкою ризику або текстом тривоги."
),
    expected_output="""
    ОБОВ'ЯЗКОВИЙ ФОРМАТ ВІДПОВІДІ:
    1. Автоматичні дії: [ТУТ МАЄ БУТИ ТОЧНИЙ ТЕКСТ З ІНСТРУМЕНТА server_temperature_high]
    2. Оцінка ризику: [Твій короткий висновок українською мовою]
    """,
    output_file = 'Agents/Learning/report.md',
    agent = security_agent
)

my_crew = Crew(
    agents = [orion, security_agent],
    tasks = [task1, task2],
    process = Process.hierarchical,
    manager_llm = "openrouter/stepfun/step-3.5-flash:free",
    memory = True,
    embedder={
        "provider": "huggingface",
        "config": {
            "model": "sentence-transformers/all-MiniLM-L6-v2"
        }
    },
    verbose = True
)



result = my_crew.kickoff()
print(result)
