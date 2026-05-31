from crewai.tools import tool
from datetime import datetime
import psutil
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(SCRIPT_DIR, "reports")


@tool
def check_open_ports(query: str=""):
    """Перевіряє відкриті порти"""
    try:
        connections = psutil.net_connections(kind='inet')
        lists = [f"Port: {c.laddr.port}, Addr: {c.laddr.ip}" for c in connections if c.status == "LISTEN"]
        return "\n".join(lists)
    except Exception as e:
        return f"Unhandled exception {e}"

@tool
def check_users(query: str=""):
    """Перевіряє кількість системних юзерів"""
    try:
        users = psutil.users()
        lists = [f"User: {user.name}, Host: {user.host}" for user in users]
        return "\n".join(lists)
    except Exception as e:
        return f"Unhandled exception {e}"


@tool
def check_running_services(query: str = ""):
    """Перевіряє запущені служби"""
    try:
        services = psutil.process_iter(['name', 'pid', 'status'])
        lists = [f"Name: {s.name}, PID: {s.pid}, Status: {s.status}" for s in services]
        return "\n".join(lists)
    except Exception as e:
        return f"Unhandled exception {e}"


@tool
def check_firewall(query: str = ""):
    """Перевіряє фаєрвол"""
    try:
        firewall = subprocess.run(
            ["netsh", "advfirewall", "show", "currentprofile"],
            capture_output=True,
            text=True
        )
        return f"State: {firewall.stdout}, Code: {firewall.returncode}"
    except Exception as e:
        return f"Unhandled exception {e}"


@tool
def save_results(query: str = ""):
    """Зберігає результати у файл"""
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        with open(os.path.join(REPORTS_DIR, "latest.json"), "w") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M") + " | " + query)
        return "Saved"
    except Exception as e:
        return f"Unhandled exception {e}"


@tool
def read_history(query: str = ""):
    """Завантажує результати з файлу"""
    try:
        with open(os.path.join(REPORTS_DIR, "latest.json"), "r") as f:
            return f.read()
    except FileNotFoundError:
        return "File Not Found"
