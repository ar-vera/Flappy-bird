import tkinter as tk
import random

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
BIRD_SIZE = 30
PIPE_WIDTH = 60
PIPE_GAP = 200
GRAVITY = 3
JUMP_STRENGTH = -15
PIPE_SPEED = 5

class FlappyBirdGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flappy Bird")
        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.bird = self.canvas.create_oval(100, 200, 100 + BIRD_SIZE, 200 + BIRD_SIZE, fill="yellow")
        self.pipes = []
        self.score = 0
        self.velocity = 0
        self.running = False

        self.start_text = self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
            text="Press any key to start", font=("Arial", 24), fill="white"
        )

        self.score_text = self.canvas.create_text(
            10, 10, anchor="nw", font=("Arial", 16), fill="white", text=f"Score: {self.score}"
        )

        self.root.bind("<Key>", self.start_game)

    def start_game(self, event=None):
        #Запуск игры по нажатию клавиши
        if not self.running:
            self.running = True
            self.canvas.delete(self.start_text)
            self.root.bind("<space>", self.jump)
            self.create_pipe()
            self.update_game()

    def jump(self, event):
        self.velocity = JUMP_STRENGTH

    def create_pipe(self):
        pipe_top_height = random.randint(50, WINDOW_HEIGHT - PIPE_GAP - 50)
        pipe_bottom_height = pipe_top_height + PIPE_GAP
        pipe_top = self.canvas.create_rectangle(WINDOW_WIDTH, 0, WINDOW_WIDTH + PIPE_WIDTH, pipe_top_height, fill="green")
        pipe_bottom = self.canvas.create_rectangle(WINDOW_WIDTH, pipe_bottom_height, WINDOW_WIDTH + PIPE_WIDTH, WINDOW_HEIGHT, fill="green")
        self.pipes.append((pipe_top, pipe_bottom))

    def update_game(self):
        if self.running:
            self.update_bird()
            self.update_pipes()
            self.check_collisions()
            self.root.after(30, self.update_game)

    def update_bird(self):
        self.velocity += GRAVITY
        self.canvas.move(self.bird, 0, self.velocity)
        bird_coords = self.canvas.coords(self.bird)
        if bird_coords[1] <= 0 or bird_coords[3] >= WINDOW_HEIGHT:
            self.game_over()

    def update_pipes(self):
        for pipe_top, pipe_bottom in self.pipes:
            self.canvas.move(pipe_top, -PIPE_SPEED, 0)
            self.canvas.move(pipe_bottom, -PIPE_SPEED, 0)
        self.pipes = [(pt, pb) for pt, pb in self.pipes if self.canvas.coords(pt)[2] > 0]

        if len(self.pipes) == 0 or self.canvas.coords(self.pipes[-1][0])[2] < WINDOW_WIDTH - 200:
            self.create_pipe()

        self.check_score()

    def check_score(self):
        for pipe_top, pipe_bottom in self.pipes:
            if self.canvas.coords(pipe_top)[2] <= 100 and self.canvas.coords(pipe_top)[2] > 95:
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def check_collisions(self):
        #Столкновения
        bird_coords = self.canvas.coords(self.bird)
        for pipe_top, pipe_bottom in self.pipes:
            if self.intersects(bird_coords, self.canvas.coords(pipe_top)) or self.intersects(bird_coords, self.canvas.coords(pipe_bottom)):
                self.game_over()

    def intersects(self, rect1, rect2):
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3])

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
            text="Game Over", font=("Arial", 32), fill="red"
        )

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()