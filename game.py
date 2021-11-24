import curses
import cProfile
from curses import wrapper
import time
import random

menu = [" TYPE MANIA ", " Singleplayer ", " Multiplayer ", " Exit "]


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu) + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(4))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def start_screen(stdscr):
    current_row_idx = 1

    print_menu(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key in [curses.KEY_UP, 450] and current_row_idx > 1:
            current_row_idx -= 1

        elif key in [curses.KEY_DOWN, 456] and current_row_idx < 3:
            current_row_idx += 1

        elif key in [curses.KEY_ENTER, 10, 13]:
            if current_row_idx == 3:
                exit()

            elif current_row_idx == 1:
                wpm_test(stdscr)

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()
    # stdscr.getkey()


def display_text(stdscr, target, current):
    stdscr.addstr(target)
    
    #for i, char in enumerate(current):
    #    correct_char = target[i]
    #    color = curses.color_pair(1)
    #    if char != correct_char:
    #        color = curses.color_pair(2)
    #
    #    stdscr.addstr(0, i, char, color)

    stdscr.addstr(0,0, "".join(current))

def display_wpm(stdscr, wpm=0):
    stdscr.addstr(1, 0, f"WPM: {wpm}")

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    h, w = stdscr.getmaxyx()
    x = w//2
    y = h//2 - 1

    target_text = load_text()
    current_text = []
    wpm = 0

    # countdown feature
    for i in range(3, 0, -1):
        stdscr.clear()
        stdscr.addstr(y, x, str(i))
        stdscr.refresh()
        time.sleep(1)

    start_time = time.time()
    stdscr.nodelay(True)

    display_text(stdscr, target_text, current_text)


    while True:
        #time_elapsed = max(time.time() - start_time, 1)
        wpm = 72 #round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text)
        display_wpm(stdscr, wpm)
        stdscr.refresh()

        if current_text == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
            display_text(stdscr, target_text, current_text)
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)



def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(
            2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
