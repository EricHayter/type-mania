import curses
from sys import stderr
from menus.menu import print_menu

curses.initscr()

stdscr = curses.initscr()


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


print(get_username(stdscr))