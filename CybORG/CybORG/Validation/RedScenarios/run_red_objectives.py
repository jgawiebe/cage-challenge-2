from CybORG import CybORG
import inspect
import json
from statistics import mean

from CybORG.Agents.SimpleAgents.KeyboardAgent import KeyboardAgent
from CybORG.Agents.SimpleAgents.GreenAgent import GreenAgent
from CybORG.Agents.Wrappers.BlueTableWrapper import BlueTableWrapper
from CybORG.Agents import B_lineAgent, BlueReactRemoveAgent, BlueReactRestoreAgent, BlueMonitorAgent
from CybORG.Agents.SimpleAgents.Meander import RedMeanderAgent
from CybORG.Agents.SimpleAgents.RedAvailabilityAgent import RedAvailabilityAgent
from CybORG.Agents.SimpleAgents.RedIntegrityAgent import RedIntegrityAgent


def run_red_scenarios(scenario, trials=10, steps=30):

    path = str(inspect.getfile(CybORG))
    path = path[:-10] + f'/Validation/RedScenarios/Scenario_{scenario}.yaml'

    # red and blue agents are pulled from the scenario file.
    # This makes for less front-end code. Green agent is optional.
    # It would be cool to modify the reward calculator here but it
    # gets read in from the scenario by the EnvController.
    agents = {'Green': GreenAgent}
    output = {}
    all_scores = []
    for trial in range(trials):
        env = CybORG(path, 'sim', agents=agents)
        results = env.reset(agent='Blue')
        reward = 0
        ntrial = f'Trial {trial}'
        output[ntrial] = {}
        for i in range(steps):
            results = env.step(agent='Blue')
            reward += results.reward
            output[ntrial][f'Action {i}'] = {
                'Blue' : str(env.get_last_action(agent='Blue')), 
                'Green' : str(env.get_last_action(agent='Green')), 
                'Red' : str(env.get_last_action(agent='Red')) 
            }
            # bug with dict update overwriting all previous i entries.
            # Using str() as temp fix.
            output[ntrial][f'Reward {i}'] = str(env.get_rewards())
        output[ntrial]['Trial Score'] = round(reward, ndigits=1)
        all_scores.append(output[ntrial]['Trial Score'])

    output['Average Score'] = mean(all_scores)
    return output

if __name__ == "__main__":
    scenarios = ['Confidentiality', 'Availability', 'Integrity']
    # for testing
    #scenarios = ['Confidentiality']

    save_path = str(inspect.getfile(CybORG))
    save_path = save_path[:-10] + f'/Validation/RedScenarios/Output_RedObjectives.json'
    output = {}

    for scenario in scenarios:
        # validate results with 10 trials
        output[f'{scenario} Scenario'] = run_red_scenarios(scenario, trials=10, steps=30)
        #output = run_red_scenarios(scenario, trials=1, steps=30)

    json_output = json.dumps(output)
    with open(save_path, 'w') as file:
        file.write(json_output)
