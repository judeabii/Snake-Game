# Snake Game
Snake Game using Python GUI

This is implemented using the tkinter module which is built into the Python Standard library

## Code Explanation
Open up the GUI window using tkinter, with the title "SNAKE GAME".
```commandline
root = Tk()
root.title("SNAKE GAME")
root.resizable(False, False)
```

Next step is to set up the label which keeps track of the score and the playing canvas.
```commandline
score = 0
    label = Label(root, text=f"Score is : {score}", font=('consolas', 50))
    label.pack()

    canvas = Canvas(root, bg="#000000", height=700, width=700)
    canvas.pack()
```


The `Snake` class contains all the attributes required for the snake, which includes a list of coordinates of the all the snakes body parts and the canvas objects (square)
of the snake.

Initial body size of the snake is 3, which means 3 squares are created for the snake at the start on the canvas.

Starting postion of the snake is at x=0,y=0, which is the top left corner of the canvas
```commandline
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
```
The `Food` class is used to randomly generate the position of food(apple) anywhere on the playing canvas. The attributes of the class include the (x,y) coordinates
of the food object and the canvas object (square) of the apple.
```commandline
class Food:

    def __init__(self):
        x = random.randint(0, 13) * 50
        y = random.randint(0, 13) * 50
        self.coordinates = [x, y]
        self.position = canvas.create_rectangle(x, y, x + 50, y + 50, fill="#FF0000", tags="food")
```

### Gameplay Code
Once the food and snake are set up on the canvas, we would need to bind the keyboard
arrow keys to change direction. Initially the snake starts moving downwards.
```commandline
direction = "down"

root.bind('<Left>', lambda event: change_direction('left'))
root.bind('<Right>', lambda event: change_direction('right'))
root.bind('<Down>', lambda event: change_direction('down'))
root.bind('<Up>', lambda event: change_direction('up'))
```
Depending on the direction at the time, the snake-head square object changes its position on the canvas. Adding
the new x,y head coordinates of the snake head into the 0th position of the list. 
```commandline
snake.coordinates.insert(0, [x, y])
square = canvas.create_rectangle(x, y, x + 50, y + 50, fill="#00FF00")
snake.squares.insert(0, square)
```
As the snake moves, a new head coordinate is added, and at the same time the old tail coordinate should be deleted
and the tail square object should be deleted.

This is to ensure the snake size stays constant as it moves.
```commandline
del snake.coordinates[-1]
canvas.delete(snake.squares[-1])
del snake.squares[-1]
```

If the snake eats the food (apple), the apple should disappear and reappear at a random location on the canvas, and
the snake should get longer by one square object. Not to forget, the score should get updated too.

This is handled by the code below by comparing the x,y coordinates of the snake head with the food.
```commandline
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
```
Last but not least, we also have to check for collisions, which would conclude the game.
```commandline
def check_collision(snake):
    x, y = snake.coordinates[0]

    for x_pos, y_pos in snake.coordinates[1:]:
        if x_pos == x and y_pos == y:
            return True

    if x >= 700 or y >= 700 or x < 0 or y < 0:
        return True

    return False
```
After the game ends, the user is presented with a "Play Again" button on the canvas. On clicking it, the game restarts.
```commandline
label.config(text=f"GAME OVER", fg="red")

play_again = Button(root, text="Play Again", font=("Helvetica", 20), width=15, command=play)
canvas.create_window(350, 370, window=play_again)
canvas.create_text(350, 450, text=f"{score}",font=("Helvetica",20),fill="white")
```
![Play again screenshot](/images/SnakeGame_PlayAgain.png)
