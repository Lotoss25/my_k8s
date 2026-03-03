from crewai import Agent, Task, Crew
from crewai.tools import tool
import os

os.environ["OPENROUTER_API_KEY"] = "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"

@tool("Server Temperature")
def get_server_temperature():
    """Повертає строку з надписом скільки саме градусів температура сервера і чи вона нормальна"""
    return "Температура сервера: 95 градусів"
    

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
    llm = "openrouter/arcee-ai/trinity-large-preview:free"
)

task1 = Task(
    description = "Дізнайся поточну температуру сервера та напиши короткий звіт",
    expected_output = "Короткий звіт про температуру сервера",
    agent = orion
)

task2 = Task(
    description = "Оціни ризики перегріву обладнання українською мовою в одну строку",
    expected_output = "Оцінка ризиків перегріву обладнання українською мовою в одну строку",
    agent = security_agent
)

my_crew = Crew(
    agents = [orion, security_agent],
    tasks = [task1, task2],
    #verbose = True
)



result = my_crew.kickoff()
print(result)
