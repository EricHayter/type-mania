import curses

menu = ["Would you like to play again?", " YES ", " NO "]


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


def end_screen(stdscr):
    current_row_idx = 1

    print_menu(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key in [curses.KEY_UP, 450] and current_row_idx > 1:
            current_row_idx -= 1

        elif key in [curses.KEY_DOWN, 456] and current_row_idx < 2:
            current_row_idx += 1

        elif key in [curses.KEY_ENTER, 10, 13]:
            if current_row_idx == 1:
                return 1

            elif current_row_idx == 2:
                return 2

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()
    # stdscr.getkey()
