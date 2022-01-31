import curses
from curses import wrapper
import random
import socket
import threading
import time

from scoring import calculateScore

# importing server
from server_utilities import server, client

# screens for game
from menus.menu import menu

home_menu = [" TYPE MANIA ", " Singleplayer ", " Multiplayer ", " Exit "]
end_menu = ["Would you like to play again?", " YES ", " NO "]
multiplayer_menu = [" Create game ", " Join game "]


class Scores:
    scores = {"you": 0}

    def getScores(self):
        return self.scores

    def setScores(self, newScores):
        self.scores.update(newScores)


scores = Scores()


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

        line = random.randint(0, len(lines) - 1)

        return (lines[line].strip(), line)


def wpm_test(stdscr, multiplayer=False):
    h, w = stdscr.getmaxyx()
    x = w // 2
    y = h // 2 - 1

    target_text = load_text()[0]
    current_text = []
    wpm = 0

    if multiplayer:
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.connect(('127.0.0.1', 4321))

        run_client = threading.Thread(target=client,
                                      args=(scores.getScores, scores.setScores,
                                            lsock))
        run_client.start()

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
        scores.setScores({"you": calculateScore(current_text, target_text)})

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


def main(stdscr):
    # initiallizing the color sets
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True:
        game_mode = menu(stdscr, home_menu, True)
        if game_mode == 1:
            wpm_test(stdscr)

        elif game_mode == 2:
            hosting = menu(stdscr, multiplayer_menu, False)
            print(f"hosting: {hosting}")
            if hosting == 0:
                threading.Thread(target=server).start()

                wpm_test(stdscr)

            elif hosting == 1:
                wpm_test(stdscr, True)

        else:
            break


wrapper(main)
