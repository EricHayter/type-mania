import curses
from curses import wrapper
import time
import random
import threading
import asyncio
import json

# multiplayer stuff
from server import handle_client
from client import send, setup

# screens for game
from game_menu import menu


home_menu = [" TYPE MANIA ", " Singleplayer ", " Multiplayer ", " Exit "]
end_menu = ["Would you like to play again?", " YES ", " NO "]
multiplayer_menu = [" Create game ", " Join game "]
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


async def wpm_test(stdscr, mode):
    if mode == "single":
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

        while True:
            time_elapsed = max(time.time() - start_time, 1)
            wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

            stdscr.clear()
            display_text(stdscr, target_text, current_text, wpm)
            stdscr.refresh()

            time.sleep(0.016)

            if "".join(current_text) == target_text:
                option = menu(stdscr, end_menu, True)
                if option == 1:
                    wpm_test(stdscr, "single")
                elif option == 2:
                    break

            try:

                key = stdscr.getkey() 
                
                if key == chr(27):
                     break

                if key in ("KEY_BACKSPACE", '\b', "\x7f"):
                    if len(current_text) > 0:
                        current_text.pop()
                elif len(current_text) < len(target_text):
                    current_text.append(key)
            except:
                pass

            time.sleep(0.016)


    else:
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

        while True:
            time_elapsed = max(time.time() - start_time, 1)
            wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

            stdscr.clear()
            display_text(stdscr, target_text, current_text, wpm)
            stdscr.refresh()

            time.sleep(0.016)

            if "".join(current_text) == target_text:
                option = menu(stdscr, end_menu, True)
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
        option = menu(stdscr, home_menu, True)
        if option == 1:
            asyncio.run(wpm_test(stdscr, "single"))

        if option == 2:
            host = menu(stdscr, multiplayer_menu, False)
            if host == 0:
                curses.endwin()
                threading.Thread(target=handle_client).start()
                setup()
                print(send("2 32"))
                print("This is a test")
                print(send("4 32"))

                time.sleep(10)


                wpm_test(stdscr, "multiplayer")

                # ends server
                print(scores)
                
            elif host == 1:
                scores.append(send("10"))

        elif option == 3:
            break


wrapper(main)
