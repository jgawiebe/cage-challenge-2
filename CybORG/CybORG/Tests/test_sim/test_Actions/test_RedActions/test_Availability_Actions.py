from CybORG import CybORG
import inspect
import pytest
from CybORG.Shared.Actions.AbstractActions.Impact import Disrupt

from CybORG.Shared.Actions.AbstractActions.Tamper import Tamper
from CybORG.Shared.Actions.AbstractActions.Analyse import Analyse
from CybORG.Shared.Actions.AbstractActions.DataRepair import DataRepair
from CybORG.Shared.Actions.AbstractActions.DiscoverNetworkServices import DiscoverNetworkServices
from CybORG.Shared.Actions.Action import Sleep

def test_scenario():
    # create cyborg environment
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + '/Shared/Scenarios/Scenario_Availability.yaml'
    cyborg = CybORG(path, 'sim')

    # test discover remote systems
    # act on all subnets in action space
    action_space = cyborg.get_action_space('Red')
    hostname = action_space['hostname']
    initial_observation = cyborg.get_observation('Red')
    session = list(action_space['session'].keys())[0]
    blue_session = cyborg.get_observation('Blue')['Defender']['Sessions'][0]['ID']

    def red_disrupt(hostname):
        action = Disrupt(hostname=hostname, agent='Red', session=session)
        result = cyborg.step(action=action, agent='Red')
        print(result.reward)

    def red_sleep(hostname):
        action = Sleep()
        result = cyborg.step(action=action, agent='Red')
        print(result.reward)
    
    def blue_analyze(hostname):
        action = Analyse(hostname=hostname, agent='Blue', session=blue_session)
        result = cyborg.step(action=action, agent='Blue')
        print(result.reward)

    def blue_repair(hostname):
        action = DataRepair(hostname=hostname, agent='Blue', session=blue_session)
        result = cyborg.step(action=action, agent='Blue')
        print(result.reward)
    
    red_sleep('User0')
    red_disrupt('User0')
    blue_analyze('User0')
    blue_repair('User0')
    blue_repair('User0')

# for fast debugging
if __name__ == "__main__":
    test_scenario()
