    
from .ConcreteAction import ConcreteAction
from CybORG.Shared import Observation
from CybORG.Shared.Actions.ConcreteActions.ConcreteAction import ConcreteAction
from CybORG.Shared.Enums import OperatingSystemType
from CybORG.Simulator.Host import Host
from CybORG.Simulator.Session import Session
from CybORG.Simulator.State import State

class AddFile(ConcreteAction):    
    def __init__(self, session: int, agent: str, target_session: int):
        super().__init__(session, agent)
        self.state = None
        self.target_session = target_session


    def sim_execute(self, state: State) -> Observation:

        self.state = state
        obs = Observation()
        target_host = state.hosts[state.sessions[self.agent][self.target_session].host]
        target_session = state.sessions[self.agent][self.target_session]

        obs = self.__drop_file(target_host, target_session)
        
        return obs

    def __drop_file(self, target_host: Host, session: Session):

        if target_host.os_type == OperatingSystemType.WINDOWS:
            path = 'C:\\temp\\'
        elif target_host.os_type == OperatingSystemType.LINUX:
            path = '/tmp/'
        else:
            return Observation(False)

        obs = Observation()
        name = 'secret.txt'
        username = target_host.get_process(session.pid).user
        target_host.add_file(name, path, username, 7,
                density=0.9, signed=False)
                
        obs.set_success(True)
        obs.add_file_info(hostid=target_host.hostname, path=path, name=name)
        return obs