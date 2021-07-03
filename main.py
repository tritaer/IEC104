import re
import struct
import binascii
from datetime import datetime

from config import *
from asdu_type import *


def control_field_number(cf):
    decimal_1 = int(cf[0], 16)
    bits_1 = bin(decimal_1)[2:].zfill(8)
    decimal_2 = int(cf[1], 16)
    bits_2 = bin(decimal_2)[2:].zfill(8)
    integer = int(bits_1 + bits_2[: -1], 2)
    return integer


def print_result(data=None, address=None, qb=None, date=None):
    if address:
        print(f'IOA {address}')
    result = ''
    if data:
        result += f'value: {data}'
    if qb:
        result += f', quality bid: {qb}'
    if date:
        result += f', date: {date}'
    print(result)


class Iec104:
    def __init__(self, message):
        self.error = False
        message = re.findall('[A-Fa-f0-9]{2}', message)  # parse octets in list
        self.message = [i.upper() for i in message]
        if len(self.message) < 4:  # minimal length of telegram 4
            self.error = True
            print(f'message to short {len(self.message)} octets')
            return
        self.start = self.message[0]
        self.length = self.message[1]
        self.control_field = self.message[2: 6]
        if self.start != '68':  # 104 telegram start octet must equal 68
            self.error = True
            print('package must start with 68')
            return
        elif int(self.length, 16) != (len(self.message) - 2):  # second octet is length of telegram
            self.error = True
            print(f'mismatch length of APDU and telegram length {int(self.length, 16)} != {(len(self.message) - 2)}')
            return

        if int(self.length, 16) > 4:  # S-type and U-type have length 4. I-type always longer
            self.type_identification = self.message[6]
            self.asdu_type = ASDU_TYPE[self.type_identification]
            self.SQ = byte_to_dec(self.message[7], stop=1)
            self.number_of_objects = byte_to_dec(self.message[7], start=1)
            self.test = byte_to_dec(self.message[8], stop=1)
            self.pos_neg = byte_to_dec(self.message[8], start=1, stop=2)
            self.COT = byte_to_dec(self.message[8], start=2)
            self.ORG = self.message[9]
            self.COA = self.message[11] + self.message[10]
            type_length = sum([information_elements_length[i] for i in self.asdu_type['format']])  # length of inf objects base on elements in type
            if self.SQ:  # SQ mean only first inf object have address, next +1 from previous
                self.objects = [self.message[12: (12 + type_length + 3)]]  # first inf object with 3 octets address
                self.objects += [self.message[(12 + 3 + i * type_length): (12 + 3 + (i + 1) * type_length)]
                                 for i in range(1, self.number_of_objects)]  # all following without address
            else:
                type_length += 3  # plus 3 octets to inf object length for address
                self.objects = [self.message[(12 + i * type_length): (12 + (i + 1) * type_length)]
                                for i in range(self.number_of_objects)]

    def report_s_type(self):
        if BODY and not HEAD:
            print('U format not have ASDU')
            return
        print('S format')
        print(f'Receive sequence {control_field_number(self.control_field[2:])}')

    def report_u_type(self):
        if BODY and not HEAD:
            print('U format not have ASDU')
            return
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
            print('Start Data Transfer Activation')
        elif self.control_field[0] == '0B':
            print('Start Data Transfer Confirmation')
        print(f'Send sequence {control_field_number(self.control_field[:2])}')
        print(f'Receive sequence {control_field_number(self.control_field[2:])}')

    def report_i_type(self):
        print('I format')
        if HEAD or not (HEAD or BODY):
            print(f'Send sequence {control_field_number(self.control_field[:2])}')
            print(f'Receive sequence {control_field_number(self.control_field[2:])}')
            if self.number_of_objects != len(self.objects):
                return print('mismatch Number of objects')
            print(f'Type identification {self.type_identification}')
            print(f'SQ {self.SQ}')
            print(f'Number of objects {self.number_of_objects} ({self.number_of_objects})')
            try:
                print(f'COT {self.COT}, {cot_dict[self.COT]}')
            except IndexError as e:
                print(f'ERROR: unknown COT {self.COT}, {int(self.COT, 16)}')
            print(f'ORG {self.ORG}')
            print(f'COA {self.COA} ({int(self.COA, 16)})')
        if BODY or not (HEAD or BODY):
            for x in self.objects:
                print('\nInformation Element')
                print(x)
                print_result(**self.asdu_type['func'](x))
        print('\n')

    def report(self):
        if self.error:
            return
        if byte_to_dec(self.control_field[0], 6) == 1:  # if last to bits is 1 -> is S type telegram
            self.report_s_type()
        elif byte_to_dec(self.control_field[0], 6) == 3:  # elif last to bits is 3 -> is U type telegram
            self.report_u_type()
        else:  # else -> is I type telegram
            self.report_i_type()


def main():
    while True:
        telegram = Iec104(input('type package:\n'))
        telegram.report()


if __name__ == '__main__':
    main()
