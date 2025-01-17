
from CybORG import CybORG
import inspect

from CybORG.Agents import TestAgent
from CybORG.Agents.Wrappers.FixedFlatWrapper import FixedFlatWrapper
from CybORG.Agents.Wrappers.IntListToAction import IntListToActionWrapper
from CybORG.Agents.Wrappers.OpenAIGymWrapper import OpenAIGymWrapper
from CybORG.Agents.Wrappers.BaseWrapper import BaseWrapper

MAX_STEPS_PER_GAME = 20
MAX_EPS = 100

class ObservationTrimWrapper(BaseWrapper):
    def __init__(self, env: BaseWrapper=None, agent=None):
        super().__init__(env, agent)

    def observation_change(self, obs):
        return obs[0:238] + obs[2218:2231] + obs[2348:2528] + obs [2708:2733]+ obs[2808:2816]

def run_training_example(scenario):
    print("Setup")
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + f'/Shared/Scenarios/{scenario}.yaml'

    agent_name = 'Red'
    cyborg = OpenAIGymWrapper(agent_name=agent_name, env=IntListToActionWrapper(ObservationTrimWrapper(FixedFlatWrapper(CybORG(path, 'sim')))))

    observation = cyborg.reset(agent=agent_name)
    action_space = cyborg.get_action_space(agent_name)
    print(f"Observation size {len(observation)}, Action Size {action_space}")
    action_count = 0
    agent = TestAgent()
    for i in range(MAX_EPS):  # laying multiple games
        # print(f"\rTraining Game: {i}", end='', flush=True)
        reward = 0
        for j in range(MAX_STEPS_PER_GAME):  # step in 1 game
            action = agent.get_action(observation, action_space)
            next_observation, r, done, info = cyborg.step(action=action)
            action_space = info.get('action_space')
            reward += r

            agent.train(observation)  # training the agent
            observation = next_observation
            if done or j == MAX_STEPS_PER_GAME - 1:
                # print(f"Training reward: {reward}")
                break
        observation = cyborg.reset(agent=agent_name)
        agent.end_episode()

if __name__ == "__main__":
    run_training_example('Scenario2')
