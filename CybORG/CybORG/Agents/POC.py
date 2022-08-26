from CybORG import CybORG
import inspect

from CybORG.Agents.SimpleAgents.KeyboardAgent import KeyboardAgent
from CybORG.Agents.SimpleAgents.GreenAgent import GreenAgent
from CybORG.Agents.Wrappers.BlueTableWrapper import BlueTableWrapper
from CybORG.Agents import B_lineAgent, BlueReactRemoveAgent, BlueReactRestoreAgent, BlueMonitorAgent
from CybORG.Agents.SimpleAgents.Meander import RedMeanderAgent
from CybORG.Agents.SimpleAgents.RedAvailabilityAgent import RedAvailabilityAgent
from CybORG.Agents.SimpleAgents.RedIntegrityAgent import RedIntegrityAgent

if __name__ == "__main__":

    scenarios = ['Confidentiality', 'Availability', 'Integrity']
    scenario = 'Confidentiality'

    path = str(inspect.getfile(CybORG))
    path = path[:-10] + f'/Shared/Scenarios/Scenario_{scenario}.yaml'

    # red and blue agents are pulled from the scenario file.
    # This makes for less front-end code. Green agent is optional.
    # It would be cool to modify the reward calculator here but it
    # gets read in from the scenario by the EnvController.
    agents = {'Green': GreenAgent}
    env = CybORG(path, 'sim', agents=agents)

    results = env.reset(agent='Blue')

    reward = 0
    for _ in range(30):
        hosts = []
        success = False
        results = env.step(agent='Blue')
        for obs_info in results.observation:
            if type(results.observation[obs_info]) == dict:
                hosts.append(results.observation[obs_info]['System info']['Hostname'])
            else:
                success = results.observation[obs_info]
        print(env.get_last_action(agent='Red'), hosts)
        print(env.get_last_action(agent='Blue'))
        print('>>> Reward: ', env.get_rewards())

        reward += results.reward
    print('Final Score: ', round(reward, ndigits=1))


