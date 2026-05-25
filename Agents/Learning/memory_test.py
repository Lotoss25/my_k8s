from crewai.tools import tool
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from datetime import datetime
import psutil
import os



load_dotenv()


@tool
def test_pc(query: str = ""):
    """
    аналізує дані сервера
    """
    try:
        disk = psutil.disk_usage('C:\\')
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        return f"Диск використано на {disk.percent}% з {disk.total // (1024**3)}Гб, Процесор використовується на {cpu}%, ОЗУ використовується на {ram}%"
    except Exception as e:
        return f"Unhandled exception {e}"


@tool
def save_results(query: str = ""):
    """Зберігає результати моніторингу у файл. Передай дані для збереження через query."""
    try:
        os.makedirs("reports", exist_ok=True)
        with open("reports/latest.json", "w") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M") + " | " + query)
        return "Saved"
    except Exception as e:
        return f"Unhandled exception {e}"


@tool
def read_history(query: str = ""):
    """loads memory"""
    try:
        with open("reports/latest.json", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "File Not Found"
    



agent = Agent(
    role = "super agent",
    goal = "doing all things",
    backstory = "супер агент, який знає і вміє все",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    tools = [test_pc, save_results, read_history]
)

task = Task(
    agent = agent,
    description = "Аналізує дані з сервера",
    expected_output = "Перевір стан сервера. Якщо є попередні дані — порівняй з ними. Збережи нові дані."
)


crew = Crew(
    agents = [agent],
    tasks = [task]
)


print(crew.kickoff())


