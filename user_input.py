import curses
from sys import stderr
from menu import print_menu

curses.initscr()
menu = 'Enter Name:'

stdscr = curses.initscr()


def input_menu(stdscr, title):
    user_input = ''

    print_menu(stdscr, [title], None)

    stdscr.nodelay(False)

    while 1:
        try:
            key = stdscr.getch()

            stdscr.clear()

            if key in [curses.KEY_ENTER, 10, 13]:
                if len(user_input) > 0:
                    stdscr.nodelay(True)
                    return user_input

            elif key in range(97, 123) or key in range(65, 90):
                if len(user_input) < 4:
                    user_input += chr(key)

            elif key in ["KEY_BACKSPACE", '\b', "\x7f", 8]:
                user_input = user_input[:-1]

        except:
            pass

        print_menu(stdscr, [title, user_input], None)
        stdscr.refresh()


print(input_menu(stdscr, menu))