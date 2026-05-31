import tools
from crewai import Agent
from dotenv import load_dotenv

load_dotenv()



manager = Agent(
    role = "Координатор безпеки",
    goal = "Координує команду",
    backstory = "Крутий менеджер, який може координувати велику команду",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    allow_delegation = True
)


ingenier = Agent(
    role = "Інженер з безпеки",
    goal = "Перевіряє сервери на різні негативні чинники",
    backstory = "Дуже крутий інженер зі стажем, знає багато чого і багато що вміє",
    tools = [tools.check_firewall, tools.check_open_ports, tools.check_running_services, tools.check_users, tools.read_history, tools.save_results],
    llm = "gemini/gemini-3.1-flash-lite-preview",
    allow_delegation = False
)


analiser = Agent(
    role = "Аналітик загроз",
    goal = "Аналізує загрози, дає рекомендації по усуненню",
    backstory = "Крутий аналітик зі стажем",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    allow_delegation = False
)
