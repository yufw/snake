import random
import select
import sys
import termios
import time
import tty

class Snake:
    def __init__(self):
        self.body = [(5, 5), (6, 5), (7, 5)] # tail to head
        self.direction = 'right'

    def setdir(self, direction): # cannot turn back
        dirs = ['left', 'up', 'down', 'right']
        if (dirs.index(self.direction) + dirs.index(direction)) != 3:
            self.direction = direction

    def move(self, food):
        direction = self.direction
        x, y = self.body[-1]
        if direction == 'right':
            x += 1
        elif direction == 'left':
            x -= 1
        elif direction == 'up':
            y -= 1
        elif direction == 'down':
            y += 1
        newhead = (x, y)
        self.body.append(newhead)
        if newhead != (food.x, food.y): # not eating
            self.body.pop(0)
        return newhead

class Food:
    def __init__(self, xmax, ymax):
        self.xmax = xmax
        self.ymax = ymax

    def feed(self):
        self.x = random.randint(0, self.xmax)
        self.y = random.randint(0, self.ymax)

class Game:
    def __init__(self, height, width):
        self.board = (height, width) # height and width
        self.snake = Snake()
        self.food = Food(width-1, height-1)
        self.food.feed()
        self.paused = False

    def render(self):
        sys.stdout.write("\x1b[2J\x1b[H")
        board = [[' ' for x in range(self.board[1])] for y in range(self.board[0])]
        for c in self.snake.body:
            board[c[1]][c[0]] = 'x'
        board[self.food.y][self.food.x] = '*'
        for line in board:
            sys.stdout.write(''.join(line) + '<' + '\r\n')
        sys.stdout.write('^' * (self.board[1] + 1) + '\r\n')
        sys.stdout.flush()
            
    def loop(self, old):
        while True:
            self.render()
            ch = None
            rl, _, _ = select.select([sys.stdin], [], [], 0.17)
            if rl:
                ch = sys.stdin.read(1)
                if ch == 'q':
                    self.quit(old)
                    return
                elif ch == 'p':
                    self.paused = not self.paused
            if self.paused:
                continue
            elif ch == 'l':
                self.snake.setdir('right')
            elif ch == 'j':
                self.snake.setdir('left')
            elif ch == 'k':
                self.snake.setdir('down')
            elif ch == 'i':
                self.snake.setdir('up')
            else:
                self.snake.setdir(self.snake.direction)
            newhead = self.snake.move(self.food)
            if not self.check(newhead):
                self.quit(old)
                return
            if newhead == (self.food.x, self.food.y): # it is eating
                self.food.feed()

    def quit(self, oldsetting):
        sys.stdout.write('life is too long' + '\r\n')
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldsetting)
        sys.stdout.write("\033[?25h")

    def check(self, newhead):
        x, y = newhead
        if 0 <= x < self.board[1] and 0 <= y < self.board[0]:
            return True
        else:
            return False

    def main(self):
        old = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        sys.stdout.write("\033[?25l")
        self.loop(old)

if __name__ == '__main__':
    g = Game(20, 40)
    g.main()
