from eudplib import *


def Timeline(loopn):
    v = EUDVariable(0)
    t = EUDVariable()
    t << 0
    if EUDWhile()(t == 0):
        vt = EUDVariable()  # Temporary variable
        vt << v
        yield vt
        EUDSetContinuePoint()
        v += 1
        t << 1
    EUDEndWhile()
    Trigger(v == loopn, v.SetNumber(0))
