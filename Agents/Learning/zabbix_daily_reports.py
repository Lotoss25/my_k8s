from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
import os, requests, logging, aiohttp, asyncio
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename="zabbix_agent.log",     # ← ім'я файлу логів
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ZabbixError(Exception): pass

@tool
def get_zabbix_hosts(query: str = ""):
    """Отримує список серверів (хостів), за якими стежить Zabbix."""
    url = os.environ.get("ZABBIX_URL")
    token = os.environ.get("ZABBIX_TOKEN")
    
    headers = {'Content-Type': 'application/json-rpc',
        'Authorization': f'Bearer {token}'
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "name"]
        },
        "id": 1
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        # #logger.info("ВІДПОВІДЬ СЕРВЕРА:", response.text)
        data = response.json()
        
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(url, json=payload, headers=headers) as response:
        #         data = await response.json()


        # Zabbix завжди повертає статус 200, тому помилки шукаємо всередині JSON
        if "error" in data:
            return f"Помилка Zabbix API: {data['error']['data']}"
            
        hosts = data.get("result", [])
        if not hosts:
            return "У Zabbix не знайдено жодного сервера."
            
        result_string = "Знайдені сервери у Zabbix:\n"
        for host in hosts:
            result_string += f"- {host['name']} (ID: {host['hostid']})\n"
            
        return result_string
        
    except requests.ConnectionError:
        logger.error("Zabbix недоступний")
        return "Zabbix недоступний"
    except requests.Timeout:
        logger.error("Zabbix не відповідає (timeout)")
        return "Zabbix не відповідає (timeout)"
    except ValueError:
        logger.error("Zabbix повернув невалідну відповідь")
        return "Zabbix повернув невалідну відповідь"


@tool
def get_zabbix_metrics(host_id: str):
    """Отримує список метрик (Items) та їхні останні значення для конкретного сервера."""
    logger.info(f"ОТРИМУЮ МЕТРИКИ ДЛЯ СЕРВЕРА: {host_id}")
    url = os.environ.get("ZABBIX_URL")
    token = os.environ.get("ZABBIX_TOKEN")
    
    headers = {
        'Content-Type': 'application/json-rpc',
        'Authorization': f'Bearer {token}'
    }
    
    payload = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["itemid", "name", "lastvalue", "units"],
            "hostids": host_id
        },
        "id": 1
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        # async with aiohttp.ClientSession() as session:
        #     async with session.post(url, json=payload, headers=headers) as response:
        #         data = await response.json()
        
        if "error" in data:
            return f"Помилка Zabbix API: {data['error']['data']}"
            
        items = data.get("result", [])
        if not items:
            return "Не знайдено жодної метрики для цього сервера."
            
        result_string = "Останні показники сервера:\n"
        for item in items:
            # Форматуємо рядок, наприклад: "CPU utilization: 25 %"
            result_string += f"- {item['name']}: {item['lastvalue']} {item['units']}\n"
            
        return result_string
        
    except requests.ConnectionError:
        logger.error("Zabbix недоступний")
        return "Zabbix недоступний"
    except requests.Timeout:
        logger.error("Zabbix не відповідає (timeout)")
        return "Zabbix не відповідає (timeout)"
    except ValueError:
        logger.error("Zabbix повернув невалідну відповідь")
        return "Zabbix повернув невалідну відповідь"


@tool
def send_telegram_message(message: str = ""):
    """Відправляє готовий фінальний звіт про стан сервера адміністратору в Telegram."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return "Успішно відправлено в Telegram!"
        else:
            return f"Помилка Telegram: {response.text}"
    except Exception as e:
        return f"Помилка з'єднання: {str(e)}"




security_agent = Agent(
    role = "Спеціаліст з пошуку проблем в ПО",
    goal = "Оцінювати ризики виходу з ладу обладнання",
    backstory = "Ти досвідчений спеціаліст з пошуку проблем в ПО, який вміє оцінювати ризики виходу з ладу обладнання",
    llm = "gemini/gemini-3.1-flash-lite-preview",
    tools = [get_zabbix_hosts, get_zabbix_metrics, send_telegram_message],
    #verbose = True,
    # allow_delegation = True
)

security_task = Task(
    description = 'проаналізуй усі наявні сервери zabbix, а потім за допомогою метода get_zabbix_metrics отримай показники кожного сервера, а потім відправ звіт адміністратору в Telegram',
    expected_output = 'Звіт про стан серверів',
    agent = security_agent
)

crew = Crew(
    agents = [security_agent],
    tasks = [security_task]
)

result = crew.kickoff()
logger.info(result)