from random import choice

from CybORG.Shared import Observation
from .Monitor import Monitor
from CybORG.Shared.Actions import Action
from CybORG.Shared.Actions.AbstractActions import Monitor
from CybORG.Shared.Actions.ConcreteActions.RemoveFile import RemoveFile
from CybORG.Shared.Actions.ConcreteActions.DensityScout import DensityScout
from CybORG.Shared.Actions.ConcreteActions.SigCheck import SigCheck
from CybORG.Simulator.Session import VelociraptorServer


class DataRepair(Action):
    def __init__(self, session: int, agent: str, hostname: str):
        super().__init__()
        self.agent = agent
        self.session = session
        self.hostname = hostname

    def sim_execute(self, state) -> Observation:
        # perform monitor at start of action
        #monitor = Monitor(session=self.session, agent=self.agent)
        #obs = monitor.sim_execute(state)
    
        parent_session: VelociraptorServer = state.sessions[self.agent][self.session]
        # find relevant session on the chosen host
        sessions = [s for s in state.sessions[self.agent].values() if s.host == self.hostname]
        if len(sessions) > 0:
            session = choice(sessions)
            obs = Observation(True)
            # remove suspicious files
            if self.hostname in parent_session.sus_files:
                for path, sus_file in parent_session.sus_files[self.hostname]:
                    sub_action = RemoveFile(agent=self.agent, session=self.session, target_session=session.ident, path=path, file_name=sus_file)
                    obs = sub_action.sim_execute(state)
                if obs.success == True:
                    del parent_session.sus_files[self.hostname]
            return obs
        else:
            return Observation(False)

    def __str__(self):
        return f"{self.__class__.__name__} {self.hostname}"
    
