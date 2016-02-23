# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
# -- own --
from provider.common import register_provider

# -- code --


@register_provider
def noop(conf, user, event):
    pass
