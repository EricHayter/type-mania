import curses
import time

player_scores = {"312": 20, "420": 50}

curses.initscr()

def progress_bar(scores):
    win = curses.newwin(len(scores),50,0,0) 
    while 1:
        win.clear()
        for h, (id,score) in enumerate(scores.items()):
            score = bar(score)
            score = f"player {id}: {score}"
            win.addstr(h,0,score)

        win.refresh()
        time.sleep(0.016)


def bar(percent):
    percent = int(percent)
    string = ""
    percent_complete = percent // 5
    string += "#" * percent_complete 
    string += "." * (20 - percent_complete)
    return string

progress_bar(player_scores)
