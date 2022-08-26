from CybORG.Shared import Observation
from CybORG.Shared.Actions.ConcreteActions.ConcreteAction import ConcreteAction
from CybORG.Simulator.Host import Host
from CybORG.Simulator.Process import Process
from CybORG.Simulator.State import State


class StopProcess(ConcreteAction):
    def __init__(self, session: int, agent: str, target_session: int, pid: int):
        super(StopProcess, self).__init__(session, agent)
        self.pid = pid
        self.target_session = target_session

    def sim_execute(self, state: State) -> Observation:
        obs = Observation()
        if self.session not in state.sessions[self.agent] or self.target_session not in state.sessions[self.agent]:
            return Observation(success=False)
        target_host: Host = state.hosts[state.sessions[self.agent][self.target_session].host]
        session = state.sessions[self.agent][self.session]
        target_session = state.sessions[self.agent][self.target_session]

        if not session.active or not target_session.active:
            return Observation(success=False)
        proc = target_host.get_process(self.pid)
        if proc is not None:
            if proc.user != 'root' and proc.user != 'SYSTEM':
                obs.set_success(True)
                self.kill_process(state, target_host, proc)
                return Observation(success=True)
        return Observation(success=False)

    # code adapted from state.remove_process
    def kill_process(self, state: State, host: Host, process: Process):
        agent, session = state.get_session_from_pid(host.hostname, pid=process.pid)
        host.processes.remove(process)
        # reset process with new PID
        process.pid = None
        host.add_process(**process.__dict__)
        if session is not None:
            host.sessions[agent].remove(session)
            session = state.sessions[agent].pop(session)
            session_reloaded = state.add_session(host=host.hostname, user=session.username,
                                                session_type=session.session_type, agent=session.agent,
                                                parent=session.parent, timeout=session.timeout)
