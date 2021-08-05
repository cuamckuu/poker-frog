#!/usr/bin/env python

import ctypes
import re
import time

import win32gui
from PIL import ImageGrab

import pokerfrog as pf


def get_games_screenshoots(auto_popup=False):
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

        if auto_popup:
            win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.05)
        res[(hwnd, title)] = ImageGrab.grab(bbox)

    return res


if __name__ == '__main__':
    # TODO: Separate track last onew for each game
    last_hand, last_table = None, None

    while True:
        try:
            for ((hwnd, title), screen) in get_games_screenshoots().items():
                time.sleep(0.7)
                hand, table = pf.vision.get_hand_and_table(screen)

                if last_hand != hand or last_table != table:
                    last_hand, last_table = hand, table
                    print('\n'*50, flush=True)
                    print('State:', pf.metrics.get_game_state(table))
                    print('Hand:', hand)
                    print('Hand Score:', pf.metrics.get_hutchinson_score(hand))
                    print('Table:', table)
        except:
            pass
