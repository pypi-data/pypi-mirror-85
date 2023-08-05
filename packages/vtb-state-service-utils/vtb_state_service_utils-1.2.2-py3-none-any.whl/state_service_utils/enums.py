from enum import Enum


class ActionType(Enum):
    DEPLOY = 'deploy'


class ActionSubType(Enum):
    RUN = 'run'
    RUN_NODE = 'run_node'
    ROLLBACK = 'rollback'
    ROLLBACK_NODE = 'rollback_node'


class ActionStatus(Enum):
    STARTED = 'started'
    COMPLETED = 'completed'
    ERROR = 'error'


class EventType(Enum):
    VM = 'vm'
    CLUSTER = 'cluster'


class EventSubType(Enum):
    STATE = 'state'
    CONFIG = 'config'


class EventState(Enum):
    ON = 'on'
    OFF = 'off'
    REBOOT = 'reboot'
    DELETED = 'deleted'


class EventVirtualization(Enum):
    OPENSTACK = 'openstack'
    VMWARE = 'vmware'
    NUTANIX = 'nutanix'
    OPENSHIFT = 'openshift'