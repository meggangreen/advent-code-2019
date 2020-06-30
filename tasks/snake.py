""" Following https://realpython.com/python-print/#building-console-user-interfaces """

import curses, time

def main(screen):
    curses.curs_set(0)  # Hide the cursor
    time.sleep(1)


##########
if __name__ == "__main__":
    # use the wrapper to protect terminal in event of code error
    curses.wrapper(main)