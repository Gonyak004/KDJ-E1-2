"""외부 패키지 없이 출력하는 콘솔 카드와 진행 막대."""

import os
import sys
import unicodedata

WIDTH = 62


def enable_color():
    if not sys.stdout.isatty() or "NO_COLOR" in os.environ:
        return False
    if os.name == "nt":
        import ctypes
        kernel = ctypes.windll.kernel32
        handle = kernel.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if not kernel.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel.SetConsoleMode(handle, mode.value | 4))
    return True


def text_width(text):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def wrapped(text, width=WIDTH - 4):
    line = ""
    for character in str(text).expandtabs(4):
        if character == "\n" or text_width(line + character) > width:
            yield line
            line = "" if character == "\n" else character
        else:
            line += character
    yield line


class Console:
    def __init__(self):
        self.color = enable_color()

    def tint(self, text, code="96"):
        return f"\033[{code}m{text}\033[0m" if self.color else text

    def card(self, title, lines, accent="96"):
        print()
        print(self.tint("+" + "-" * WIDTH + "+", accent))
        for text in [title, "-" * (WIDTH - 4), *lines]:
            for line in wrapped(text):
                padding = " " * (WIDTH - 4 - text_width(line))
                print(self.tint("|", accent) + f"  {line}{padding}  " + self.tint("|", accent))
        print(self.tint("+" + "-" * WIDTH + "+", accent))

    def progress(self, current, total):
        filled = current * 20 // total
        return "[" + "#" * filled + "." * (20 - filled) + f"] {current}/{total}"
