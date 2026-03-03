import json
import requests



my_agent = {
    "name" : "Orion",
    "level" : 1
}

def level_up(my_agent):
    my_agent["level"] += 1
    print(my_agent["name"] + " отримав новий рівень")
    return(my_agent)

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
        "Authorization" : "Bearer " + "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"
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


def get_server_temperature():
    return "Температура сервера: 45 градусів"
    