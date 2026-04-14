from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
import os, psutil, wmi, requests
from dotenv import load_dotenv
load_dotenv()


w = wmi.WMI(namespace="root\\wmi")
raw_temp = w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature

@tool
def get_server_temperature(query: str = ""):
    """Повертає строку з надписом скільки саме градусів температура сервера і чи вона нормальна"""
    return f"Температура сервера: {(round(raw_temp / 10 - 273.15, 1))} градусів"
    

@tool
def server_temperature_high(query: str = ""):
    """Якщо температура сервера занадто висока, більша за 75 градусів, повертає строку з детальною інформацією що саме зробити вже зараз, щоб потім не було гірше"""
    return "Увімкнено аварійне живлення і сирену, вимкнено всі зайві процеси, відправлено повідомлення адміністратору"

@tool
def server_cpu_and_ram(query: str = ""):
    """Повертає строку з надписом скільки саме навантаження CPU та оперативної пам'яті"""
    return f"Навантаження CPU: {psutil.cpu_percent(interval=1)}%, Навантаження оперативної пам'яті: {psutil.virtual_memory().percent}%"

@tool
def send_telegram_message(message: str = ""):
    """Відправляє готовий фінальний звіт про стан сервера адміністратору в Telegram."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return "Успішно відправлено в Telegram!"
        else:
            return f"Помилка Telegram: {response.text}"
    except Exception as e:
        return f"Помилка з'єднання: {str(e)}"


orion = Agent(
    role = "Технічний експерт",
    goal = "Зрозуміло пояснювати технічні проблеми",
    backstory = "Ти досвідчений інженер, який вміє пояснювати складний код простими словами",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    tools = [get_server_temperature, server_cpu_and_ram]
)

security_agent = Agent(
    role = "Спеціаліст з кібербезпеки",
    goal = "Оцінювати ризики перегріву обладнання",
    backstory = "Ти досвідчений спеціаліст з кібербезпеки, який вміє оцінювати ризики перегріву обладнання",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    tools = [server_temperature_high],
    allow_delegation = True
)

telegram_agent = Agent(
    role = "Спеціаліст з кібербезпеки",
    goal = "Оцінювати ризики перегріву обладнання",
    backstory = "Ти майстер відправки повідомлень в Telegram",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    tools = [send_telegram_message],
    allow_delegation = True
)

task1 = Task(
    description = "Дізнайся поточну температуру сервера та напиши короткий звіт",
    expected_output = "Короткий звіт про температуру сервера",
    agent = orion,
    async_execution = False
)

task1_5 = Task(
    description = "Дізнайся навантаження CPU та оперативної пам'яті",
    expected_output = "Короткий звіт про навантаження CPU та оперативної пам'яті",
    agent = orion,
    async_execution = False
)

task2 = Task(
    description=(
    "Проаналізуй звіт про температуру. "
    "Якщо температура вище 40 градусів, ти ЗОБОВ'ЯЗАНИЙ використати інструмент server_temperature_high. "
    "КРИТИЧНО ВАЖЛИВО: ЗАБОРОНЕНО вигадувати власні поради щодо охолодження або дій. "
    "Ти маєш видати ТІЛЬКИ той точний текст, який поверне тобі інструмент."
    "А тільки після цього додай ще від себе короткий звіт українською мовою з оцінкою ризику або текстом тривоги."
    "Надай дані про навантаження CPU та оперативної пам'яті"
    #"Обов'язково додай у звіт інформацію про швидкість обертання кулерів охолодження. Щоб дізнатися швидкість кулерів, ти ЗОБОВ'ЯЗАНИЙ використати інструмент 'Ask question to co-worker' і запитати про це агента 'Технічний експерт'."
),
    expected_output="""
    ОБОВ'ЯЗКОВИЙ ФОРМАТ ВІДПОВІДІ:
    1. Автоматичні дії: [ТУТ МАЄ БУТИ ТОЧНИЙ ТЕКСТ З ІНСТРУМЕНТА server_temperature_high]
    2. Оцінка ризику: [Твій короткий висновок українською мовою]
    """,
    output_file = 'Agents/Learning/report.md',
    agent = security_agent,
    context = [task1, task1_5]
)

task3 = Task(
    description = "Відправ звіт адміністратору в Telegram за допомогою інструменту send_telegram_message",
    expected_output = "Звіт відправлено адміністратору в Telegram",
    agent = telegram_agent,
    context = [task2],
    async_execution = False
)

my_crew = Crew(
    agents = [orion, security_agent, telegram_agent],
    tasks = [task1, task1_5, task2, task3],
    process = Process.hierarchical,
    manager_llm = "groq/meta-llama/llama-4-scout-17b-16e-instruct",
    memory = True,
    embedder={
        "provider": "google-generativeai",
        "config": {
            "model": "models/embedding-002"
        }
    },
    verbose = True
)



result = my_crew.kickoff()
print(result)
