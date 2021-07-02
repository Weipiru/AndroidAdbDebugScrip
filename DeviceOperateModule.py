import os
import sys


def get_device(device_line):
    arr = device_line.split()
    # print(arr)
    dev_mod = DeviceObject()
    dev_mod.id = arr[0]
    dev_mod.status = arr[1]
    try:
        temp_arr = arr[4].split(':')
        dev_mod.device = temp_arr[1]
    except Exception as e:
        dev_mod.device = '无法获取'

    try:
        temp_arr = arr[2].split(':')
        dev_mod.product = temp_arr[1]
    except Exception:
        dev_mod.product = '未知'

    try:
        temp_arr = arr[3].split(':')
        dev_mod.model = temp_arr[1]
    except Exception:
        dev_mod.model = '未知'

    return dev_mod


def select_devices():
    cmd_exr = os.popen('adb devices -l')
    result = cmd_exr.read().rstrip()
    lines = result.splitlines()

    if len(lines) == 2:
        device = get_device(lines[1])
        print('\033[1;32muse device %s \033[0m' % device.id)
        return device.id
    else:
        dev_list = []
        dev_list.clear()
        for index, dev in enumerate(lines):
            if index == 0:
                continue
            dev = get_device(dev)
            print('\033[1;33m%d、%s %s - %s %s\033[0m' % (index - 1, dev.id, dev.model, dev.device, dev.status))
            dev_list.append(dev.id)
        sel = 0
        if len(dev_list) == 0:
            print('没有设备')
            input('按下 Enter 结束......')
            sys.exit(0)
        try:
            sel = int(input('存在多个设备，请输入序号[0]: '))
        except Exception as e:
            sel = 0
        if sel >= len(dev_list):
            sel = len(dev_list) - 1
        return dev_list[sel]


def go_adb_path():
    '''
    获取当前adb进程路径
    :return:
    '''
    print('\033[1;33m* 获取进程[adb.exe] 路径:\033[0m', end=' ')
    cmd_exr = os.popen('wmic process where name="adb.exe" get executablepath')
    lines = cmd_exr.read()
    line_arr = lines.splitlines()
    if len(line_arr) >= 3:
        path_str = line_arr[2].lstrip().rstrip()
        path_str = os.path.dirname(path_str)
        print('\033[1;33m%s\033[0m' % path_str)
        os.chdir(path_str)
    else:
        print('\033[1;33m没有检测到 adb 进程\033[0m')


class DeviceObject:
    def __init__(self):
        self.id = ''
        self.status = ''
        self.product = ''
        self.model = ''
        self.device = ''
        self.transport_id = ''

