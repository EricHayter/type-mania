import curses


def print_menu(stdscr, menu, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(4))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def menu(stdscr, menu, title):
    first = 0
    if title:
        first = 1

    current_row_idx = first

    print_menu(stdscr, menu, current_row_idx)

    stdscr.nodelay(False)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key in [curses.KEY_UP, 450] and current_row_idx > first:
            current_row_idx -= 1

        elif key in [curses.KEY_DOWN, 456] and current_row_idx < len(menu):
            current_row_idx += 1

        elif key in [curses.KEY_ENTER, 10, 13]:
            stdscr.nodelay(True)
            return current_row_idx

        print_menu(stdscr, menu, current_row_idx)
        stdscr.refresh()


def info_screen(stdscr, text):
    print_menu(stdscr, text)
