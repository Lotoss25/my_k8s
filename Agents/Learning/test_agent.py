from agent import Agent, AuditorAgent, OrchestratorAgent

def test_agent_creation():
    orion = Agent(name="Orion")
    assert orion.name == "Orion"
    assert orion.level == 1
    assert orion.audited == False


def test_level_up():
    orion = Agent(name="Orion")
    orion.level_up()
    assert orion.level == 2

def test_auditor_agent():
    checker = AuditorAgent(name="Checker")
    orion = Agent(name="Orion")
    checker.audit(orion)
    assert checker.audits == 1
    assert orion.audited == True

def test_orchestrator_agent():
    orion = Agent(name="Orion")
    second = Agent(name="Second")
    commander = OrchestratorAgent(name="Commander")
    commander.summon(orion)
    commander.summon(second)
    assert len(commander.team) == 2


def test_audit_wrong_type():
    checker = AuditorAgent(name="Checker")
    result = checker.audit("Hello")
    assert checker.audits == 0