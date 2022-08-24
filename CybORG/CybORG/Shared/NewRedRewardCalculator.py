from collections import namedtuple

from CybORG.Shared import Scenario
from CybORG.Shared.Actions import FindFlag, Impact
from CybORG.Shared.Actions.Action import Action
from CybORG.Shared.Enums import OperatingSystemType
from CybORG.Shared.RewardCalculator import RewardCalculator
from CybORG.Shared.RedRewardCalculator import PwnRewardCalculator

WIN_REWARD = 0
LOSE_REWARD = 0
SESSION_REWARD = 0
ROOT_SESSION_REWARD = 0
LOSE_SESSION_REWARD = 0
LOSE_ROOT_SESSION_REWARD = 0

REWARD_MAX_DECIMAL_PLACES = 1
HostReward = namedtuple('HostReward','confidentiality availability')

# supposed to wrap Pwn calculator with a done clause, need to understand how inheritance works...
class SparseConfidentialityCalculator(RewardCalculator):
    def __init__(self, agent_name: str, scenario: Scenario):
        super().__init__(agent_name)
        self.pwn_calculator = PwnRewardCalculator(agent_name, scenario)
        self.total_reward = 0.0

    def reset(self):
        self.pwn_calculator.reset()

    def calculate_reward(self, current_state: dict, action: dict, agent_observations: dict, done: bool):
        reward = self.pwn_calculator.calculate_reward(current_state, action, agent_observations, done)
        self.total_reward += reward
        if done == True:
            return round(self.total_reward, REWARD_MAX_DECIMAL_PLACES)
        else:
            return 0.0

# the disruptRewardCalculator relies on the presence of OTservice to determine its reward. It checks to see if the
# process exists and gives a reward if it doesn't. This should be expanded to include all services,
# with OTService being higher reward but each service having some impact to the total score. 
class AvailabilityCalculator(RewardCalculator):
    # calculates the reward for disrupting the network
    def __init__(self, agent_name: str, scenario: Scenario):
        super(AvailabilityCalculator, self).__init__(agent_name)
        self.scenario = scenario
        self.procs = None
        self.mapping = {'None': 0.0,
                        'Low': 0.1,
                        'Medium': 1.0,
                        'High': 10.0}

        self.impacted_hosts = {}

    def reset(self):
        self.procs = None

    def calculate_reward(self, current_state: dict, action: dict, agent_observations: dict, done: bool):
        self.impacted_hosts = {}
        disrupted = {}
        # run this block if there's no history on scenario processes
        if self.procs is None:
            self.procs = {}
            # make a dict of all processes indexed by host
            for host_info in current_state.values():
                if type(host_info) is not dict:
                    continue
                # check this line in debugger
                hostname = host_info['System info']['Hostname']
                if 'Processes' in host_info:
                    proc_list = []
                    for proc in host_info['Processes']:
                        proc_list.append(proc)
                    self.procs[hostname] = proc_list
        # compare list of procs that should be there to the list discovered
        for host_info in current_state.values():
            if type(host_info) is not dict:
                continue
            # step through existing hosts
            hostname = host_info['System info']['Hostname']
            if hostname in self.procs:
                if 'Processes' in host_info:
                    # iterate over processes that should exist to isolate missing ones
                    for proc in self.procs[hostname]:
                        if proc not in host_info['Processes']:
                            # less elegant solution is to just count up procs
                            if hostname in disrupted:
                                disrupted[hostname] += 1
                            else:
                                disrupted[hostname] = 1

        # get availability values                    
        availability_scores = [self.mapping[self.scenario.get_host(i).get('AvailabilityValue', 'Low')] for i in disrupted]
        # sum disrupted hosts
        self.impacted_hosts = dict(zip(disrupted,availability_scores))
        for host in self.impacted_hosts:
            disrupted[host] *= self.impacted_hosts[host]

        reward = sum(disrupted.values())
        return round(reward, REWARD_MAX_DECIMAL_PLACES)

class IntegrityCalculator(RewardCalculator):
    # calculates the reward for modifying data on the hosts
    def __init__(self, agent_name: str, scenario: Scenario):
        super(IntegrityCalculator, self).__init__(agent_name)
        self.scenario = scenario
        self.files = None
        self.mapping = {'None': 0.0,
                        'Low': 0.1,
                        'Medium': 1.0,
                        'High': 10.0}

    def reset(self):
        self.files = None

    def calculate_reward(self, current_state: dict, action: dict, agent_observations: dict, done: bool):
        disrupted = []
        for hostname in agent_observations['Red'].data:
            obs_info = agent_observations['Red'].data[hostname]
            if type(obs_info) is not dict:
                continue
            if 'Files' in obs_info:
                # iterate over files in the current obs and give reward for each 'secret.txt'
                for file in obs_info['Files']:
                    if file['File Name'] == 'secret.txt':
                        disrupted.append(hostname)
                                
        # get availability values (to be changed to integrity values)             
        availability_scores = [self.mapping[self.scenario.get_host(i).get('AvailabilityValue', 'Low')] for i in disrupted]
        #self.impacted_hosts = dict(zip(disrupted,availability_scores))
        reward = sum(availability_scores)
        return round(reward, REWARD_MAX_DECIMAL_PLACES)