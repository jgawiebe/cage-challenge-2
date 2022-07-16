import inspect
import os
import json
from tabnanny import verbose
import numpy as np
import subprocess
from shutil import make_archive
from statistics import mean, stdev
from CybORG import CybORG
from CybORG.Agents import B_lineAgent, SleepAgent, GreenAgent
from CybORG.Agents.SimpleAgents.Meander import RedMeanderAgent
from CybORG.Agents.Wrappers import ChallengeWrapper
import ray
from ray import tune
import ray.rllib.algorithms.ppo as ppo
from ray.tune.registry import register_env

MAX_EPS = 100
agent_name = 'Blue'

def wrap(env):
    return ChallengeWrapper(env=env, agent_name='Blue')

def evaluate(steps, trainer):
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + '/Shared/Scenarios/Scenario1b.yaml'
    obs = []
    #print(f'using CybORG v{cyborg_version}, {scenario}\n')
    for num_steps in steps:
        for red_agent in [B_lineAgent]:
            cyborg = CybORG(path, 'sim', agents={'Red': red_agent})
            wrapped_cyborg = wrap(cyborg)
            observation = wrapped_cyborg.reset()
            obs.append(observation)
            # observation = cyborg.reset().observation
            action_space = wrapped_cyborg.get_action_space(agent_name)
            # action_space = cyborg.get_action_space(agent_name)
            total_reward = []
            actions = []
            for i in range(MAX_EPS):
                r = []
                a = []
                # cyborg.env.env.tracker.render()
                for j in range(num_steps):
                    action = trainer.compute_single_action(observation)
                    action_vec = np.zeros(145)
                    action_vec[int(action)] = 1
                    #action = agent.get_action(observation, action_space)
                    observation, rew, done, info = wrapped_cyborg.step(action)
                    obs.append(observation)
                    actions.append(action_vec)
                    # result = cyborg.step(agent_name, action)
                    r.append(rew)
                    # r.append(result.reward)
                    a.append((str(cyborg.get_last_action('Blue')), str(cyborg.get_last_action('Red'))))
                total_reward.append(sum(r))
                # actions.append(a)
                # observation = cyborg.reset().observation
                observation = wrapped_cyborg.reset()
            print(f'Average reward for red agent {red_agent.__name__} and steps {num_steps} is: {mean(total_reward):.1f} with a standard deviation of {stdev(total_reward):.1f}')
            return mean(total_reward), np.mean(np.array(obs), axis=0),  np.mean(np.array(actions), axis=0)

def env_creator(env_config):
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + '/Shared/Scenarios/Scenario1b.yaml'
    agents = {"Red": B_lineAgent, "Green": GreenAgent}
    cyborg = CybORG(scenario_file=path, environment='sim', agents=agents)
    env = ChallengeWrapper(env=cyborg, agent_name='Blue')
    return env

register_env("cyborg", env_creator)

def experiment(config):

    iterations = 10000
    trainer = ppo.PPO(config=config, env="cyborg")
    checkpoint = None
    train_results = {}
    
    allrewards = []
    reward = []
    novel_obs = []
    novel_actions = []

    for i in range(iterations):
        train_results = trainer.train()
        tune.report(**train_results)
        if i % 500 == 0 or i == iterations - 1:
            checkpoint = trainer.save(tune.get_trial_dir())
            r, o, a = evaluate([50], trainer)
            reward.append(r)
            novel_obs.append(o)
            novel_actions.append(a)
    trainer.stop()
    allrewards.append(reward)
    np.save('ppo_reward.npy', np.array(reward))
    np.save('ppo_obs.npy', np.stack(novel_obs))
    np.save('ppo_actions.npy', np.stack(novel_actions))


if __name__ == "__main__":

    ray.init()
    config = ppo.DEFAULT_CONFIG.copy()
    config['framework'] = "tf"
    config['env'] = 'cyborg'
    config['num_gpus'] = 1
    config["num_workers"] = 3
    config['horizon'] = 1024
    config['train_batch_size'] = 1024
    config['sgd_minibatch_size'] = 128
    config['rollout_fragment_length'] = 100
    config['model'] = {
        "fcnet_hiddens": [512, 512],
        "fcnet_activation": "relu"
    }
    config['batch_mode'] = "truncate_episodes"
    config['lambda'] = 0.95
    config['kl_coeff'] = 0.5
    config['clip_rewards'] = True
    config['clip_param'] = 0.1
    config['vf_clip_param'] = 10.0
    config['entropy_coeff'] = 0.01
    config['vf_share_layers'] = True
    # config['num_sgd_iter'] = 10
    # config["exploration_config"] = {
    #     "type": "Curiosity",  # <- Use the Curiosity module for exploring.
    #     "eta": 1.0,  # Weight for intrinsic rewards before being added to extrinsic ones.
    #     "lr": 0.001,  # Learning rate of the curiosity (ICM) module.
    #     "feature_dim": 288,  # Dimensionality of the generated feature vectors.
    #     # Setup of the feature net (used to encode observations into feature (latent) vectors).
    #     "feature_net_config": {
    #         "fcnet_hiddens": [],
    #         "fcnet_activation": "relu",
    #     },
    #     "inverse_net_hiddens": [256],  # Hidden layers of the "inverse" model.
    #     "inverse_net_activation": "relu",  # Activation of the "inverse" model.
    #     "forward_net_hiddens": [256],  # Hidden layers of the "forward" model.
    #     "forward_net_activation": "relu",  # Activation of the "forward" model.
    #     "beta": 0.2,  # Weight for the "forward" loss (beta) over the "inverse" loss (1.0 - beta).
    #     # Specify, which exploration sub-type to use (usually, the algo's "default"
    #     # exploration, e.g. EpsilonGreedy for DQN, StochasticSampling for PG/SAC).
    #     "sub_exploration": {
    #         "type": "StochasticSampling",
    #     }
    # }

    tune.run(
        experiment,
        config=config,
        resources_per_trial=ppo.PPO.default_resource_request(config),
        verbose=0 # Quiet
    )