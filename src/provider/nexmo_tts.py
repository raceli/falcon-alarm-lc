# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
import requests

# -- own --
from provider.common import register_provider

# -- code --


@register_provider
def nexmo_tts(conf, user, event):
    if not user['phone']:
        return

    if event['status'] != 'PROBLEM':
        return

    requests.post('https://api.nexmo.com/tts/json', params={
        'api_key': conf['api_key'],
        'api_secret': conf['api_secret'],
        'to': '86' + user['phone'],
        'voice': conf['voice'],
        'lg': conf['lg'],
        'repeat': conf['repeat'],
    }, data={'text': conf['prefix'] + event['note']})
