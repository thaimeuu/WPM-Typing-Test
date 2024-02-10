import curses
from curses import wrapper
import time
import random


def start_game(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to WPM-Typing-Test. Press any key to start..", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getkey()    


def wpm(stdscr):
    with open("texts.txt", "r") as f:
        lines = f.readlines()
    
    test = random.choice(lines).strip()
    current_text = []
    start_time = time.time()
    wpm = 0
    stdscr.nodelay(True)
    
    while True:
        time_passed = max(time.time() - start_time, 1)
        wpm = round((60 / time_passed) * len(current_text) / 5)
        
        stdscr.clear()
        stdscr.addstr(test)
        stdscr.addstr(1, 0, f"WPM: {wpm}")
        
        for i, char in enumerate(current_text):
            if char == test[i]:
                stdscr.addstr(0, i, char, curses.color_pair(1))
            else:
                stdscr.addstr(0, i, char, curses.color_pair(2))
        
        stdscr.refresh()
        
        # Quit program when correct answer is received
        if "".join(current_text) == test:
            stdscr.nodelay(False)
            break
        
        try: 
            key = stdscr.getkey()
        except:
            continue
        
        # Quit program when use hit escape (esc)
        try:
            if ord(key) == 27:
                break
        except:
            pass
        # Handling backspace
        if key in ["KEY_BACKSPACE", "\b", "\x7f"]:
            if len(current_text) > 0:
                current_text.pop()
        # Handling arrow key, pg up, pg dn
        elif key in ["KEY_UP", "KEY_DOWN", "KEY_RIGHT", "KEY_LEFT", "KEY_PPAGE", "KEY_NPAGE"]:
            pass 
        elif len(current_text) < len(test):
            current_text.append(key)
        
        
        
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    start_game(stdscr)
    
    while True:
        wpm(stdscr)
        stdscr.addstr(2, 0, "You completed the challenge! Press any key to play again. Press esc to quit.")
        key = stdscr.getkey()
        try:
            if ord(key) == 27:
                break
        except:
            continue
    
wrapper(main)
