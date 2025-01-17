from random import choice

from CybORG.Shared import Observation
from CybORG.Shared.Actions import Action
from CybORG.Shared.Actions.ConcreteActions.StopProcess import StopProcess
from CybORG.Shared.Actions.ConcreteActions.StopService import StopService
from CybORG.Simulator.Session import RedAbstractSession
from CybORG.Simulator.State import State


class Impact(Action):
    def __init__(self, session: int, agent: str, hostname: str):
        super().__init__()
        self.agent = agent
        self.session = session
        self.hostname = hostname

    def sim_execute(self, state: State) -> Observation:
        # find session on the chosen host
        sessions = [s for s in state.sessions[self.agent].values() if s.host == self.hostname]
        if len(sessions) == 0:
            # no valid session could be found on chosen host
            return Observation(success=False)
        # find if any session are already SYSTEM or root
        min_level = 0
        session = None
        for s in sessions:
            # else find if session is Admin or sudo
            if s.username == 'root' or s.username == 'SYSTEM':
                session = s.ident
                obs = Observation(success=True)
                obs.add_session_info(hostid=self.hostname, **s.get_state())
                break
        # else use random session
        if session is None:
            session = choice(sessions).ident

        if state.sessions[self.agent][self.session].ot_service is not None:
            ot_service = state.sessions[self.agent][self.session].ot_service
            # stop the ot service if known else we will just return a failure
            sub_action = StopService(agent=self.agent, session=self.session, service=ot_service, target_session=session)
            obs = sub_action.sim_execute(state)
        else:
            obs = Observation(success=False)

        return obs

    def __str__(self):
        return f"{self.__class__.__name__} {self.hostname}"

class Disrupt(Action):
    def __init__(self, session: int, agent: str, hostname: str):
        super().__init__()
        self.agent = agent
        self.session = session
        self.hostname = hostname
        self.invalid_type = ['RedAbstractSession', 'VelociraptorClient', 'green_session']
        self.invalid_user = ['root',
                             'SYSTEM']

    def sim_execute(self, state: State) -> Observation:
        # find session on the chosen host
        sessions = [s for s in state.sessions[self.agent].values() if s.host == self.hostname]
        if len(sessions) == 0:
            # no valid session could be found on chosen host
            return Observation(success=False)
            
        session = choice(sessions).ident

        hostname = state.sessions[self.agent][session].host
        invalid_type = ['RedAbstractSession', 'VelociraptorClient', 'green_session']
        for proc in state.hosts[hostname].processes:
            # had issues using any to compare
            if proc.name != 'RedAbstractSession' and proc.name != 'VelociraptorClient' and proc.decoy_type.value == False:
            # stop each process on session that isn't root (excluding red and blue sessions)
                sub_action = StopProcess(session=self.session, agent=self.agent, target_session=session, pid=proc.pid)
                sub_action.sim_execute(state)
        return Observation(success=True)

    def __str__(self):
        return f"{self.__class__.__name__} {self.hostname}"
