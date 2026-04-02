class APU:
    def __init__(self):
        self.channel1 = bytearray(5)
        self.channel2 = bytearray(4)
        self.channel3 = bytearray(5)
        self.channel4 = bytearray(4)
        self.sound_control = bytearray(3)
        self.waveram = bytearray(16)

    def write(self, addrs, value):
        if 0xff10 <= addrs < 0xff15:
            offset = addrs - 0xff10
            self.channel1[offset] = value
        elif 0xff16 <= addrs < 0xff20:
            offset = addrs - 0xff16
            self.chanel2[offset] = value
        elif 0xff1a <= addrs < 0xff1f:
            offset = addrs - 0xff1a
            self.channel3[offset] = value
        elif 0xff20 <= addrs < 0xff24:
            offset = addrs - 0xff20
            self.channel4[offset] = value
        elif 0xff24 <= addrs < 0xff27:
            offset = addrs - 0xff24
            self.sound_control[offset] = value
        elif 0xff30 <= addrs < 0xff40:
            offset = addrs - 0xff30
            self.waveram[offset] = value

    def read(self, addrs):
        if 0xff10 <= addrs < 0xff15:
            offset = addrs - 0xff10
            return self.channel1[offset]
        elif 0xff16 <= addrs < 0xff20:
            offset = addrs - 0xff16
            return self.chanel2[offset]
        elif 0xff1a <= addrs < 0xff1f:
            offset = addrs - 0xff1a
            return self.channel3[offset]
        elif 0xff20 <= addrs < 0xff24:
            offset = addrs - 0xff20
            return self.channel4[offset]
        elif 0xff24 <= addrs < 0xff27:
            offset = addrs - 0xff24
            return self.sound_control[offset]
        elif 0xff30 <= addrs < 0xff40:
            offset = addrs - 0xff30
            return self.waveram[offset]
