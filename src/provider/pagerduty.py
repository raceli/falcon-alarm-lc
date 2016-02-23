# -*- coding: utf-8 -*-

# -- stdlib --
import json

# -- third party --
import requests

# -- own --
from provider.common import register_provider

# -- code --


@register_provider
def pagerduty(conf, user, event):
    api_key = conf.get('api_key')

    if 'pagerduty' in user['extra']:
        api_key = user['extra']['pagerduty']

    if not api_key:
        return

    resp = requests.post(
        'https://events.pagerduty.com/generic/2010-04-15/create_event.json',
        headers={'Content-Type': 'application/json'},
        timeout=10,
        data=json.dumps({
            'service_key': api_key,
            'incident_key': event['id'],
            'event_type': 'trigger' if event['status'] == 'PROBLEM' else 'resolve',
            'description': event['title'],
            'details': {'detail': event['text']},
        }),
    )
    if not resp.ok:
        raise Exception(resp.json())
