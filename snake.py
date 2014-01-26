#!/usr/bin/env python3.3

import curses
import random
import time
import signal


def redraw(window, snake):
    window.erase()
    for i in range(curses.LINES):
        for j in range(curses.COLS):
            if snake[i][j] != 0:
                window.addch(i, j, '*')
    window.refresh()

def food(snake):
    y = random.randint(0, curses.LINES)
    x = random.randint(0, curses.COLS)
    while snake[y][x] != 0:
        y = random.randint(0, curses.LINES)
        x = random.randint(0, curses.COLS)
    snake[y][x] = -1

def run():
    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.curs_set(False)
    stdscr.border(0)

    snake = [[0 for i in range(curses.COLS)] for j in range(curses.LINES)]
    snake[curses.LINES // 2][curses.COLS // 2] = 1
    data = {'drow': 0, 'dcol': 1, 'total_nodes': 1,
            'head_y': curses.LINES // 2, 'head_x': curses.COLS // 2}

    food(snake)
    redraw(stdscr, snake)
    # move(stdscr, snake, data)

    def move(signum, frame):
        data['head_y'] = data['head_y'] + data['drow']
        data['head_x'] = data['head_x'] + data['dcol']
        if snake[data['head_y']][data['head_x']] == -1:
            snake[data['head_y']][data['head_x']] = data['total_nodes'] + 1
            data['total_nodes'] = data['total_nodes'] + 1
            food(snake)
        elif snake[data['head_y']][data['head_x']] == 0:
            snake[data['head_y']][data['head_x']] = data['total_nodes'] + 1
            for i in range(curses.LINES):
                for j in range(curses.COLS):
                    if snake[i][j] > 0:
                        snake[i][j] = snake[i][j] - 1
        redraw(stdscr, snake)

    def none_handler():
        pass

    signal.signal(signal.SIGALRM, move)
    while True:
        signal.alarm(1)
        c = stdscr.getch()
        if c == ord('q'):
            stdscr.keypad(False)
            curses.endwin()
            signal.signal(signal.SIGTERM, none_handler)
        elif c == curses.KEY_LEFT:
            data['drow'] = 0
            data['dcol'] = -1
        elif c == curses.KEY_RIGHT:
            data['drow'] = 0
            data['dcol'] = 1
        elif c == curses.KEY_UP:
            data['drow'] = -1
            data['dcol'] = 0
        elif c == curses.KEY_DOWN:
            data['drow'] = 1
            data['dcol'] = 0
run()
