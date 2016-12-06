from eudplib import *


def Timeline(loopn):
    v = EUDVariable(0)
    vt = EUDVariable()  # Temporary variable
    vt << v
    yield vt
    v += 1
    Trigger(v == loopn, v.SetNumber(0))
