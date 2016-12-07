# Code by klassical_31@naver.com
# http://pastebin.com/Vyx02FvJ

from eudplib import *


class KeyState:
    _base_address = 0x596A18

    def __init__(self, *keys):
        keys = list(keys)
        # convert to VK-Codes
        for i, key in enumerate(keys):
            if isinstance(key, str):
                key = key.upper()  # transform to uppercase
                assert len(key) == 1 and ord('0') <= ord(key) <= ord('Z'), \
                    "에러: 키는 한글자 알파벳&숫자 스트링, \
                       혹은 1부터 255까지의 수여야 합니다. '%s' 해석 불가." % key
                keys[i] = ord(key)

        self.dictionary = dict()

        # check for existence from 1 ( VK_LBUTTON ) to 0xFE ( VK_OEM_CLEAR )
        for i in range(0, 0x100):
            if i in keys:
                self.dictionary[i] = {
                    "curr": EUDVariable(),
                    "prev": EUDLightVariable()
                }

    def newlyKeyDown(self, key):
        if isinstance(key, str):
            key = ord(key.upper())  # transform to uppercase
        assert key in self.dictionary, \
            "에러: 해당 키 '%s' 는 초기화 시점 포함되지 않았습니다." % key
        return [self.dictionary[key]["prev"].Exactly(0),
                self.dictionary[key]["curr"].Exactly(1)]

    def newlyKeyUp(self, key):
        if isinstance(key, str):
            key = ord(key.upper())  # transform to uppercase
        assert key in self.dictionary, \
            "에러: 해당 키 '%s' 는 초기화 시점 포함되지 않았습니다." % key
        return [self.dictionary[key]["prev"].Exactly(1),
                self.dictionary[key]["curr"].Exactly(0)]

    def currentlyKeyDown(self, key):
        if isinstance(key, str):
            key = ord(key.upper())  # transform to uppercase
        assert key in self.dictionary,\
            "에러: 해당 키 '%s' 는 초기화 시점 포함되지 않았습니다." % key
        return self.dictionary[key]["curr"].Exactly(1)

    def currentlyKeyUp(self, key):
        if isinstance(key, str):
            key = ord(key.upper())  # transform to uppercase
        assert key in self.dictionary,\
            "에러: 해당 키 '%s' 는 초기화 시점 포함되지 않았습니다." % key
        return self.dictionary[key]["curr"].Exactly(0)

    @EUDMethod
    def update(self):
        '''
       이전 값을 저장하는 곳을 현재 값을 저장하는 곳으로부터 값을 옮기고
       현재 값을 저장하는 곳을 실제로 스타 메모리에서 새롭게 읽어 값을 새로고침해요
       '''

        # update previous values
        for key in self.dictionary:
            Trigger(
                conditions=self.dictionary[key]["curr"].AtLeast(1),
                actions=self.dictionary[key]["prev"].SetNumber(1)
            )
            Trigger(
                conditions=self.dictionary[key]["curr"].Exactly(0),
                actions=self.dictionary[key]["prev"].SetNumber(0)
            )

        # update current values
        for p in range(0, 0x100 // 4):
            broken = None
            for i in range(4):
                if 4 * p + i in self.dictionary:
                    if broken is None:
                        broken = f_dwbreak(
                            f_dwread_epd(EPD(self._base_address) + p))

                    self.dictionary[4 * p + i]["curr"] << broken[2 + i]