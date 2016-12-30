from eudplib import *

usernameDb = Db(u2b(settings['username']) + b'\0')
print(u2b(settings['username']) + b'\0')

def onPluginStart():
    # 임시 : 리플레이 방지
    if EUDIf()(Memory(0x6D0F14, AtLeast, 1)):
        for pl in range(8):
            f_setcurpl(pl)
            DoActions([
                DisplayText('\x05Replay blocked'),
                Defeat()
            ])

        if EUDInfLoop()():
            EUDDoEvents()
        EUDEndInfLoop()
    EUDEndIf()

    if EUDIf()(Memory(0x57F0B4, Exactly, 0)):
        DoActions([
            [
                SetCurrentPlayer(player),
                DisplayText('\x05Single play blocked.'),
                Draw()
            ] for player in range(6)
        ])

        if EUDInfLoop()():
            EUDDoEvents()
        EUDEndInfLoop()
    EUDEndIf()

    # ID Check
    allowexec = EUDVariable(0)
    for player in range(8):
        Trigger(
            f_strcmp(0x57EEEB + 36 * player, usernameDb) == 0,
            allowexec.SetNumber(1)
        )

    if EUDIf()(allowexec == 0):
        DoActions([
            DisplayExtText('\x05테스트 버젼 실행시엔 제작자가 필요합니다.'),
            KillUnit('(any unit)', AllPlayers),
            SetMemory(0x6509A0, SetTo, 999999),
            Defeat(),
        ])
        EUDDoEvents()
    EUDEndIf()

    DoActions([
        [
            SetCurrentPlayer(player),
            DisplayText('\x05[TEST VERSION] 제작자 확인 완료.')
        ] for player in range(6)
    ])
