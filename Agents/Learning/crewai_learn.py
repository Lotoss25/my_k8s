from crewai import Agent, Task, Crew
import os

os.environ["OPENROUTER_API_KEY"] = "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"

orion = Agent(
    role = "Технічний експерт",
    goal = "Зрозуміло пояснювати технічні проблеми",
    backstory = "Ти досвідчений інженер, який вміє пояснювати складний код простими словами",
    llm = "openrouter/arcee-ai/trinity-large-preview:free"
)

task1 = Task(
    description = "Поясни чому це не працює",
    expected_output = "Коротке пояснення проблеми",
    agent = orion
)

my_crew = Crew(
    agents = [orion],
    tasks = [task1]
)

result = my_crew.kickoff()
print(result)
