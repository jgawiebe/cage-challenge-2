from CybORG import CybORG
import inspect

from CybORG.Agents.SimpleAgents.KeyboardAgent import KeyboardAgent
from CybORG.Agents.SimpleAgents.GreenAgent import GreenAgent
from CybORG.Agents.Wrappers.BlueTableWrapper import BlueTableWrapper
from CybORG.Agents import B_lineAgent, BlueReactRemoveAgent
from CybORG.Agents.SimpleAgents.Meander import RedMeanderAgent

if __name__ == "__main__":
    print("Setup")
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + '/Shared/Scenarios/Scenario_Integrity.yaml'

    agents = {'Red': RedMeanderAgent,'Green': GreenAgent}
    env = CybORG(path, 'sim', agents=agents)
    
    agent_name = 'Blue'
    agent = BlueReactRemoveAgent()

    results = env.reset(agent=agent_name)

    reward = 0
    for _ in range(30):
        observation = results.observation
        action_space = results.action_space

        action = agent.get_action(observation, action_space)
        results = env.step(agent=agent_name, action=action)

        hosts = []
        for obs_info in results.observation:
            if type(results.observation[obs_info]) == dict:
                hosts.append(results.observation[obs_info]['System info']['Hostname'])
        print(env.get_last_action(agent='Red'), hosts)
        print(env.get_last_action(agent='Blue'))
        #print(results.observation[])
        print('>>> Reward: ', env.get_rewards())

        reward += results.reward
    print('Final Score: ', round(reward, ndigits=1))


