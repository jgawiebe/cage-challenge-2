from atexit import register
from os.path import dirname, abspath
from os import environ
# Needed because libiomp5md error gets thrown 
# https://stackoverflow.com/questions/64209238/error-15-initializing-libiomp5md-dll-but-found-libiomp5md-dll-already-initial
# environ['KMP_DUPLICATE_LIB_OK']='True'
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
import inspect
from CybORG import CybORG
from CybORG.Agents import B_lineAgent
from CybORG.Agents.Wrappers import ChallengeWrapper

import argparse
import numpy as np

import ray
from ray import tune
import ray.rllib.algorithms.ppo as ppo
from ray.tune.registry import register_env
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.models.catalog import ModelCatalog
from ray.rllib.utils.framework import try_import_torch

parser = argparse.ArgumentParser()
parser.add_argument("--train-iterations", type=int, default=10)
torch, _ = try_import_torch()

# The custom model that will be wrapped by an LSTM.
class MyCustomModel(TorchModelV2):
    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        super().__init__(obs_space, action_space, num_outputs, model_config, name)
        self.num_outputs = int(np.product(self.obs_space.shape))
        self._last_batch_size = None

    # Implement your own forward logic, whose output will then be sent
    # through an LSTM.
    def forward(self, input_dict, state, seq_lens):
        obs = input_dict["obs_flat"]
        # Store last batch size for value_function output.
        self._last_batch_size = obs.shape[0]
        # Return 2x the obs (and empty states).
        # This will further be sent through an automatically provided
        # LSTM head (b/c we are setting use_lstm=True below).
        return obs * 2.0, []

    def value_function(self):
        return torch.from_numpy(np.zeros(shape=(self._last_batch_size,)))


def env_creator(env_config):
    path = str(inspect.getfile(CybORG))
    path = path[:-10] + '/Shared/Scenarios/Scenario1b.yaml'
    cyborg = CybORG(path, 'sim', agents={'Red': B_lineAgent})
    env = ChallengeWrapper(env=cyborg, agent_name='Blue')
    return env

ModelCatalog.register_custom_model("my_torch_model", MyCustomModel)
register_env("cyborg", env_creator)

def experiment(config):

    iterations = config.pop("train-iterations")
    algo = ppo.PPO(config=config, env="cyborg")
    checkpoint = None
    train_results = {}

    # Train
    for i in range(iterations):
        train_results = algo.train()
        if i % 2 == 0 or i == iterations - 1:
            checkpoint = algo.save(tune.get_trial_dir())
        tune.report(**train_results)
    algo.stop()

    # Manual Eval
    config["num_workers"] = 0
    eval_algo = ppo.PPO(config=config, env="cyborg")
    eval_algo.restore(checkpoint)
    env = eval_algo.workers.local_worker().env

    obs = env.reset()
    done = False
    eval_results = {"eval_reward": 0, "eval_eps_length": 0}
    while not done:
        action = eval_algo.compute_single_action(obs)
        next_obs, reward, done, info = env.step(action)
        eval_results["eval_reward"] += reward
        eval_results["eval_eps_length"] += 1
    results = {**train_results, **eval_results}
    tune.report(results)


if __name__ == "__main__":
    args = parser.parse_args()
    ray.init(num_cpus=3)
    config = ppo.DEFAULT_CONFIG.copy()
    config={
        "framework": "torch",
        "model": {
            # Auto-wrap the custom(!) model with an LSTM.
            "use_lstm": True,
            # To further customize the LSTM auto-wrapper.
            "lstm_cell_size": 64,
            # Specify our custom model from above.
            "custom_model": "my_torch_model",
            # Extra kwargs to be passed to your model's c'tor.
            "custom_model_config": {},
        }
    }
    config["train-iterations"] = args.train_iterations
    config["env"] = "cyborg"
    tune.run(
        experiment,
        config=config,
        resources_per_trial=ppo.PPO.default_resource_request(config),
    )