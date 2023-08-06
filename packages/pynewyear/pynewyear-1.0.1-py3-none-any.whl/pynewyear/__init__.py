import os
import platform
import random
import shutil
import time
from dataclasses import dataclass
from threading import Thread

__version__ = '1.0.1'

TREE_HIGH = 12
TERMINAL_WIDTH = shutil.get_terminal_size().columns


@dataclass
class Colors:
    red: str = '\x1b[1;31;40m'
    green: str = '\x1b[1;32;40m'
    yellow: str = '\x1b[1;33;40m'
    blue: str = '\x1b[1;34;40m'
    magenta: str = '\x1b[1;35;40m'
    cyan: str = '\x1b[1;36;40m'
    full_yellow: str = '\x1b[1;33;43m'
    end: str = '\x1b[0m'


class PrintTreeThread(Thread):

    def clear(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def colorize(self, text, color):
        return color + text + Colors.end

    def print_center(self, text, visible_len=None):
        if visible_len is None:
            visible_len = len(text)
        print(' ' * ((TERMINAL_WIDTH - visible_len) // 2) + text)

    def get_row(self, row_len):
        if row_len == 1:
            return '*'
        # possible positions for "o"
        positions = range(1, row_len - 1)
        # how many possible "o"
        quantity = random.randint(0, row_len // 4 + 1)
        # get "o" positions
        positions = random.sample(positions, quantity)
        row = ['o' if i in positions else '*' for i in range(row_len)]
        return ''.join(row)

    def colorize_row(self, row):
        result = []
        for x in row:
            if x == '*':
                result.append(self.colorize(x, Colors.green))
            else:
                color = random.choice([
                    Colors.red,
                    Colors.yellow,
                    Colors.blue,
                    Colors.magenta,
                    Colors.cyan
                ])
                result.append(self.colorize(x, color))
        return ''.join(result)

    def run(self):
        high_x2 = TREE_HIGH * 2
        self.__is_run = True

        while self.__is_run:
            self.clear()
            # draw crown
            for x in range(1, high_x2, 2):
                row = self.get_row(x)
                color_row = self.colorize_row(row)
                self.print_center(color_row, x)

            # draw trunk
            for _ in range(2):
                trunk_text = self.colorize('mWm', Colors.full_yellow)
                self.print_center(trunk_text, 3)

            print()

            # text
            self.print_center(self.colorize('🎅 🎄', Colors.red), 6)
            ny_text = self.colorize('Happy New Year!', Colors.red)
            self.print_center(ny_text, 15)

            print()
            self.print_center('Press Enter...')
            time.sleep(1)

    def stop(self):
        self.__is_run = False


def main():
    t = PrintTreeThread(daemon=True)
    t.start()
    input()
    t.stop()
