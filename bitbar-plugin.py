#!/usr/bin/python
# -*- coding: utf-8 -*-

# -- stdlib --
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# -- third party --
import requests

# -- own --

# -- code --
BASEURL = 'http://YOUR_URL'
alarms = requests.get(BASEURL + '/api/alarms').json()['alarms']

if alarms:
    print '😱 = %s' % len(alarms)
    print '---'
    for a in alarms:
        if a['tags']:
            t = ','.join(['%s=%s' % (k, v) for k, v in a['tags'].items()])
            t = '[%s]' % t
        else:
            t = ''

        print u'{a[title]}{t} | href={url}#{a[id]}'.format(a=a, t=t, url=BASEURL)
else:
    print u'😆'
