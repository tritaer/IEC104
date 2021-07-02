import struct
import binascii
from datetime import datetime

qoi_dict = {0: 'not used',
            **dict.fromkeys([i for i in range(1, 20)], 'reserved for standard definitions of this companion standard'),
            20: 'global station interrogation',
            **dict.fromkeys([i for i in range(37, 64)], 'reserved for future norm definitions of this companion standard (compatible range)'),
            **dict.fromkeys([i for i in range(64, 256)], 'reserved for user definitions (private range)'),
            **{i: f'group {i - 20} station interrogation' for i in range(21, 37)}}


def byte_to_dec(byte, start=0, stop=8):
    bits = byte_to_bit(byte)
    integer = int(bits[start: stop], 2)
    return integer


def byte_to_bit(byte):
    decimal = int(byte, 16)
    return bin(decimal)[2:].zfill(8)


def get_ioa(inf_element):
    return f'{inf_element[2]} {inf_element[1]} {inf_element[0]} ' \
           f'({int(inf_element[2] + inf_element[1] + inf_element[0], 16)})'


def quality_bits(bits):
    result = ''
    if bool(int(bits[3])):
        result += f'blocked quality: {bool(int(bits[3]))} '
    if bool(int(bits[2])):
        result += f'substituted quality: {bool(int(bits[2]))} '
    if bool(int(bits[1])):
        result += f'topical quality: {bool(int(bits[1]))} '
    if bool(int(bits[0])):
        result += f'invalid quality: {bool(int(bits[0]))} '
    return result


def SIQ(byte):
    bits = byte_to_bit(byte)
    if int(bits[-1]) == 0:
        result = 'OFF '
    else:
        result = 'ON '
    result += quality_bits(bits)
    return result


def DIQ(byte):
    bits = byte_to_bit(byte)
    DPI = int(bits[6:], 2)
    if DPI == 0:
        result = 'indeterminate or intermediate state '
    elif DPI == 1:
        result = 'OFF '
    elif DPI == 2:
        result = 'ON '
    else:
        result = 'indeterminate '
    result += quality_bits(bits)
    return result


def VTI(byte):
    state = byte_to_dec(byte, stop=1)
    if state == 0:
        state_desc = 'equipment is not in transient state '
    else:
        state_desc = 'equipment is in transient state '
    data = byte_to_dec(byte, start=1) - 64
    print(f'state: {state_desc}, data: {data}')


def BSI(array):
    return int(''.join(array[::-1]), 16)


def NVA(array):
    return int(array[-1] + array[0], 16)


def SVA(array):
    return int(array[-1] + array[0], 16) - 32768


def IEEE_STD_754(array):
    return struct.unpack('<f', binascii.unhexlify(''.join(array)))[0]


def QDS(byte):
    bits = byte_to_bit(byte)
    result = ''
    if bool(int(bits[-1])):
        result += f'overflow quality: {bool(int(bits[-1]))} '
    result += quality_bits(bits)
    return result


def QOI(byte):
    int_ = byte_to_dec(byte)
    result = f'{int_} {qoi_dict[int_]}'
    return result


def CP16Time2a(array):
    ms = int(array[1] + array[0], 16)
    microsecond = ms % 1000 * 1000
    second = ms // 1000
    dt = datetime(second=second, microsecond=microsecond)
    return dt


def CP24Time2a(array):
    ms = int(array[1] + array[0], 16)
    microsecond = ms % 1000 * 1000
    second = ms // 1000
    minute = byte_to_dec(array[2], 2)
    dt = datetime(minute=minute, second=second, microsecond=microsecond)
    return dt


def CP56Time2a(array):
    ms = int(array[1] + array[0], 16)
    microsecond = ms % 1000 * 1000
    second = ms // 1000
    minute = byte_to_dec(array[2], 2)
    hour = byte_to_dec(array[3], 3)
    day = byte_to_dec(array[4], 3)
    month = byte_to_dec(array[5], 4)
    year = byte_to_dec(array[6], 1)
    dt = datetime(year + 2000, month, day, hour, minute, second, microsecond)
    return dt


progres = {'SIQ': '+', 'DIQ': '+', 'BSI': '+', 'SCD': '-', 'QDS': '+', 'VTI': '1',
           'NVA': '+', 'SVA': '+', 'IEEE_STD_754': '+', 'BCR': '5', }


def SCD(array):
    print('not ready yet')





def BCR(array):
    print('not ready yet')

