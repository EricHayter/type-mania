import curses
from curses import wrapper
import random
import socket
import threading
import time

from scoring import calculateScore

# importing server
from client import Client
from server import Server

# screens for game
from game_menus import *


class Player:
    START_MESSAGE = "!START"

    def __init__(self, name):
        self.scores = {name: 0}
        self.gameRunning = False

    def getScores(self):
        return self.scores

    def setScores(self, newScores):
        self.scores.update(newScores)

    def startGame(self):
        self.gameRunning = True

    def isGameRunning(self):
        return self.gameRunning


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
        # scores.setScores({NAME: calculateScore(current_text, target_text)})

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        time.sleep(0.016)

        if "".join(current_text) == target_text:
            option = end_screen(stdscr)
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
        game_mode = home_screen(stdscr)
        if game_mode == 1:
            wpm_test(stdscr)

        elif game_mode == 2:

            hosting = multiplayer_screen(stdscr)

            PORT = get_port_number(stdscr)
            NAME = get_username(stdscr)
            scores = Player(NAME)

            # if the user is hosting the game
            if hosting:
                # starting up server
                s = Server()
                s.bind()
                threading.Thread(target=s.start).start()

                # creating a client for the host
                client = Client(PORT, scores.getScores, scores.setScores)
                client.connect()

                # TODO loading screen for the host
                setupThread = threading.Thread(target=client.setup)
                setupThread.start()

                # TODO add title to the top of the loading screen that says "PLAYERS"
                waiting = True
                while waiting:
                    stdscr.clear()
                    info_screen(
                        stdscr, ["PLAYERS", *scores.getScores().keys()])
                    stdscr.refresh()

                    # waiting for the host to start the game
                    startGame = stdscr.getch()
                    if startGame == ord("\n"):
                        stdscr.nodelay(True)
                        s.startGame()

                    # setting the FPS
                    time.sleep(0.016)

                    if not setupThread.is_alive():
                        waiting = False
                # TODO try to merge together this if else statement (too much repeating code)

            # if they are joining the game
            else:

                # starting up client
                client = Client(PORT, scores.getScores, scores.setScores)
                client.connect()

                # loading screen
                setupThread = threading.Thread(target=client.setup)
                setupThread.start()

                # TODO add title to the top of the loading screen that says "PLAYERS"
                waiting = True
                while waiting:
                    stdscr.clear()
                    info_screen(
                        stdscr, ["PLAYERS", *scores.getScores().keys()])
                    stdscr.refresh()
                    time.sleep(0.016)

                    if not setupThread.is_alive():
                        waiting = False

            # starting up the game when the client is ready
            wpm_test(stdscr, True)

        else:
            break


wrapper(main)
