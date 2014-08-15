__author__ = 'dongdaqing'

import os

def parse_install_info():
    return_info = os.popen('adb shell am start -n com.youku.phone/com.youku.phone.ActivityWelcome').read()
    print return_info
    if return_info.find('Error type 3') != -1:
        print 'the app is not install'
    else:
        print 'the app is install'

if __name__ == '__main__':
    parse_install_info()