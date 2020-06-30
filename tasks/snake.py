""" Following https://realpython.com/python-print/#building-console-user-interfaces """

import curses, time

def main(screen):
    curses.curs_set(0)  # Hide the cursor

    snake = [(0, i) for i in reversed(range(20))]
    
    # Draw the snake
    screen.addstr(*snake[0], '@')
    for segment in snake[1:]:
        screen.addstr(*segment, '*')

    screen.refresh()


    time.sleep(1)


##########
if __name__ == "__main__":
    # use the wrapper to protect terminal in event of code error
    curses.wrapper(main)