import agent


auditor_agent = {
    "name" : "Auditor",
    "level" : 1
}

def perform_audit(agent):
    print(agent["name"] + " проводить аудит")
    agent["audited"] = True
    return agent

agent = perform_audit(agent.my_agent)
print(agent)