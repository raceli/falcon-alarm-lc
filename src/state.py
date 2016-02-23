from utils import instantiate


@instantiate
class State(object):
    __slots__ = [
        'config',
        'options',
        'alarms',
    ]
