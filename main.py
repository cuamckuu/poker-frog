#!/usr/bin/env python

import ctypes
import re
import time

import win32gui
from PIL import ImageGrab

import pokerfrog as pf


def get_games_screenshoots():
    """Return dict with Pillow images for every opened window with game."""
    winlist = []
    def enum_cb(hwnd, results):
        title = win32gui.GetWindowText(hwnd)

        if re.findall('Без лимита Холдем', title):
            winlist.append((hwnd, title))

    win32gui.EnumWindows(enum_cb, [])

    res = {}
    for (hwnd, title) in winlist:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9

        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            ctypes.wintypes.HWND(hwnd),
            ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
            ctypes.byref(rect),
            ctypes.sizeof(rect),
        )
        bbox = (rect.left, rect.top, rect.right, rect.bottom)

        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.05)
        res[(hwnd, title)] = ImageGrab.grab(bbox)

    return res


if __name__ == '__main__':
    last_hand, last_table = None, None
    while True:
        try:
            for ((hwnd, title), screen) in get_games_screenshoots().items():
                time.sleep(0.6)
                hand, table = pf.vision.get_hand_and_table(screen)

                if last_hand != hand or last_table != table:
                    last_hand, last_table = hand, table
                    print("Hand:", hand)
                    print("Table:", table)
                    print()
        except:
            pass
