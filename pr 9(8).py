import tkinter as tk
import random
import heapq
import time
from collections import deque

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
        self.goal_x, self.goal_y = 8, 9
        self.dynamic_objects = [(4, 4), (7, 2)]
        self.object_directions = [(1, 0), (0, 1)]  # Directions for dynamic objects

        self.maze_canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.maze_canvas.pack(side="left")

        self.trace_canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.trace_canvas.pack(side="right")

        self.trace_map = tk.PhotoImage(width=400, height=400)
        self.trace_canvas.create_image((0, 0), image=self.trace_map, anchor="nw")

        self.root.bind("<KeyPress>", self.on_key_press)

        self.start_time = None  # Track the start time for efficiency calculation
        self.steps_count = 0  # Track the number of steps taken by the player
        self.optimal_path = None
        self.real_path = []  # To store the real path of the player

        self.draw_maze()

        # Create buttons for selecting algorithm
        self.a_star_button = tk.Button(self.root, text="A* Path", command=self.show_a_star_path)
        self.a_star_button.pack(side="top")

        self.dijkstra_button = tk.Button(self.root, text="Dijkstra Path", command=self.show_dijkstra_path)
        self.dijkstra_button.pack(side="top")

        self.wave_button = tk.Button(self.root, text="Wave Algorithm Path", command=self.show_wave_path)
        self.wave_button.pack(side="top")

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

                if x == self.goal_x and y == self.goal_y:
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
        if self.start_time is None:  # Start timing when the player moves for the first time
            self.start_time = time.time()

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
                self.real_path.append((self.player_x, self.player_y))  # Track the real path
                self.update_trace()
                self.player_x, self.player_y = new_x, new_y
                self.steps_count += 1
                self.draw_maze()

        # Compare the real path with the optimal path
        if (self.player_x, self.player_y) == (self.goal_x, self.goal_y):
            self.end_game()

    def a_star(self, start_x, start_y, goal_x, goal_y):
        """A* pathfinding algorithm"""
        open_list = []
        closed_list = set()
        came_from = {}
        g_score = { (start_x, start_y): 0 }
        f_score = { (start_x, start_y): self.heuristic(start_x, start_y, goal_x, goal_y) }

        heapq.heappush(open_list, (f_score[(start_x, start_y)], (start_x, start_y)))

        while open_list:
            _, current = heapq.heappop(open_list)
            current_x, current_y = current

            if (current_x, current_y) == (goal_x, goal_y):
                return self.reconstruct_path(came_from, current)

            closed_list.add((current_x, current_y))

            for neighbor in self.get_neighbors(current_x, current_y):
                if neighbor in closed_list:
                    continue

                tentative_g_score = g_score.get((current_x, current_y), float('inf')) + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = (current_x, current_y)
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor[0], neighbor[1], goal_x, goal_y)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return []

    def heuristic(self, x, y, goal_x, goal_y):
        """Calculate Manhattan distance"""
        return abs(x - goal_x) + abs(y - goal_y)

    def get_neighbors(self, x, y):
        """Get valid neighbors (up, down, left, right)"""
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze) and self.maze[ny][nx] == 0:
                neighbors.append((nx, ny))
        return neighbors

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append((self.player_x, self.player_y))
        path.reverse()
        return path

    def dijkstra(self, start_x, start_y, goal_x, goal_y):
        """Dijkstra's algorithm"""
        queue = [(0, start_x, start_y)]  # (distance, x, y)
        distances = { (start_x, start_y): 0 }
        came_from = {}

        while queue:
            current_distance, current_x, current_y = heapq.heappop(queue)

            if (current_x, current_y) == (goal_x, goal_y):
                return self.reconstruct_path(came_from, (current_x, current_y))

            for neighbor in self.get_neighbors(current_x, current_y):
                tentative_distance = current_distance + 1
                if neighbor not in distances or tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heapq.heappush(queue, (tentative_distance, neighbor[0], neighbor[1]))
                    came_from[neighbor] = (current_x, current_y)

        return []

    def wave_algorithm(self, start_x, start_y, goal_x, goal_y):
        """Wave Algorithm (BFS-based)"""
        queue = deque([(start_x, start_y)])
        came_from = { (start_x, start_y): None }
        while queue:
            current_x, current_y = queue.popleft()

            if (current_x, current_y) == (goal_x, goal_y):
                return self.reconstruct_path(came_from, (current_x, current_y))

            for neighbor in self.get_neighbors(current_x, current_y):
                if neighbor not in came_from:
                    came_from[neighbor] = (current_x, current_y)
                    queue.append(neighbor)

        return []

    def show_a_star_path(self):
        self.optimal_path = self.a_star(self.player_x, self.player_y, self.goal_x, self.goal_y)
        self.show_optimal_path()

    def show_dijkstra_path(self):
        self.optimal_path = self.dijkstra(self.player_x, self.player_y, self.goal_x, self.goal_y)
        self.show_optimal_path()

    def show_wave_path(self):
        self.optimal_path = self.wave_algorithm(self.player_x, self.player_y, self.goal_x, self.goal_y)
        self.show_optimal_path()

    def show_optimal_path(self):
        if self.optimal_path:
            for (x, y) in self.optimal_path:
                self.maze_canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill="yellow", outline="gray"
                )
            print("Оптимальный путь найден!")

    def end_game(self):
        """When the player reaches the goal"""
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        optimal_steps = len(self.optimal_path)
        real_steps = len(self.real_path)
        print(f"Игра окончена! Время: {elapsed_time:.2f} секунд")
        print(f"Оптимальные шаги: {optimal_steps}, Шаги игрока: {real_steps}")
        print(f"Эффективность: {real_steps / optimal_steps:.2f} ")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("850x450")
    app = MazeGame(root)
    root.mainloop()
