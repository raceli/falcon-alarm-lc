# -*- coding: utf-8 -*-

# -- stdlib --
from functools import partial
import json

# -- third party --
import gevent
import gevent.pool
import redis
import requests

# -- own --
from state import State
import provider


# -- code --
pool = gevent.pool.Pool(20)


def get_relevant_entities(ev):
    url = '%s/api/action/%s' % (State.config['api']['portal'], ev['action_id'])
    groups = requests.get(url).json()['data']['uic'].split(',')
    users = {}

    for g in groups:
        url = '%s/team/users' % State.config['api']['uic']
        for u in requests.get(url, params={'name': g}).json()['users']:
            u = provider.common.cook_user(u)

            try:
                threshold = int(u['extra']['threshold'])
            except:
                threshold = 999

            if not threshold > ev['level']:
                continue

            users[u['id']] = u

    return groups, users.values()


def get_relevant_providers(ev):
    lvl = str(ev['level'])
    return [
        partial(provider.from_string(conf['provider']), conf)
        for conf in State.config['strategy']
        if lvl in str(conf['level'])
    ]


def merge(ev, groups, users):
    alarms = State.alarms
    ev = dict(ev)
    ev.update({
        'groups': groups,
        'users': users,
    })
    if ev['status'] == 'PROBLEM':
        alarms[ev['id']] = ev
    else:
        alarms.pop(ev['id'], '')


def process_single_event(raw):
    ev = provider.common.cook_event(raw)
    groups, users = get_relevant_entities(ev)
    providers = get_relevant_providers(ev)

    merge(ev, groups, users)

    for u in users:
        for p in providers:
            p(u, ev)


def process_events():
    r = redis.from_url(State.config['redis'])
    queues = [
        'event:p%s' % i for i in
        xrange(State.config['max_level'] + 1)
    ]

    while True:
        q, raw = r.blpop(queues)
        pool.spawn(process_single_event, json.loads(raw))
