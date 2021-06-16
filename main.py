from datetime import datetime
import binascii
import struct
import re


type_length = {'1E': 11, '21': 15, '22': 15, '24': 15}


def byte_decode(byte, start=0, stop=8):
    decimal = int(byte, 16)
    bits = bin(decimal)[2:].zfill(8)
    integer = int(bits[start: stop], 2)
    return integer


def control_field_number(cf):
    decimal_1 = int(cf[0], 16)
    bits_1 = bin(decimal_1)[2:].zfill(8)
    decimal_2 = int(cf[1], 16)
    bits_2 = bin(decimal_2)[2:].zfill(8)
    integer = int(bits_1 + bits_2[: -1], 2)
    return integer


class Iec104:
    def __init__(self, message):
        self.message = re.findall('[A-Z0-9]{2}', message)
        self.start = self.message[0]
        self.length = self.message[1]
        self.control_field = self.message[2: 6]

        if int(self.length, 16) > 4:
            self.type_identification = self.message[6]
            self.number_of_objects = self.message[7]
            self.COT = self.message[8]
            self.ORG = self.message[9]
            self.COA = self.message[11] + self.message[10]
            self.objects = [self.message[(12 + i * type_length[self.type_identification]):
                                         (13 + (i + 1) * type_length[self.type_identification])]
                            for i in range(int(self.number_of_objects, 16))]

    def report(self):
        if self.start != '68':
            return print('package must start with 68')
        elif int(self.length, 16) != (len(self.message) - 2):
            return print(f'mismatch length of APDU {int(self.length, 16)} != {(len(self.message) - 2)}')

        if byte_decode(self.control_field[0], 6) == 1:
            print('S format')
            print(f'Receive sequence {control_field_number(self.control_field[2:])}')
            return
        elif byte_decode(self.control_field[0], 6) == 3:
            print('U format')
            if self.control_field[0] == '43':
                print('Test Frame Activation')
            elif self.control_field[0] == '83':
                print('Test Frame Confirmation')
            elif self.control_field[0] == '13':
                print('Stop Data Transfer Activation')
            elif self.control_field[0] == '23':
                print('Stop Data Transfer Confirmation')
            elif self.control_field[0] == '07':
                print('Start Data Transfer Activation ')
            elif self.control_field[0] == '0B':
                print('Start Data Transfer Confirmation')
            print(f'Send sequence {control_field_number(self.control_field[:2])}')
            print(f'Receive sequence {control_field_number(self.control_field[2:])}')
            return
        print('I format')
        print(f'Send sequence {control_field_number(self.control_field[:2])}')
        print(f'Receive sequence {control_field_number(self.control_field[2:])}')
        if int(self.number_of_objects, 16) != len(self.objects):
            return print('mismatch Number of objects')
        print(f'Type identification {self.type_identification}')
        print(f'Number of objects {self.number_of_objects} ({int(self.number_of_objects, 16)})')
        print(f'COT {self.COT}')
        print(f'ORG {self.ORG}')
        print(f'COA {self.COA} ({int(self.COA, 16)})')
        for x in self.objects:
            print('\nInformation Element')
            print(x)
            report_object(self, x, self.type_identification)


def report_object(self, inf_element, data_type):
    if data_type == '1E':
        type_1e(inf_element)
    elif data_type == '21':
        type_21(inf_element)
    elif data_type == '22':
        type_22(inf_element)
    elif data_type == '23':
        type_23(inf_element)
    elif data_type == '24':
        type_24(inf_element)


def type_1e(inf_element):
    data = byte_decode(inf_element[3], 0)
    date = CP56Time2a(inf_element[4:11])


def type_21(inf_element):
    data = IEEE_STD_754(inf_element[3: 7])
    qb = QDS(inf_element[7])
    date = CP56Time2a(inf_element[8:15])


def type_22(inf_element):
    data = IEEE_STD_754(inf_element[3: 7])
    qb = QDS(inf_element[7])
    date = CP56Time2a(inf_element[8:15])


def type_23(inf_element):
    data = IEEE_STD_754(inf_element[3: 7])
    qb = QDS(inf_element[7])
    date = CP56Time2a(inf_element[8:15])


def type_24(inf_element):
    address = f'{inf_element[2]} {inf_element[1]} {inf_element[0]} ' \
              f'({int(inf_element[2] + inf_element[1] + inf_element[0], 16)})'
    data = IEEE_STD_754(inf_element[3: 7])
    qb = QDS(inf_element[7])
    date = CP56Time2a(inf_element[8:])
    if qb:
        print(address)
        print(data, qb, date)
    else:
        print(address)
        print(data, date)


def QDS(byte):
    decimal = int(byte, 16)
    bits = bin(decimal)[2:].zfill(8)
    result = ''
    if bool(int(bits[-1])):
        result += f'overflow quality: {bool(int(bits[-1]))} '
    if bool(int(bits[3])):
        result += f'blocked quality: {bool(int(bits[3]))} '
    if bool(int(bits[2])):
        result += f'substituted quality: {bool(int(bits[2]))} '
    if bool(int(bits[1])):
        result += f'topical quality: {bool(int(bits[1]))} '
    if bool(int(bits[0])):
        result += f'invalid quality: {bool(int(bits[0]))} '
    if result == '':
        return False
    else:
        return result


def IEEE_STD_754(array):
    return struct.unpack('<f', binascii.unhexlify(''.join(array)))[0]


def CP56Time2a(array):
    ms = int(array[1] + array[0], 16)
    microsecond = ms % 1000
    second = ms // 1000
    minute = byte_decode(array[2], 2)
    hour = byte_decode(array[3], 3)
    day = byte_decode(array[4], 3)
    month = byte_decode(array[5], 4)
    year = byte_decode(array[6], 1)
    dt = datetime(year + 2000, month, day, hour, minute, second, microsecond)
    return dt


def main():
    while True:
        telegram = Iec104(input('type package:\n'))
        telegram.report()



if __name__ == '__main__':
    main()
    # print(IEEE_STD_754(['6F', '12', '83', '3B']))
    # print(QDS('AE'))
