# -*- coding: utf-8 -*-

user_example = {
    'id': 3,
    'name': 'proton',
    'cnname': '王滨',
    'email': 'bwang@leancloud.rocks',
    'phone': '18612748499',
    'qq': '84065234',
    'extra': {
        'threshold': '3',
        'bearychat': 'https://hook.bearychat.com/=bw52Y/incoming/3c2a48f7427034f2af65faed68b9d822',
        'pagerduty': '6a885a644d8d47189ecde6a951bb3212',
        'onealert': 'c6f9a559-8dfa-ed6b-248e-32b55af51910',
    }
}


expression_event_example = {
    u'currentStep': 1,
    u'endpoint': u'redis-feed',
    u'eventTime': 1456129801,
    u'expression': {
        u'actionId': 3,
        u'func': u'all(#3)',
        u'id': 1,
        u'maxStep': 3,
        u'metric': u'df.bytes.used.percent',
        u'note': u'TEST',
        u'operator': u'>',
        u'priority': 0,
        u'rightValue': 10,
        u'tags': {u'fstype': u'ext4'}
    },
    u'id': u'e_1_43b2b1fcbf57084371fa6637d915d8eb',
    u'leftValue': 19.887414742862205,
    u'pushedTags': {u'fstype': u'ext4', u'mount': u'/'},
    u'status': u'PROBLEM',
    u'strategy': None
}

template_event_example = {
    u'currentStep': 2,
    u'endpoint': u'docker15',
    u'eventTime': 1455862890,
    u'expression': None,
    u'id': u's_2_cee9e233343680db89c97d5c51b154a3',
    u'leftValue': 100,
    u'pushedTags': {
        u'fstype': u'proc',
        u'mount': u'/run/docker/netns/a79bb84a902a'
    },
    u'status': u'PROBLEM',
    u'strategy': {
        u'func': u'all(#3)',
        u'id': 2,
        u'maxStep': 2,
        u'metric': u'df.bytes.used.percent',
        u'note': u'\u78c1\u76d875%',
        u'operator': u'>=',
        u'priority': 5,
        u'rightValue': 75,
        u'tags': {},
        u'tpl': {
            u'actionId': 2,
            u'creator': u'proton',
            u'id': 3,
            u'name': u'infra.disk',
            u'parentId': 0
        }
    }
}


