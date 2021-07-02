import os
import win32con
import win32clipboard
import sys

import DeviceOperateModule

dev_list = []


class ActivityModel:
    def __init__(self):
        self.activity_name = ''
        self.full_act_name = ''
        self.app_id = ''

    def __str__(self):
        return self.full_act_name

#
# class DeviceObject:
#     def __init__(self):
#         self.id = ''
#         self.status = ''
#         self.product = ''
#         self.model = ''
#         self.device = ''
#         self.transport_id = ''
#


def copy(text):
    """复制"""
    win32clipboard.OpenClipboard()  # 打开剪贴板
    win32clipboard.EmptyClipboard()  # 清空剪贴板内容。可以忽略这步操作，但是最好加上清除粘贴板这一步
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)  # 以Unicode文本形式放入剪切板
    win32clipboard.CloseClipboard()  # 关闭剪贴板


# def select_devices():
#     cmd_exr = os.popen('adb devices -l')
#     result = cmd_exr.read().rstrip()
#     lines = result.splitlines()
#
#     if len(lines) == 2:
#         device = get_device(lines[1])
#         print('\033[1;32muse device %s \033[0m' % device.id)
#         return device.id
#     else:
#         global dev_list
#         dev_list.clear()
#         for index, dev in enumerate(lines):
#             if index == 0:
#                 continue
#             dev = get_device(dev)
#             print('\033[1;33m%d、%s %s - %s %s\033[0m' % (index - 1, dev.id, dev.model, dev.device, dev.status))
#             dev_list.append(dev.id)
#         sel = 0
#         if len(dev_list) == 0:
#             print('没有设备')
#             input('按下 Enter 结束......')
#             sys.exit(0)
#         try:
#             sel = int(input('存在多个设备，请输入序号[0]: '))
#         except Exception as e:
#             sel = 0
#         if sel >= len(dev_list):
#             sel = len(dev_list) - 1
#         return dev_list[sel]
#
#
# def get_device(device_line):
#     arr = device_line.split()
#     # print(arr)
#     dev_mod = DeviceObject()
#     dev_mod.id = arr[0]
#     dev_mod.status = arr[1]
#     try:
#         temp_arr = arr[4].split(':')
#         dev_mod.device = temp_arr[1]
#     except Exception as e:
#         dev_mod.device = '无法获取'
#
#     try:
#         temp_arr = arr[2].split(':')
#         dev_mod.product = temp_arr[1]
#     except Exception:
#         dev_mod.product = '未知'
#
#     try:
#         temp_arr = arr[3].split(':')
#         dev_mod.model = temp_arr[1]
#     except Exception:
#         dev_mod.model = '未知'
#
#     return dev_mod


def parse_line(line):
    arr = line.lstrip().rstrip().split(' ')
    for element in arr:
        if '/' in element:
            activity_model = ActivityModel()
            arr = element.split('/')
            activity_model.app_id = arr[0]
            activity_model.full_act_name = arr[1]
            arr = activity_model.full_act_name.split('.')
            activity_model.activity_name = arr[len(arr) - 1]
            return activity_model


if __name__ == '__main__':
    DeviceOperateModule.go_adb_path()
    dev_id = DeviceOperateModule.select_devices()
    cmd = 'adb -s {} shell dumpsys activity|findstr ResumedActivit'.format(dev_id)
    print(cmd)
    cmd_exr = os.popen(cmd, mode='r')
    result = cmd_exr.read()
    activities = []
    for line in result.splitlines():
        model = parse_line(line)
        if model is None:
            continue
        exist = False
        for e in activities:
            if e.full_act_name == model.full_act_name:
                exist = True
                break
        if exist is False:
            activities.append(model)

    if len(activities) == 1:
        temp_model = activities[0]
        print('copy: \033[1;34m%s\033[0m' % temp_model.activity_name)
        copy(temp_model.activity_name)
    elif len(activities) == 0:
        print('\033[1;31m没有找到任何Activity\033[0m')
        input('按下 Enter 退出')
        sys.exit(0)
    else:
        print('\033[1;33m发现多个Activity：\033[0m')
        print(len(activities))
        for index, element in enumerate(activities):
            print('%d、%s' % (index, element.full_act_name))
        ipt = int(input('输入目标索引:'))
        act = activities[ipt]
        print('你选择了 %s' % act)
        copy(act.activity_name)
        print('copy: \033[1;34m%s\033[0m' % act.activity_name)
