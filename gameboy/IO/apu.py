class APU:
    def __init__(self):
        self.channel1 = bytearray(5)
        self.channel1_mask = [0xFF, 0b11000000, 0xFF, 0x00, 0b01000000]
        self.channel2 = bytearray(4)
        self.channel2_mask = [0b11000000, 0xFF, 0x00, 0x01000000]
        self.channel3 = bytearray(5)
        self.channel3_mask = [0b10000000, 0x00, 0b01100000, 0x00, 0b01000000]
        self.channel4 = bytearray(4)
        self.channel4_mask = [0b00111111, 0xFF, 0xFF, 0b01000000]
        self.sound_control = bytearray(3)
        self.sound_control_mask = [0xFF, 0xFF, 0xFF]
        self.waveram = bytearray(16)

    def write(self, addrs, value):
        if 0xff10 <= addrs < 0xff15:
            offset = addrs - 0xff10
            self.channel1[offset] = value
        elif 0xff16 <= addrs < 0xff1A:
            offset = addrs - 0xff16
            print(f"{addrs:04x}", offset)
            self.channel2[offset] = value
        elif 0xff1a <= addrs < 0xff1f:
            offset = addrs - 0xff1a
            self.channel3[offset] = value
        elif 0xff20 <= addrs < 0xff24:
            offset = addrs - 0xff20
            self.channel4[offset] = value
        elif 0xff24 <= addrs < 0xff27:
            offset = addrs - 0xff24
            if offset == 2:
                value &= 0b10000000
            self.sound_control[offset] = value
        elif 0xff30 <= addrs < 0xff40:
            offset = addrs - 0xff30
            self.waveram[offset] = value

    def read(self, addrs):
        if 0xff10 <= addrs < 0xff15:
            offset = addrs - 0xff10
            return self.channel1[offset] & self.channel1_mask[offset]
        elif 0xff16 <= addrs < 0xff20:
            offset = addrs - 0xff16
            return self.channel2[offset] & self.channel2_mask[offset]
        elif 0xff1a <= addrs < 0xff1f:
            offset = addrs - 0xff1a
            return self.channel3[offset] & self.channel3_mask[offset]
        elif 0xff20 <= addrs < 0xff24:
            offset = addrs - 0xff20
            return self.channel4[offset] & self.channel4_mask[offset]
        elif 0xff24 <= addrs < 0xff27:
            offset = addrs - 0xff24
            return self.sound_control[offset] & self.sound_control_mask[offset]
        elif 0xff30 <= addrs < 0xff40:
            offset = addrs - 0xff30
            return self.waveram[offset]
        return 0xFF
