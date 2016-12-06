from eudplib import *


def Timeline(loopn):
    v = EUDVariable(0)
    yield v
    v += 1
    Trigger(v == loopn, v.SetNumber(0))
