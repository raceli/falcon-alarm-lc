# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import yaml
from example_data import user_example, template_event_example


class TestProvider(object):

    @classmethod
    def setUpClass(cls):
        confs = yaml.load(open('config/config-for-testing.yaml').read())['strategy']
        confs = {i['provider']: i for i in confs}
        cls.confs = confs

    def do_tezt_provider(self, name):
        import provider
        f = provider.from_string(name)
        f(self.confs[name], user_example, provider.common.cook_event(template_event_example))

    # def test_bearychat(self):
    #     return self.do_tezt_provider('bearychat')

    # def test_nexmo_tts(self):
    #     return self.do_tezt_provider('nexmo_tts')

    # def test_noop(self):
    #     return self.do_tezt_provider('noop')

    # def test_pagerduty(self):
    #     return self.do_tezt_provider('pagerduty')

    # def test_smtp(self):
    #     return self.do_tezt_provider('smtp')

    # def test_yunpian_sms(self):
    #     return self.do_tezt_provider('yunpian_sms')

    # def test_onealert(self):
    #    return self.do_tezt_provider('onealert')
