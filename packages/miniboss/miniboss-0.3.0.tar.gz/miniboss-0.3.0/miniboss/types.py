from typing import NamedTuple

# pylint: disable=inherit-non-class
class Network(NamedTuple):
    name: str
    id: str

# pylint: disable=inherit-non-class
class Options(NamedTuple):
    network: Network
    timeout: int
    run_new_containers: bool
    remove: bool
    run_dir: str

class AgentStatus:
    NULL = 'null'
    IN_PROGRESS = 'in-progress'
    STARTED = 'started'
    FAILED = 'failed'
    STOPPED = 'stopped'

class RunCondition:
    CREATED = 'created'
    STARTED = 'started'
    ALREADY_RUNNING = 'already-running'

class Actions:
    START = 'start'
    STOP = 'stop'
