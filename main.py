import curses
from datetime import datetime as dt
from random import randint

stdscr = curses.initscr()

if curses.has_colors():
    curses.start_color()

curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)

lastsec = dt.now()

initlen = 20
interval = 69420 # in microseconds

def reapple(lis, apple):
    while 1:
        napple = randint(0, curses.LINES-2), round(randint(0, curses.COLS-2)/2)
        if napple not in lis + [apple]:
            apple = napple
            break
    return apple

def psnake(scr, lis, dir, apple, move=False, die=False):
    global stdscr
    stdscr.move(0, 0)
    stdscr.chgat(-1, curses.A_REVERSE)
    stdscr.addstr("  cursnake ", curses.A_REVERSE)
    stdscr.addstr(f" length: {len(lis)} ")
    stdscr.addstr(f" arrow keys to move, q to quit, r to restart ", curses.A_REVERSE)
    stdscr.refresh()

    scr.clear()

    y, x = lis[-1]
    
    dir = [dir[-1], dir[-1]]

    if not die:
        if move:
            if apple in lis:
                y, x = apple 
            match dir[-1]:
                case "up":
                    newc = (y-1, x)
                case "down":
                    newc = (y+1, x)
                case "left":
                    newc = (y, x-1)
                case "right":
                    newc = (y, x+1)
                case _:
                    newc = (y, x)
            if apple in lis:
                apple = reapple(lis, apple)
                lis.append(newc)
            else:
                lis = lis[1:] + [newc]
        if sorted(list(set(lis))) != sorted(lis):
            lis, apple, die, dir = psnake(scr, lis, dir, apple, move=False, die=True)
            die = True
            return lis, apple, die, dir
    for y, x in lis:
        if not die:
            try:
                scr.chgat(y, x*2, 2, curses.A_REVERSE)
            except:
                lis, apple, die = psnake(scr, lis, dir, apple, move=False, die=True)
                die = True
                return lis, apple, die, dir
        else:
            try:
                scr.addstr(y, x*2, "  " if x*2+1 != curses.COLS else " ", curses.color_pair(1))
            except:
                pass 
        scr.addstr(apple[0], apple[1]*2, "  ", curses.color_pair(1))
    scr.refresh()
    return lis, apple, die, dir

def main(stdscr):
    global lastsec

    snakewin = curses.newwin(curses.LINES-1, curses.COLS, 1, 0)
    snakewin.nodelay(True)
    snakewin.keypad(1)
    pixels = [(round(curses.LINES/2), x) for x in range(initlen)]
    dir = ["right"]
    curses.curs_set(0)
    apple = reapple(pixels, (0, 0))
    pixels, apple, die, dir = psnake(snakewin, pixels, dir, apple)
    die = False

    while True:
        brk = False
        if not die:
            while True:
                if (dt.now() - lastsec).microseconds > interval:
                    pixels, apple, die, dir = psnake(snakewin, pixels, dir, apple, True)
                    lastsec = dt.now()
                c = snakewin.getch()
                if c != -1:
                    match chr(c):
                        case "q" | "Q":
                            brk = True
                            break
                        case "r" | "R":
                            snakewin = curses.newwin(curses.LINES-1, curses.COLS, 1, 0)
                            snakewin.nodelay(True)
                            snakewin.keypad(1)
                            pixels = [(round(curses.LINES/2), x) for x in range(initlen)]
                            dir = ["right"]
                            curses.curs_set(0)
                            apple = reapple(pixels, (0, 0))
                            pixels, apple, die, dir = psnake(snakewin, pixels, dir, apple)
                            die = False
                            continue
                        case "ă":
                            if "down" not in dir:
                                dir = [dir[-1], "up"]
                        case "Ą":
                            if "right" not in dir:
                                dir = [dir[-1], "left"]
                        case "Ă":
                            if "up" not in dir:
                                dir = [dir[-1], "down"]
                        case "ą":
                            if "left" not in dir:
                                dir = [dir[-1], "right"]
                if die:
                    break
        c = snakewin.getch()
        if c != -1:
            match chr(c):
                case "q" | "Q":
                    break
                case "r" | "R":
                    snakewin = curses.newwin(curses.LINES-1, curses.COLS, 1, 0)
                    snakewin.nodelay(True)
                    snakewin.keypad(1)
                    pixels = [(round(curses.LINES/2), x) for x in range(initlen)]
                    dir = "right"
                    curses.curs_set(0)
                    apple = reapple(pixels, (0, 0))
                    pixels, apple, die, dir = psnake(snakewin, pixels, dir, apple)
                    die = False
                    continue 
        if brk:
            break

curses.wrapper(main)
