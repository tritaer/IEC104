from information_elements import *


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


def type_in_development(inf_element):
    print('type under development')


def type_1(inf_element):
    if len(inf_element) == 4:
        address = get_ioa(inf_element)
    else:
        address = None
    data = SIQ(inf_element[-1])
    print_result(data, address)


def type_2(inf_element):
    if len(inf_element) == 7:
        address = get_ioa(inf_element)
    else:
        address = None
    data = SIQ(inf_element[-4])
    date = CP24Time2a(inf_element[-3:])
    print_result(data, address, date=date)


def type_3(inf_element):
    if len(inf_element) == 4:
        address = get_ioa(inf_element)
    else:
        address = None
    data = DIQ(inf_element[-1])
    print_result(data, address)


def type_4(inf_element):
    if len(inf_element) == 7:
        address = get_ioa(inf_element)
    else:
        address = None
    data = DIQ(inf_element[-4])
    date = CP24Time2a(inf_element[-3:])
    print_result(data, address, date=date)


def type_5(inf_element):
    if len(inf_element) == 5:
        address = get_ioa(inf_element)
    else:
        address = None
    data = VTI(inf_element[-2])
    qb = QDS(inf_element[-1])
    print_result(data, address, qb)


def type_6(inf_element):
    if len(inf_element) == 8:
        address = get_ioa(inf_element)
    else:
        address = None
    data = VTI(inf_element[-5])
    qb = QDS(inf_element[-4])
    date = CP24Time2a(inf_element[-3:])
    print_result(data, address, qb, date)


def type_7(inf_element):
    if len(inf_element) == 8:
        address = get_ioa(inf_element)
    else:
        address = None
    data = BSI(inf_element[-5:-1])
    qb = QDS(inf_element[-1])
    print_result(data, address, qb)


def type_8(inf_element):
    if len(inf_element) == 11:
        address = get_ioa(inf_element)
    else:
        address = None
    data = BSI(inf_element[-8:-4])
    qb = QDS(inf_element[-4])
    date = CP24Time2a(inf_element[-3:])
    print_result(data, address, qb, date)


def type_9(inf_element):
    if len(inf_element) == 6:
        address = get_ioa(inf_element)
    else:
        address = None
    data = NVA(inf_element[-3: -1])
    qb = QDS(inf_element[-1])
    print_result(data, address, qb)


def type_a(inf_element):
    if len(inf_element) == 9:
        address = get_ioa(inf_element)
    else:
        address = None
    data = NVA(inf_element[3])
    qb = QDS(inf_element[-4])
    date = CP24Time2a(inf_element[-3:])
    print_result(data, address, qb, date)


def type_b(inf_element):
    if len(inf_element) == 6:
        address = get_ioa(inf_element)
    else:
        address = None
    data = SVA(inf_element[-3:-1])
    qb = QDS(inf_element[-1])
    print_result(data, address, qb)


def type_c(inf_element):
    if len(inf_element) == 9:
        address = get_ioa(inf_element)
    else:
        address = None
    data = SVA(inf_element[-6:-4])
    qb = QDS(inf_element[-4])
    date = CP24Time2a(inf_element[-3:])
    print_result(data, address, qb, date)


def type_d(inf_element):
    if len(inf_element) == 8:
        address = get_ioa(inf_element)
    else:
        address = None
    data = IEEE_STD_754(inf_element[-5: -1])
    qb = QDS(inf_element[-1])
    print_result(data, address, qb)


def type_e(inf_element):
    if len(inf_element) == 11:
        address = get_ioa(inf_element)
    else:
        address = None
    data = IEEE_STD_754(inf_element[-8: -4])
    qb = QDS(inf_element[-4])
    date = CP24Time2a(inf_element[-3:])
    print_result(data, address, qb, date)


def type_15(inf_element):
    if len(inf_element) == 15:
        address = get_ioa(inf_element)
    else:
        address = None
    data = NVA(inf_element[-2:])
    print_result(data, address)


# long time tag
def type_1e(inf_element):
    if len(inf_element) == 11:
        address = get_ioa(inf_element)
    else:
        address = None
    data = SIQ(inf_element[-8])
    date = CP56Time2a(inf_element[-7:])
    print_result(data, address, date=date)


def type_1f(inf_element):
    if len(inf_element) == 11:
        address = get_ioa(inf_element)
    else:
        address = None
    data = DIQ(inf_element[-8])
    date = CP56Time2a(inf_element[-7:])
    print_result(data, address, date=date)


def type_20(inf_element):
    if len(inf_element) == 12:
        address = get_ioa(inf_element)
    else:
        address = None
    data = VTI(inf_element[-9])
    qb = QDS(inf_element[-8])
    date = CP56Time2a(inf_element[-7:])
    print_result(data, address, qb, date)


def type_21(inf_element):
    if len(inf_element) == 15:
        address = get_ioa(inf_element)
    else:
        address = None
    data = BSI(inf_element[-12: -8])
    qb = QDS(inf_element[-8])
    date = CP56Time2a(inf_element[-7:])
    print_result(data, address, qb, date)


def type_22(inf_element):
    if len(inf_element) == 13:
        address = get_ioa(inf_element)
    else:
        address = None
    data = NVA(inf_element[-10: -8])
    qb = QDS(inf_element[-8])
    date = CP56Time2a(inf_element[-7:])
    print_result(data, address, qb, date)


def type_23(inf_element):
    if len(inf_element) == 13:
        address = get_ioa(inf_element)
    else:
        address = None
    data = SVA(inf_element[-10: -8])
    qb = QDS(inf_element[-8])
    date = CP56Time2a(inf_element[-7:])
    print_result(data, address, qb, date)


def type_24(inf_element):
    if len(inf_element) == 15:
        address = get_ioa(inf_element)
    else:
        address = None
    data = IEEE_STD_754(inf_element[-12: -8])
    qb = QDS(inf_element[-8])
    date = CP56Time2a(inf_element[-7:])
    print_result(data, address, qb, date)


def type_26(inf_element):
    if len(inf_element) == 12:
        address = get_ioa(inf_element)
    else:
        address = None
    date1 = CP16Time2a(inf_element[-5:-7])
    date2 = CP56Time2a(inf_element[-7:])
    date = f'CP16: {date1}, CP56: {date2}'
    print_result(address=address, date=date)


def type_64(inf_elem):
    data = QOI(inf_elem[-1])
    print_result(data)
