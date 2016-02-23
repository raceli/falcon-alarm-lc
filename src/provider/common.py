# -*- coding: utf-8 -*-

# -- stdlib --
import datetime
import shlex

# -- third party --
# -- own --

# -- code --
PROVIDERS = {}


def register_provider(f):
    PROVIDERS[f.__name__] = f
    return f


def from_string(s):
    return PROVIDERS[s]


def cook_event(event):
    if event['strategy']:
        inner = event['strategy']
        action_id = inner['tpl']['actionId']
    else:
        inner = event['expression']
        action_id = inner['actionId']

    note = inner['note'] or inner['metric']
    title = u'%s: %s' % (event['endpoint'], note)

    expr = u"%s: %s == %.2f %s %s" % (
        inner['metric'], inner['func'],
        event['leftValue'], inner['operator'], inner['rightValue'],
    )

    ts = datetime.datetime. \
        fromtimestamp(event['eventTime']). \
        strftime("%Y-%m-%d %H:%M:%S").decode('utf-8')

    final = [
        (u"Time", ts),
        (u"Step", u"%s / %s" % (event['currentStep'], inner['maxStep'])),
        (u"Expr", expr),
    ]

    relevant_tags = {
        k: event['pushedTags'][k] for k in
        (set(event['pushedTags']) - set(inner['tags']))
    }

    final.extend(relevant_tags.items())

    text = u'\n'.join([u"%s: %s" % (k, v) for k, v in final])

    return {
        # 事件 id，每个事件是唯一的
        u'id':         event['id'],

        # 事件的 action_id，根据这个寻找报警人
        u'action_id':  action_id,

        # 事件的标题
        u'title':      title,

        # 当前报警次数
        u'step':       event['currentStep'],

        # 最大报警次数
        u'max_step':   inner['maxStep'],

        # 事件发生的时间
        u'time':       event['eventTime'],
        u'formatted_time': ts,

        # 事件的级别，0最高，值越大级别越低
        u'level':      inner['priority'],

        # 事件状态，'PROBLEM' 或者是 'OK'
        u'status':     event['status'],

        # open-falcon 中的概念，通常是机器名
        u'endpoint':   event['endpoint'],

        # open-falcon 中的概念，监控数据的名字
        u'metric':     inner['metric'],

        # 相关的 tags （除去了规则中指定的tag）
        u'tags':       relevant_tags,

        # 报警条目的注释
        u'note':       note,

        # 可读的表达式
        u'expr':       expr,

        # 期望值
        u'expected':   inner['rightValue'],

        # 实际值
        u'actual':     event['leftValue'],

        # 显示在报警中的文本
        u'text':       text,
    }


def cook_user(u):
    # (|||ﾟдﾟ)
    extra = shlex.split(u['im'])
    extra = {k: v for k, v in (i.split(':', 1) for i in extra if i)}
    cooked = dict(u)
    cooked.pop('im')
    cooked['extra'] = extra
    return cooked
