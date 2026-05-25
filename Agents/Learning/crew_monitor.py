from crewai.tools import tool
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import psutil

load_dotenv()

@tool
def check_disk_space(query: str = ""):
    """This tool checks the disk space on the local machine.
    """
    disk = psutil.disk_usage('C:\\')
    return f"Диск використано на {disk.percent}% з {disk.total // (1024**3)}Гб"


@tool
def check_cpu_usage(query: str=""):
    """
    This tool checks cpu usage on local machine
    """
    cpu = psutil.cpu_percent(interval=1)
    return f"Процесор використовується на {cpu}%"


@tool
def check_ram_usage(query: str=""):
    """
    This tool checks ram usage on local machine
    """
    ram = psutil.virtual_memory().percent
    return f"ОЗУ використовується на {ram}%"


agent = Agent(
    role = "Techician",
    goal = "solves technician problems",
    backstory = """
    You are a technician with 20 years of experience in solving technical problems.
    """,
    tools = [check_disk_space, check_cpu_usage, check_ram_usage],
    llm = "gemini/gemini-3.1-flash-lite-preview"
)

analyst = Agent(
    role = "Аналітик",
    goal = "Аналізує все що дадуть",
    backstory = "Аналітик з величезними здібностіми до аналізу всього і вся. З величезним досвідом в області ІТ",
    llm = "gemini/gemini-3.1-flash-lite-preview"
)


task1 = Task(
    description = "Check all state of local machine",
    expected_output = "percent of disk space, cpu and ram usage",
    agent = agent
)

task2 = Task(
    description = "На основі зібраних метрик напиши короткий звіт: що нормально, що потребує уваги",
    expected_output = "На основі зібраних метрик напиши короткий звіт: що нормально, що потребує уваги",
    agent = analyst
)

crew = Crew(
    agents = [agent, analyst],
    tasks = [task1, task2],
    process = Process.sequential
)

print(crew.kickoff())