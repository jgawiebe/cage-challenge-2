from collections import namedtuple

from CybORG.Shared import Scenario
from CybORG.Shared.RedRewardCalculator import DistruptRewardCalculator, PwnRewardCalculator
from CybORG.Shared.RewardCalculator import RewardCalculator

from CybORG.Shared.NewRedRewardCalculator import DoSRewardCalculator, TamperRewardCalculator

class QoSRewardCalculator(RewardCalculator):
    # Calculate punishment for defending agent based on reduction in availability
    def __init__(self, agent_name: str, scenario: Scenario):
        super(QoSRewardCalculator, self).__init__(agent_name)
        self.adversary = scenario.get_agent_info(agent_name).adversary
        self.disrupt_rc = DoSRewardCalculator(self.adversary, scenario)
        self.impacted_hosts = {}

    def reset(self):
        self.disrupt_rc.reset()

    def calculate_reward(self, current_state: dict, action: dict, agent_observations: dict, done: bool) -> float:
        self.impacted_hosts = {}
        reward = -self.disrupt_rc.calculate_reward(current_state, action, agent_observations, done)
        self._calculate_impacted_hosts()
        return reward

    def _calculate_impacted_hosts(self):
        for host, value in self.disrupt_rc.impacted_hosts.items():
            self.impacted_hosts[host] = -1 * value

class IntegrityRewardCalculator(RewardCalculator):
    # Calculate punishment for defending agent based on reduction in availability
    def __init__(self, agent_name: str, scenario: Scenario):
        super(IntegrityRewardCalculator, self).__init__(agent_name)
        self.adversary = scenario.get_agent_info(agent_name).adversary
        self.disrupt_rc = TamperRewardCalculator(self.adversary, scenario)
        self.impacted_hosts = {}

    def reset(self):
        self.disrupt_rc.reset()

    def calculate_reward(self, current_state: dict, action: dict, agent_observations: dict, done: bool) -> float:
        self.impacted_hosts = {}
        reward = -self.disrupt_rc.calculate_reward(current_state, action, agent_observations, done)
        self._calculate_impacted_hosts()
        return reward

    def _calculate_impacted_hosts(self):
        for host, value in self.disrupt_rc.impacted_hosts.items():
            self.impacted_hosts[host] = -1 * value