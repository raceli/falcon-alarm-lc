# -*- coding: utf-8 -*-

# -- stdlib --
import json

# -- third party --
import requests

# -- own --
from provider.common import register_provider

# -- code --


@register_provider
def bearychat(conf, user, event):
    if 'bearychat' not in user['extra']:
        return

    url = user['extra']['bearychat']

    if event['status'] == 'PROBLEM':
        color = [
            u'#be10c2',  # purple 0
            u'#ef1000',  # red 1
            u'#fbb726',  # orange 2
            u'#fdfd00',  # yellow 3
            u'#f5f5f5',  # grey 4+
        ][min(event['level'], 4)]
    else:
        color = u'#5cab2a'  # green

    requests.post(
        url,
        headers={'Content-Type': 'application/json'},
        timeout=10,
        data=json.dumps({
            'text': event['status'],
            'attachments': [{
                'title': event['title'],
                'text': event['text'],
                'color': color,
            }],
        }),
    )
