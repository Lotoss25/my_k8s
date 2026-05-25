from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter
import os


load_dotenv()

mcp_dir = os.path.dirname(os.path.abspath(__file__))

server_params = StdioServerParameters(
    command = "python",
    args = [os.path.join(mcp_dir, "mcp_server.py")]
)


with MCPServerAdapter(server_params) as mcp_tools:
    agent = Agent(
        role = "Techician",
        goal = "solves technician problems",
        backstory = """
        You are a technician with 20 years of experience in solving technical problems.
        """,
        tools = mcp_tools,
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

