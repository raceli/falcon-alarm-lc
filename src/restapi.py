# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
from bottle import route

# -- own --
from state import State


# -- code --
@route('/api/alarms')
def alarms():
    return {'result': 'success', 'alarms': State.alarms.values()}


@route('/api/alarms/<ids>', method='DELETE')
def resolve(ids):
    ids = ids.split(',')
    alarms = State.alarms
    for i in ids:
        alarms.pop(i, '')

    return {'result': 'success'}
