import curses

stdscr = curses.initscr()
stdscr.keypad(0)
curses.noecho()

string = "This is a test"

stdscr.addstr(string)

stdscr.move(0, 0)

while True:
  input = stdscr.getch()

  # if the user pressed escape in the program it will close
  if input == 27:
    break

  stdscr.addstr(chr(input))


curses.endwin()