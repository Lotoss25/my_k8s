import agent
import auditor_agent


if __name__ == "__main__":
    agent.level_up(agent.my_agent)
    auditor_agent.perform_audit(agent.my_agent)
    print(agent.my_agent)
    if agent.my_agent["audited"] == True:
        print(agent.analyze_error("Яка температура на сервері? "))
    else:
        print("Agent not audited")