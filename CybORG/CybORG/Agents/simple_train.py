import inspect
from CybORG import CybORG
from CybORG.Agents import B_lineAgent, RedMeanderAgent
from CybORG.Agents.SimpleAgents.RLAgent import RLAgent
from CybORG.Agents.Wrappers import ChallengeWrapper


def wrap( env):
    return ChallengeWrapper('Blue', env)


if __name__ == "__main__":

    cyborg_version = '1.2'
    scenario = 'Scenario1b'
    agent_name = 'Blue'

    path = str(inspect.getfile(CybORG))
    path = path[:-10] + '/Shared/Scenarios/Scenario1b.yaml'

    red_agents = [B_lineAgent, RedMeanderAgent]

    RL_algos = ["A2C", "PPO", "DQN"]

    timesteps = 100000

    for red_agent in red_agents:
        for RL_algo in RL_algos:
            cyborg = CybORG(path, 'sim', agents={'Red': red_agent})
            env = wrap(cyborg)
            model = RLAgent(env=env, agent_type = RL_algo)
            model.train(timesteps=int(timesteps), log_name = f"{RL_algo}")
            model.save(f"{RL_algo} against {red_agent.__name__}")
