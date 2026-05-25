from crewai.tools import tool
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import psutil

load_dotenv()


@tool
def test_pc(query: str = ""):
    """
    Перевіряє стан сервера
    """
    try:
        disk = psutil.disk_usage('C:\\')
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        return f"Диск використано на {disk.percent}% з {disk.total // (1024**3)}Гб, Процесор використовується на {cpu}%, ОЗУ використовується на {ram}%"
    except Exception as e:
        return f"Unhandled exception {e}"



manager = Agent(
    role = "Керує своїм підрозділом",
    goal = "Знайти кому делегувати завдання",
    backstory = "Супер менеджер, який активно вміє делегувати завдання",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    allow_delegation = True
)


ingenier = Agent(
    role = "Інженер-спец",
    goal = "Вміє виконувати завдання з тестування і ремонту техніки",
    backstory = "Спеціаліст з великим стажем і вмінням",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    allow_delegation = False,
    tools = [test_pc]
)


task = Task(
    description = "Перевіряє дані з сервера",
    expected_output = "Підготуй звіт про стан сервера",
    agent = manager
)


crew = Crew(
    agents = [ingenier, manager],
    tasks = [task]
)


print(crew.kickoff())
