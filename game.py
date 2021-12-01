import curses
from curses import wrapper
import time
import random
import threading
import json

# multiplayer stuff
from server import start
from client import send, setup

# screens for game
from home_screen import start_screen
from game_menu import end_screen


menu = [" TYPE MANIA ", " Singleplayer ", " Multiplayer ", " Exit "]
scores = {}


def percentComplete(typed, actual):
    shared = 0
    try:
        for idx, character in enumerate(actual):
            if typed[idx] == character:
                shared += 1
        return int(shared/len(actual)*100)
    except:
        return 0


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def load_text(line=False):
    with open("text.txt", "r") as f:
        lines = f.readlines()
        if line:
            return (lines[line].strip(), line)

        line = random.randint(0, len(lines))

        return (lines[line].strip(), line)


def wpm_test(stdscr):
    h, w = stdscr.getmaxyx()
    x = w//2
    y = h//2 - 1

    target_text = load_text()[0]
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

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            option = end_screen(stdscr)
            if option == 1:
                wpm_test(stdscr)
            elif option == 2:
                break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
            scores.update(json.loads(
                send(f"0 {percentComplete(current_text, target_text)}")))


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True:
        option = start_screen(stdscr)
        if option == 1:
            wpm_test(stdscr)

        if option == 2:
            curses.endwin()

            host = int(input())
            if host == 1:
                thread = threading.Thread(target=start)
                thread.start()
                setup()

                wpm_test(stdscr)

                # ends server
                print(scores)
                send("!DISCONNECT")

            elif host == 0:
                scores.append(send("10"))

        elif option == 3:
            break


wrapper(main)
