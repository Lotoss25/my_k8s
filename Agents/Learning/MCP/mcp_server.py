from mcp.server.fastmcp import FastMCP


mcp = FastMCP("MonitorServer")



@mcp.tool()
def check_disk_space(query: str = ""):
    """This tool checks the disk space on the local machine.
    """
    import psutil
    disk = psutil.disk_usage('C:\\')
    return f"Диск використано на {disk.percent}% з {disk.total // (1024**3)}Гб"


@mcp.tool()
def check_cpu_usage(query: str=""):
    """
    This tool checks cpu usage on local machine
    """
    import psutil
    cpu = psutil.cpu_percent(interval=1)
    return f"Процесор використовується на {cpu}%"


@mcp.tool()
def check_ram_usage(query: str=""):
    """
    This tool checks ram usage on local machine
    """
    import psutil
    ram = psutil.virtual_memory().percent
    return f"ОЗУ використовується на {ram}%"



if __name__ == "__main__":
    mcp.run(transport="stdio")