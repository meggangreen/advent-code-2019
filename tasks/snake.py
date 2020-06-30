""" Following https://realpython.com/python-print/#building-console-user-interfaces """
import curses

def main(screen):
    pass


##########
if __name__ == "__main__":
    # use the wrapper to protect terminal in event of code error
    curses.wrapper(main)