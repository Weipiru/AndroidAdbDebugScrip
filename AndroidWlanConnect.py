import os
import sys
import re
import time

import DeviceOperateModule

if __name__ == '__main__':
    DeviceOperateModule.go_adb_path()
    device_id = DeviceOperateModule.select_devices()
    time.sleep(2)
    cmd = 'adb -s {} tcpip 5555'.format(device_id)
    print(cmd)
    cmd_exr = os.popen(cmd)
    result = cmd_exr.read()
    # print(result)
    if result.lstrip().startswith('restarting in') and result.rstrip().endswith('5555'):
        print('\033[1;32m5555 端口已打开\033[0m')
        time.sleep(1)
        cmd = 'adb -s {} shell ifconfig wlan0'.format(device_id.strip())
        print(cmd)
        cmd_exr = os.popen(cmd)
        result = cmd_exr.read()
        for line in result.splitlines():
            if line.lstrip().startswith('inet addr'):
                pattern = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
                ip_str_obj = pattern.search(line)
                ip_str = ip_str_obj.group(0)
                print('连接IP:\033[1;33m %s\033[0m' % ip_str)
                cmd_exr = os.popen('adb connect {}'.format(ip_str))
                result = cmd_exr.read()
                if result.lstrip().startswith('connected') and result.rstrip().endswith('5555'):
                    input('连接成功')
                else:
                    input('连接失败：' + result)
                break
    else:
        print("端口打开失败: %s" % result)
