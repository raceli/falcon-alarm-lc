# -*- coding: utf-8 -*-
# -- stdlib --
# -- third party --
# -- own --
from provider.common import register_provider

# -- code --


@register_provider
def debug(conf, user, event):
    import pprint
    print '>>>' + '=' * 77
    pprint.pprint(user)
    print '-' * 80
    pprint.pprint(event)
    print '<<<' + '=' * 77
