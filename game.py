import curses

def game(stdscr):
  stdscr.keypad(0)
  curses.noecho()
  
  string = "you should not be able to change this"

  stdscr.addstr(string)
  stdscr.move(0,0)

  while True:
    input = stdscr.getch()

    # if the user pressed escape in the program it will close
    if input == 27:
      break

    elif input == 8:
      try:
        pos = stdscr.getyx()
        stdscr.addstr(pos[0],pos[1],string[pos[1]])
        stdscr.move(pos[0],pos[1]-1)
      except:
        stdscr.move(0,0)
        pass

    else: 
      stdscr.addstr(chr(input))


  curses.endwin()

def main():
    curses.wrapper(game)

if (__name__ == "__main__"):
    main()

main()