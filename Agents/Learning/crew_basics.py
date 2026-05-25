from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()


researcher = Agent(
    role = "Дослідник",
    goal = "Знайти детальну інформацію по заданій темі",
    backstory = """
    Ти старший дослідник з 20-річним досвідом у AI.
    Твоє завдання - знайти детальну інформацію по заданій темі.
    Використовуй всі доступні інструменти для пошуку інформації.
    """,
    llm = "gemini/gemini-3.1-flash-lite-preview"
)

writer = Agent(
    role = "Копірайтер",
    goal = "Написати звіт на основі дослідження",
    backstory = """
    Ти досвідчений копірайтер з 20-річним досвідом у журналістиці.
    Твоє завдання - написати короткий звіт на основі дослідження.
    """,
    llm = "gemini/gemini-3.1-flash-lite-preview"
)


task1 = Task(
    description="Досліди тему: що таке MCP",
    expected_output = "Детальний опис що таке MCP і для чого він потрібен",
    agent = researcher
)


task2 = Task(
    description="Напиши короткий звіт на основі дослідження",
    expected_output = "Короткий звіт на основі дослідження",
    agent = writer
)


crew = Crew(
    agents = [researcher, writer],
    tasks = [task1, task2],
    process = Process.sequential
)


if __name__ == "__main__":
    result = crew.kickoff()
    print(result)