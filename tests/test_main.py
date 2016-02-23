# -*- coding: utf-8 -*-
import yaml
from example_data import expression_event_example, template_event_example
import json

uic_resp = {
  "msg": "",
  "users": [
    {
      "id": 5,
      "name": "proton",
      "cnname": "meh",
      "email": "bwang@leancloud.rocks",
      "phone": "18612748499",
      "im": "threshold:3",
      "qq": "84065234",
      "role": 0
    }, {
      "id": 2,
      "name": "jwu",
      "cnname": "meow",
      "email": "jwu@leancloud.rocks",
      "phone": "18911674224",
      "im": "",
      "qq": "53791477",
      "role": 1
    }
  ]
}

portal_resp = {
  "data": {
    "after_callback_mail": 0,
    "after_callback_sms": 0,
    "before_callback_mail": 0,
    "before_callback_sms": 0,
    "callback": 0,
    "id": 2,
    "uic": "operation,api",
    "url": ""
  },
  "msg": ""
}


class TestMain(object):

    @classmethod
    def setUpClass(cls):
        from state import State
        confs = yaml.load(open('config/config-for-testing.yaml').read())
        State.config = confs
        State.alarms = {}
        State.options = {}

    def test_process_single_event(self):
        from main import process_single_event
        from httmock import response, HTTMock, urlmatch

        @urlmatch(netloc=r'(portal|uic|api.nexmo.com|yunpian.com)')
        def response_content(url, request):
            print url
            headers = {'Content-Type': 'application/json'}
            if url.netloc == 'portal' and url.path.startswith('/api/action/'):
                return response(200, json.dumps(portal_resp), headers)
            elif url.netloc == 'uic' and url.path == '/team/users':
                return response(200, json.dumps(uic_resp), headers)
            elif url.netloc == 'api.nexmo.com':
                return response(200, '{}', headers)
            elif url.netloc == 'yunpian.com':
                return response(200, '{"code": 0}', headers)
            else:
                raise Exception('Meh!')

        with HTTMock(response_content):
            process_single_event(template_event_example)
            process_single_event(expression_event_example)
