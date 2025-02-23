import builtins
import math
import os
import sys
import time
import threading
import shutil

if os.name == 'nt':
    import msvcrt
    import ctypes


    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]


class Cursor:
    # This code of cursor object is made by James Spencer, big thanks!
    def __init__(self):
        self.ci = _CursorInfo()
        self.on = os.name

    def hide(self):
        if self.on == 'nt':
            self._cur(False)
        elif self.on == 'posix':
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    def show(self):
        if self.on == 'nt':
            self._cur(True)
        elif self.on == 'posix':
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

    def _cur(vis):
        self.ci = _CursorInfo()
        handle = windll.kernel32.GetStdHandle(-11)
        windll.kernel32.GetConsoleCursorInfo(handle, byref(self.ci))
        self.ci.visible = vis
        windll.kernel32.SetConsoleCursorInfo(handle, byref(self.ci))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def set_title(title):
    os.system("title " + title)


def set_size_of_console(width=None, height=None):
    term_size = os.get_terminal_size()

    if width is None:
        width = term_size.columns
    if height is None:
        height = term_size.lines

    os.system(f'mode con: cols={width} lines={height}')


def split(symbol="█"):
    term_size = shutil.get_terminal_size()
    builtins.print(symbol * term_size.columns)

class AnimatedTitle:
    def __init__(self, text, timing = 0.1):
        self.text = text
        self.enabled = False
        self.timing = timing
    def move(self):
        while self.enabled:
            set_title(self.text)
            self.text = self.text[-1]+self.text[:-1]
            time.sleep(self.timing)
    def start(self):
        self.enabled = True
        threading.Thread(target = self.move, daemon = True).start()
    def stop(self):
        self.enabled = False

def colorize_fade(text, fade, ncolorate=False):

    os.system(""); faded = ""
    if not ncolorate:
        fade = fade.generate(len(text))
        for i in range(len(text)):
            ob = fade[i].rgb()
            faded += (f"\033[38;2;{ob[0]};{ob[1]};{ob[2]}m{text[i]}\033[0m")
    else:
        for i in text.split('\n'):
            faded += colorize_fade(i, fade)+'\n'
        if text[-1] == '\n':
            faded = faded[:-1]
    return faded


def colorize_onecolor(text, color):
    ob = color.rgb()
    return (f"\033[38;2;{ob[0]};{ob[1]};{ob[2]}m{text}\033[0m")

def centralize(text, text_length = None):
    if text_length is None:
        text_length = len(text)
    term_size = shutil.get_terminal_size()

    width = term_size.columns

    return (math.ceil((width-text_length)/2)*" ")+text