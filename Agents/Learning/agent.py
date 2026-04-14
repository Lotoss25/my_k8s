import json
import requests



# my_agent = {
#     "name" : "Orion",
#     "level" : 1
# }

class Agent:
    def __init__(self, name):
        self.name = name
        self.level = 1

    def level_up(self):
        self.level += 1
        print(self.name + " отримав новий рівень")
        return(self)
    
    def __str__(self):
        return(f"Мій нік: {self.name}, мій рівень: {self.level}")

class AuditorAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.audits = 0
    
    def audit(self, target: Agent):
        if not isinstance(target, Agent):
            print("Неможливо провести аудит")
            return
        self.audits +=1
        target.audited = True
        print(f"{self.name} проводить аудит {target.name}")


class OrchestratorAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.team = []
    def summon(self, agent: Agent):
        self.team.append(agent)
    def __str__(self):
        names = [agent.name for agent in self.team]
        return(f"Мій нік: {self.name}, моя команда: {names}")




def analyze_error(error_message):
    analyze = {
        "model" : "arcee-ai/trinity-large-preview:free",
        "messages" : [
            {"role" : "user", "content" : error_message}
        ],
        "tools" : [
            {
                "type": "function",
                "function": {
                    "name": "get_server_temperature",
                    "description": "Отримати температуру сервера"
                }
            }
        ]
    }
    api_headers = {
        "Authorization" : "Bearer " + "your_openrouter_api_key"
    }
    req = requests.post("https://openrouter.ai/api/v1/chat/completions", json=analyze, headers=api_headers)
    ai_message = req.json()["choices"][0]["message"]
    if "tool_calls" in ai_message:
        tool_result = get_server_temperature()
        second_pass_data = {"model" : "arcee-ai/trinity-large-preview:free",
        "messages" : [
            {"role" : "user", "content" : "Я виконав функцію. Ось результат: " + tool_result + " Напиши одним реченням і стисло в одну строку."}
        ]
        }
        req = requests.post("https://openrouter.ai/api/v1/chat/completions", json=second_pass_data, headers=api_headers)
        return req.json()["choices"][0]["message"]["content"]
    else:
        return ai_message["content"]

orion = Agent("Orion")
checker = AuditorAgent("Checker")

orion.level_up()
orion.level_up()
Agent.level_up(orion)
checker.level_up()
checker.audit(orion)

commander = OrchestratorAgent("Commander")
commander.summon(orion)
commander.summon(checker)

print(orion)
print(checker)
print(commander)
print(orion.audited)


def get_server_temperature():
    return "Температура сервера: 45 градусів"
    