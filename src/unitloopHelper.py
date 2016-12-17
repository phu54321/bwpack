from eudplib import *


def EUDLoopUnit2():
    ptr, epd = EUDCreateVariables(2)
    ptr << 0x59CCA8
    epd << EPD(0x59CCA8)
    if EUDLoopN()(1700):
        ptr2, epd2 = EUDCreateVariables(2)
        SetVariables([ptr2, epd2], [ptr, epd])
        EUDContinueIf(MemoryEPD(epd + (0x0C // 4), Exactly, 0))
        yield ptr, epd
        EUDSetContinuePoint()
        ptr += 336
        epd += 336 // 4
    EUDEndLoopN()
