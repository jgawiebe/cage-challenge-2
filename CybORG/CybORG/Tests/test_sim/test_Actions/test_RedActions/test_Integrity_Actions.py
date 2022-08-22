from CybORG import CybORG
import inspect
import pytest

from CybORG.Shared.Actions.AbstractActions.Tamper import Tamper

def test_scenario1b():
    # create cyborg environment
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + '/Shared/Scenarios/Scenario1b.yaml'
    cyborg = CybORG(path, 'sim')

    # test discover remote systems
    # act on all subnets in action space
    action_space = cyborg.get_action_space('Red')
    hostname = action_space['hostname']
    initial_observation = cyborg.get_observation('Red')
    session = list(action_space['session'].keys())[0]

    def red_tamper(hostname):
        action = Tamper(hostname=hostname, agent='Red', session=session)
        result = cyborg.step(action=action, agent='Red')
        print(result.reward)
    
    red_tamper('User0')