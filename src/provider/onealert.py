# -*- coding: utf-8 -*-

# -- stdlib --
import json

# -- third party --
import requests

# -- own --
from provider.common import register_provider

# -- code --


@register_provider
def onealert(conf, user, event):
    api_key = conf.get('api_key')

    if 'onealert' in user['extra']:
        api_key = user['extra']['onealert']

    if not api_key:
        return

    resp = requests.post(
        'http://api.110monitor.com/alert/api/event',
        headers={'Content-Type': 'application/json'},
        timeout=10,
        data=json.dumps({
            "app": api_key,
            "eventId": event['id'],
            "eventType": 'trigger' if event['status'] == 'PROBLEM' else 'resolve',
            "alarmName": event['expr'],
            "entityName": event['title'],
            "entityId": event['title'],
            "priority": 1,
            "alarmContent": event['text'],
        }),
    )

    if not resp.ok:
        raise Exception(resp.json())
