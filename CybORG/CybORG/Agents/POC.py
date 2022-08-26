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
    print("Setup")
    path = str(inspect.getfile(CybORG))
    #path = path[:-10] + '/Shared/Scenarios/Scenario_Confidentiality.yaml'
    #path = path[:-10] + '/Shared/Scenarios/Scenario_Availability.yaml'
    path = path[:-10] + '/Shared/Scenarios/Scenario_Integrity.yaml'

    agents = {'Red': RedIntegrityAgent,'Green': GreenAgent}
    env = CybORG(path, 'sim', agents=agents)
    
    agent_name = 'Blue'
    #agent = BlueReactRestoreAgent()

    results = env.reset(agent=agent_name)

    reward = 0
    for _ in range(30):
        hosts = []
        success = False
        results = env.step(agent=agent_name)
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

# NOTE: currently no rewards given for pwn in A, I scenarios. 


