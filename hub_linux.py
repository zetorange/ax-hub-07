import subprocess
from subprocess import PIPE, Popen
import pyautogui
import random
import time
import string
import re


# BASE_WINDOWS = ['gedit', 'Google Chrome', 'Sublime']
# BASE_WINDOWS = ['gedit', 'Google Chrome', 'Google Chrome']
BASE_WINDOWS = ['gedit', 'Sublime', 'Sublime']
# BASE_WINDOWS = ['gedit', 'Visual Studio', 'Visual Studio']
# BASE_WINDOWS = ['gedit', ' IDA ', ' IDA ']
BROWSER_DURATION_START = 50
BROWSER_DURATION_END = 70
BROWSER_MOUSE_INIT_X = 100
BROWSER_MOUSE_INIT_Y = 100


def get_active_window():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+),.*$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        return match.group("name").strip('"')

    return None


def act_mouse():
    time.sleep(1)
    def action(choice_window):
        global BROWSER_MOUSE_INIT_X
        global BROWSER_MOUSE_INIT_Y
        size = pyautogui.size()
        size_x = size[0]
        size_y = size[1]
        idx = random.randint(0, 20)
        rnd_x = random.randint(100, size_x-100)
        rnd_y = random.randint(100, size_y-100)
        rnd_scroll = random.randint(-5, 5)
        if idx < 3:
            pyautogui.moveTo(rnd_x, rnd_y, duration=1)
        elif idx < 4:
            pyautogui.moveTo(BROWSER_MOUSE_INIT_X, BROWSER_MOUSE_INIT_Y, duration=0.1)
            pyautogui.scroll(rnd_scroll)
            time.sleep(1)
        elif idx < 5:
            pyautogui.moveTo(BROWSER_MOUSE_INIT_X, BROWSER_MOUSE_INIT_Y, duration=0.1)
            pyautogui.click()
            time.sleep(1)
        elif idx < 6:
            if BASE_WINDOWS[choice_window] != ' IDA ':
                pyautogui.keyDown('ctrlleft')
                tab_len = random.randint(0, 10)
                for _ in range(tab_len):
                    pyautogui.keyDown('tab')
                    pyautogui.keyUp('tab')
                pyautogui.keyUp('ctrlleft')
            time.sleep(1)
        else:
            time.sleep(1)
        
    choice_window = random.randint(1, len(BASE_WINDOWS)-1)
    subprocess.call(['wmctrl', '-a', BASE_WINDOWS[choice_window]])

    period = random.randint(BROWSER_DURATION_START, BROWSER_DURATION_END)
    sec = 0
    while(sec < period):
        action(choice_window)
        sec += 1

def act_keyboard():
    time.sleep(1)
    subprocess.call(['wmctrl', '-a', 'gedit'])
    N = random.randint(8, 12)
    random_str = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))
    speed = float(random.randint(12,17))/10
    for s in random_str:
        try:
            if 'gedit' not in get_active_window():
                return
        except:
            return
        pyautogui.typewrite(s)
        time.sleep(speed)

def main():
    windows = subprocess.check_output(['wmctrl', '-l']).decode().split('\n')
    for base_win in BASE_WINDOWS:
        opened_win = [win for win in windows if base_win in win]
        if not opened_win:
            print('You need to open %s!' % base_win)
            return

    global BROWSER_MOUSE_INIT_X
    global BROWSER_MOUSE_INIT_Y
    BROWSER_MOUSE_INIT_X, BROWSER_MOUSE_INIT_Y = pyautogui.position()

    time.sleep(3)

    subprocess.call('wmctrl -a gedit'.split(' '))
#    gedit_id = subprocess.check_output('xdotool getwindowfocus'.split(' ')).strip('\n')
#    gedit_hide_command = ('xdotool windowmove %s -5000 -5000' % gedit_id).split(' ')
#    subprocess.call(gedit_hide_command)
    subprocess.call('wmctrl -r gedit -b add,below'.split(' '))
    
    while (1):
        act_keyboard()
        act_mouse()
        time.sleep(random.randint(60, 180))

main()
