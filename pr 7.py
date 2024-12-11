import tkinter as tk
import random

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game")

        self.cell_size = 40
        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        ]
        self.player_x, self.player_y = 1, 0
        self.dynamic_objects = [(4, 4), (7, 2)]
        self.object_directions = [(1, 0), (0, 1)]  # Directions for dynamic objects

        self.maze_canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.maze_canvas.pack(side="left")

        self.trace_canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.trace_canvas.pack(side="right")

        self.trace_map = tk.PhotoImage(width=400, height=400)
        self.trace_canvas.create_image((0, 0), image=self.trace_map, anchor="nw")

        self.root.bind("<KeyPress>", self.on_key_press)
        self.draw_maze()
        self.move_dynamic_objects()

    def draw_maze(self):
        self.maze_canvas.delete("all")
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                color = "black" if self.maze[y][x] == 1 else "white"
                self.maze_canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline="gray"
                )

                if x == self.player_x and y == self.player_y:
                    self.maze_canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="blue"
                    )

                if x == 8 and y == 9:
                    self.maze_canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="green"
                    )

        for obj_x, obj_y in self.dynamic_objects:
            self.maze_canvas.create_oval(
                obj_x * self.cell_size + 5, obj_y * self.cell_size + 5,
                (obj_x + 1) * self.cell_size - 5, (obj_y + 1) * self.cell_size - 5,
                fill="red"
            )

    def update_trace(self):
        x1 = self.player_x * self.cell_size
        y1 = self.player_y * self.cell_size
        x2 = (self.player_x + 1) * self.cell_size
        y2 = (self.player_y + 1) * self.cell_size

        self.trace_canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="")

    def on_key_press(self, event):
        new_x, new_y = self.player_x, self.player_y

        if event.keysym == "Up":
            new_y -= 1
        elif event.keysym == "Down":
            new_y += 1
        elif event.keysym == "Left":
            new_x -= 1
        elif event.keysym == "Right":
            new_x += 1

        if 0 <= new_x < len(self.maze[0]) and 0 <= new_y < len(self.maze):
            if self.maze[new_y][new_x] == 0:
                self.update_trace()
                self.player_x, self.player_y = new_x, new_y
                self.draw_maze()

    def move_dynamic_objects(self):
        for i, (obj_x, obj_y) in enumerate(self.dynamic_objects):
            dir_x, dir_y = self.object_directions[i]
            new_x, new_y = obj_x + dir_x, obj_y + dir_y

            if (new_x < 0 or new_x >= len(self.maze[0]) or
                new_y < 0 or new_y >= len(self.maze) or
                self.maze[new_y][new_x] == 1 or
                (new_x, new_y) in self.dynamic_objects or
                (new_x == self.player_x and new_y == self.player_y)):
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(directions)
                for new_dir_x, new_dir_y in directions:
                    temp_x, temp_y = obj_x + new_dir_x, obj_y + new_dir_y
                    if (0 <= temp_x < len(self.maze[0]) and 0 <= temp_y < len(self.maze) and
                        self.maze[temp_y][temp_x] == 0 and
                        (temp_x, temp_y) not in self.dynamic_objects and
                        not (temp_x == self.player_x and temp_y == self.player_y)):
                        dir_x, dir_y = new_dir_x, new_dir_y
                        new_x, new_y = temp_x, temp_y
                        break
                else:
                    dir_x, dir_y = -dir_x, -dir_y

            self.dynamic_objects[i] = (new_x, new_y)
            self.object_directions[i] = (dir_x, dir_y)

        self.draw_maze()
        self.root.after(500, self.move_dynamic_objects)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("850x450")
    app = MazeGame(root)
    root.mainloop()
    