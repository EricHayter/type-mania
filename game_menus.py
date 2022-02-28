import curses
from sys import stderr
from menu_functions import *


def get_port_number(stdscr):
    user_input = ''

    print_menu(stdscr, ['Enter Port Number:'], None)

    stdscr.nodelay(False)

    while 1:
        try:
            key = stdscr.getch()

            stdscr.clear()

            if key == 27:
                return

            # IF THE USER PRESSES ENTER
            if key in [curses.KEY_ENTER, 10, 13]:
                if int(user_input) in range(1024, 9999):
                    stdscr.nodelay(True)
                    return int(user_input)

            # LETTER INPUT
            elif key in range(48, 58):
                if len(user_input) < 4:
                    user_input += chr(key)

            elif key in ["KEY_BACKSPACE", '\b', "\x7f", 8]:
                user_input = user_input[:-1]

        except:
            pass

        print_menu(stdscr, ["Enter Port Number:", user_input], None)
        stdscr.refresh()


def get_username(stdscr):
    user_input = ''

    print_menu(stdscr, ['Enter Name:'], None)

    stdscr.nodelay(False)

    while 1:
        try:
            key = stdscr.getch()

            stdscr.clear()

            if key == 27:
                return

            # IF THE USER PRESSES ENTER
            if key in [curses.KEY_ENTER, 10, 13]:
                if len(user_input) > 0:
                    stdscr.nodelay(True)
                    return user_input

            # LETTER INPUT
            elif key in range(97, 123) or key in range(65, 90):
                if len(user_input) < 4:
                    user_input += chr(key)

            elif key in ["KEY_BACKSPACE", '\b', "\x7f", 8]:
                user_input = user_input[:-1]

        except:
            pass

        print_menu(stdscr, ["Enter Name:", user_input], None)
        stdscr.refresh()


def home_screen(stdscr):
    home_menu = [" TYPE MANIA ", " Singleplayer ", " Multiplayer ", " Exit "]
    return menu(stdscr, home_menu, True)


def end_screen(stdscr):
    end_menu = ["Would you like to play again?", " YES ", " NO "]
    return menu(stdscr, end_menu, True)


def multiplayer_screen(stdscr):
    multiplayer_menu = [" Create game ", " Join game "]
    return menu(stdscr, multiplayer_menu, False)