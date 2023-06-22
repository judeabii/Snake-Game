import random
import tkinter.messagebox
from tkinter import *
from tkinter import messagebox


class Snake:

    def __init__(self):
        self.body_size = 3
        self.coordinates = []
        self.squares = []

        for i in range(0, 3):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + 50, y + 50, fill="#00FF00")
            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, 13) * 50
        y = random.randint(0, 13) * 50
        self.coordinates = [x, y]
        self.position = canvas.create_rectangle(x, y, x + 50, y + 50, fill="#FF0000", tags="food")


def gameover():
    global play_again
    play_again = False
    canvas.delete("all")
    label.config(text=f"GAME OVER", fg="red")

    play_again = Button(root, text="Play Again", font=("Helvetica", 20), width=15, command=play)
    canvas.create_window(350, 370, window=play_again)
    canvas.create_text(350, 450, text=f"{score}",font=("Helvetica",20),fill="white")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= 50
    if direction == 'down':
        y += 50
    if direction == 'left':
        x -= 50
    if direction == 'right':
        x += 50

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + 50, y + 50, fill="#00FF00")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        label.config(text=f"Score is : {score}")

        last_x, last_y = snake.coordinates[-1]
        snake.coordinates.insert(-1, [last_x, last_y])
        square = canvas.create_rectangle(last_x, last_y, last_x + 50, last_y + 50, fill="#00FF00")
        snake.squares.insert(-1, square)

        canvas.delete(food.position)
        del food.coordinates
        food = Food()

    del snake.coordinates[-1]
    canvas.delete(snake.squares[-1])
    del snake.squares[-1]

    if check_collision(snake):
        gameover()
    else:
        root.after(100, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    if new_direction == 'right' and direction != 'left':
        direction = new_direction
    if new_direction == 'up' and direction != 'down':
        direction = new_direction
    if new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collision(snake):
    x, y = snake.coordinates[0]

    for x_pos, y_pos in snake.coordinates[1:]:
        if x_pos == x and y_pos == y:
            return True

    if x >= 700 or y >= 700 or x < 0 or y < 0:
        return True

    return False


def play():
    global score, label, canvas, direction
    try:
        label.destroy()
        canvas.destroy()
    except NameError:
        pass

    score = 0
    label = Label(root, text=f"Score is : {score}", font=('consolas', 50))
    label.pack()

    canvas = Canvas(root, bg="#000000", height=700, width=700)
    canvas.pack()

    direction = "down"

    root.bind('<Left>', lambda event: change_direction('left'))
    root.bind('<Right>', lambda event: change_direction('right'))
    root.bind('<Down>', lambda event: change_direction('down'))
    root.bind('<Up>', lambda event: change_direction('up'))

    food = Food()
    snake = Snake()
    next_turn(snake, food)

    root.mainloop()


root = Tk()
root.title("SNAKE GAME")
root.resizable(False, False)
play()
