import tkinter as tk
import random
from queue import PriorityQueue

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game v2")

        self.cell_size = 40
        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 2, 0, 0, 1, 0, 3, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 4, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        ]
        self.start = (1, 0)
        self.end = (8, 9)
        self.player_x, self.player_y = self.start
        self.teleport_points = [(5, 8), (4, 4)]
        self.frozen_turns = 0

        self.maze_canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.maze_canvas.pack()

        self.root.bind("<KeyPress>", self.on_key_press)
        self.draw_maze()

        if not self.check_reachability():
            print("Конечная точка недостижима!")
        else:
            print("Конечная точка достижима!")

    def draw_maze(self):
        self.maze_canvas.delete("all")
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                color = "black" if self.maze[y][x] == 1 else "white"
                if self.maze[y][x] == 2:
                    color = "orange"  # Slowdown obstacle
                elif self.maze[y][x] == 3:
                    color = "red"  # Dangerous obstacle
                elif self.maze[y][x] == 4:
                    color = "purple"  # Teleport obstacle

                self.maze_canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline="gray"
                )

                if (x, y) == self.start:
                    self.maze_canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="blue"
                    )

                if (x, y) == self.end:
                    self.maze_canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="green"
                    )

        self.maze_canvas.create_rectangle(
            self.player_x * self.cell_size, self.player_y * self.cell_size,
            (self.player_x + 1) * self.cell_size, (self.player_y + 1) * self.cell_size,
            fill="blue"
        )

    def on_key_press(self, event):
        if self.frozen_turns > 0:
            self.frozen_turns -= 1
            return

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
            cell = self.maze[new_y][new_x]
            if cell == 0:
                self.player_x, self.player_y = new_x, new_y
            elif cell == 2:
                self.player_x, self.player_y = new_x, new_y
                self.root.after(500)
            elif cell == 3:
                self.player_x, self.player_y = self.start
            elif cell == 4:
                self.player_x, self.player_y = random.choice(self.teleport_points)

        self.draw_maze()

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self):
        start, goal = self.start, self.end
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            _, current = frontier.get()

            if current == goal:
                break

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_x, next_y = current[0] + dx, current[1] + dy
                if 0 <= next_x < len(self.maze[0]) and 0 <= next_y < len(self.maze):
                    if self.maze[next_y][next_x] != 1:
                        cost = 1
                        if self.maze[next_y][next_x] == 2: 
                            cost = 2
                        elif self.maze[next_y][next_x] == 3:  
                            continue  

                        next_cost = cost_so_far[current] + cost
                        next_cell = (next_x, next_y)
                        if next_cell not in cost_so_far or next_cost < cost_so_far[next_cell]:
                            cost_so_far[next_cell] = next_cost
                            priority = next_cost + self.heuristic(goal, next_cell)
                            frontier.put((priority, next_cell))
                            came_from[next_cell] = current

        return came_from

    def check_reachability(self):
        came_from = self.a_star_search()
        return self.end in came_from

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x450")
    game = MazeGame(root)
    root.mainloop()
