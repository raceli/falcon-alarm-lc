# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
import requests

# -- own --
from provider.common import register_provider


# -- code --
@register_provider
def yunpian_sms(conf, user, event):
    if not user['phone']:
        return

    msg = u'【%s】%s[P%s]\n%s\n' % (
        conf['signature'],
        u'😱' if event['status'] == 'PROBLEM' else u'😅',
        event['level'],
        event['title'],
    ) + event['text']

    rst = requests.post('http://yunpian.com/v1/sms/send.json', data={
        'apikey': conf['api_key'],
        'mobile': user['phone'],
        'text': msg,
    }).json()

    if rst['code'] != 0:
        raise Exception(rst['detail'])
