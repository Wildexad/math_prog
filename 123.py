import tkinter as tk 
from tkinter import messagebox 
import random 

ships_config = { 
"Эсминец": 1, 
"Катер": 0
} 

ship_sizes = { 
"Эсминец": 4, 
"Катер": 1 
} 
debug = False 
debug_window = None 
placed_ships = {} 
current_orientation = "horizontal" 
orientation_button = None 
start_button = None 
auto_place_button = None  

 
 
def display_board(battlefield, board, hide_ships=False): 
    battlefield.delete("all") 
    n = len(board) 
    cell_size = 500 // n 
    for i in range(n): 
        for j in range(n): 
            if hide_ships and board[i][j] == 1: 
                color = "white"  
            elif board[i][j] == 0: 
                color = "white"  
            elif board[i][j] == 1: 
                color = "green"  
            elif board[i][j] == 2: 
                color = "red"  
            elif board[i][j] == 3: 
                color = "gray"  
            battlefield.create_rectangle( 
                j * cell_size, i * cell_size, 
                (j + 1) * cell_size, (i + 1) * cell_size, 
                fill=color, outline="black" 
            ) 
 
def update_remaining_ships_label(label): 
    remaining_ships = [] 
    for ship, count in ships_config.items(): 
        remaining = count - placed_ships.get(ship, 0) 
        if remaining > 0: 
            remaining_ships.append(f"{ship}: {remaining}") 
    label.config(text="\n" + "\n".join(remaining_ships)) 
 
def generate_board(size): 
    board = [[0 for _ in range(size)] for _ in range(size)] 
    for ship, count in ships_config.items(): 
        ship_size = ship_sizes[ship] 
        for _ in range(count): 
            placed = False 
            while not placed: 
                orientation = random.choice(["horizontal", "vertical"]) 
                if orientation == "horizontal": 
                    x = random.randint(0, size - ship_size) 
                    y = random.randint(0, size - 1) 
                    if (all(board[y][x + i] == 0 for i in range(ship_size)) 
                        and check_surroundings(board, x, y, ship_size, "horizontal")): 
                        for i in range(ship_size): 
                            board[y][x + i] = 1 
                        placed = True 
                else: 
                    x = random.randint(0, size - 1) 
                    y = random.randint(0, size - ship_size) 
                    if (all(board[y + i][x] == 0 for i in range(ship_size)) 
                        and check_surroundings(board, x, y, ship_size, "vertical")): 
                        for i in range(ship_size): 
                            board[y + i][x] = 1 
                        placed = True 
    return board 
 
 
 
def check_victory(board): 
    for row in board: 
        if 1 in row: 
            return False 
    return True 
 
def check_and_paint_surroundings(board, ship_cells, battlefield): 
    for cell_y, cell_x in ship_cells: 
        for dx in [-1, 0, 1]: 
            for dy in [-1, 0, 1]: 
                nx, ny = cell_x + dx, cell_y + dy 
                if (0 <= nx < 10 and 0 <= ny < 10 and board[ny][nx] == 0): 
                    board[ny][nx] = 3  
                    cell_size = 500 // len(board) 
                    battlefield.create_rectangle( 
                        nx * cell_size, ny * cell_size, 
                        (nx + 1) * cell_size, (ny + 1) * cell_size, 
                        fill="gray", outline="black" 
                    ) 
 
def is_ship_sunk(board, x, y): 
    ship_cells = [(y, x)] 
    visited = set(ship_cells) 
    queue = [(y, x)] 
    while queue: 
        cell_y, cell_x = queue.pop(0) 
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
            nx, ny = cell_x + dx, cell_y + dy 
            if (0 <= nx < 10 and 0 <= ny < 10 and 
                (ny, nx) not in visited and board[ny][nx] in [1, 2]): 
                visited.add((ny, nx)) 
                ship_cells.append((ny, nx)) 
                queue.append((ny, nx)) 
    for cell_y, cell_x in ship_cells: 
        if board[cell_y][cell_x] != 2: 
            return False, ship_cells 
    return True, ship_cells 
 
def player_attack(event, enemy_board, enemy_battlefield, 
                  player_board, player_battlefield, 
                  root, status_label, hide_ships): 
    x, y = event.x // 50, event.y // 50 
    if 0 <= x < 10 and 0 <= y < 10: 
        if enemy_board[y][x] == 1: 
            enemy_board[y][x] = 2  
            status_label.config(text="Попадание!") 
            sunk, ship_cells = is_ship_sunk(enemy_board, x, y) 
            if sunk: 
                status_label.config(text="Корабль уничтожен!") 
                check_and_paint_surroundings( 
                    enemy_board, ship_cells, enemy_battlefield 
                ) 
            display_board(enemy_battlefield, enemy_board, hide_ships) 
            if check_victory(enemy_board): 
                status_label.config(text="Игрок победил!") 
                enemy_battlefield.unbind("<Button-1>") 
                return 
        elif enemy_board[y][x] == 0: 
            enemy_board[y][x] = 3  
            status_label.config(text=" Ход компьютера") 
            display_board(enemy_battlefield, enemy_board, hide_ships) 
            enemy_battlefield.unbind("<Button-1>") 
            root.after(1000, lambda: computer_attack( 
                player_board, player_battlefield, 
                enemy_battlefield, enemy_board, 
                root, status_label, hide_ships 
            )) 
 
def computer_attack(player_board, player_battlefield, 
                    enemy_battlefield, enemy_board, 
                    root, status_label, hide_ships): 
    while True: 
        x, y = random.randint(0, 9), random.randint(0, 9) 
        if player_board[y][x] == 0: 
            player_board[y][x] = 3  
            display_board(player_battlefield, player_board) 
            status_label.config(text=" Ход игрока") 
            enemy_battlefield.bind("<Button-1>", lambda event: player_attack( 
                event, enemy_board, enemy_battlefield, 
                player_board, player_battlefield, 
                root, status_label, hide_ships 
            )) 
            break 
        elif player_board[y][x] == 1: 
            player_board[y][x] = 2 
            status_label.config(text="Попадание!") 
            sunk, ship_cells = is_ship_sunk(player_board, x, y) 
            if sunk: 
                status_label.config(text="Корабль уничтожен!") 
                check_and_paint_surroundings( 
                    player_board, ship_cells, player_battlefield 
                ) 
            display_board(player_battlefield, player_board) 
            if check_victory(player_board): 
                status_label.config(text="Компьютер победил!") 
                return 
            root.after(1000, lambda: computer_attack( 
                player_board, player_battlefield, 
                enemy_battlefield, enemy_board, 
                root, status_label, hide_ships 
            )) 
            return 
        else: 
            continue 
        break 
 
def check_surroundings(board, x, y, ship_size, orientation): 
    for i in range(ship_size): 
        if orientation == "horizontal": 
            cell_x, cell_y = x + i, y 
        else: 
            cell_x, cell_y = x, y + i 
        for dx in [-1, 0, 1]: 
            for dy in [-1, 0, 1]: 
                nx, ny = cell_x + dx, cell_y + dy 
                if (0 <= nx < 10 and 0 <= ny < 10 and 
                    board[ny][nx] == 1): 
                    return False 
    return True 
 
def toggle_ship(event, board, battlefield, remaining_label): 
    x, y = event.x // 50, event.y // 50 
    if 0 <= x < 10 and 0 <= y < 10: 
        if board[y][x] == 1: 
            ship_cells = [(y, x)] 
            i = x + 1 
            while i < 10 and board[y][i] == 1: 
                ship_cells.append((y, i)) 
                i += 1 
            i = x - 1 
            while i >= 0 and board[y][i] == 1: 
                ship_cells.append((y, i)) 
                i -= 1 
            i = y + 1 
            while i < 10 and board[i][x] == 1: 
                ship_cells.append((i, x)) 
                i += 1 
            i = y - 1 
            while i >= 0 and board[i][x] == 1: 
                ship_cells.append((i, x)) 
                i -= 1 
            ship_length = len(ship_cells) 
            for ship, size in ship_sizes.items(): 
                if ship_length == size: 
                    for cell_y, cell_x in ship_cells: 
                        board[cell_y][cell_x] = 0 
                    placed_ships[ship] -= 1 
                    break 
        else: 
            current_ship_type = None 
            for ship, size in ship_sizes.items(): 
                if placed_ships.get(ship, 0) < ships_config[ship]: 
                    current_ship_type = ship 
                    break 
            if current_ship_type is None: 
                messagebox.showinfo("Информация", "Все корабли уже размещены!") 
                return 
            ship_size = ship_sizes[current_ship_type] 
            if (current_orientation == "horizontal" and 
                x + ship_size <= 10): 
                if (all(board[y][x + i] == 0 for i in range(ship_size)) and 
                    check_surroundings(board, x, y, ship_size, "horizontal")): 
                    for i in range(ship_size): 
                        board[y][x + i] = 1 
                    placed_ships[current_ship_type] += 1 
                else: 
                    messagebox.showerror( 
                        "Ошибка", 
                        "Невозможно разместить корабль: требуется отступ в 1 клетку!" 
                    ) 
            elif (current_orientation == "vertical" and 
                  y + ship_size <= 10): 
                if (all(board[y + i][x] == 0 for i in range(ship_size)) and 
                    check_surroundings(board, x, y, ship_size, "vertical")): 
                    for i in range(ship_size): 
                        board[y + i][x] = 1 
                    placed_ships[current_ship_type] += 1 
                else: 
                    messagebox.showerror( 
                        "Ошибка", 
                        "Невозможно разместить корабль: требуется отступ в 1 клетку!" 
                    ) 
            else: 
                messagebox.showerror( 
                    "Ошибка", 
                    "Невозможно разместить корабль в данной позиции!" 
                ) 
        display_board(battlefield, board) 
        update_remaining_ships_label(remaining_label) 
 
def change_orientation(): 
    global current_orientation 
    current_orientation = ("vertical" if current_orientation == "horizontal" 
                           else "horizontal") 
 
def start_game(player_board, player_battlefield, 
               enemy_board, enemy_battlefield, 
               root, status_label, hide_ships): 
    for ship, count in ships_config.items(): 
        if placed_ships.get(ship, 0) < count: 
            messagebox.showerror( 
                "Ошибка", 
                f"Вы должны разместить все {ship} перед началом игры!" 
            ) 
            return 
    player_battlefield.unbind("<Button-1>") 
    status_label.config(text="Ход игрока") 
    display_board(enemy_battlefield, enemy_board, hide_ships=True) 
    enemy_battlefield.bind("<Button-1>", lambda event: player_attack( 
        event, enemy_board, enemy_battlefield, 
        player_board, player_battlefield, 
        root, status_label, hide_ships 
    )) 
    orientation_button.pack_forget() 
 
def start_game_with_check(player_board, player_battlefield, enemy_board, 
enemy_battlefield, root, status_label, hide_ships): 
    start_game(player_board, player_battlefield, enemy_board, enemy_battlefield, 
root, status_label, hide_ships) 
    global start_button 
    start_button.pack_forget() 
    auto_place_button.pack_forget() 
 
def reset_game(root): 
    global placed_ships, current_orientation 
    placed_ships = {ship: 0 for ship in ships_config} 
    current_orientation = "horizontal" 
    for widget in root.winfo_children(): 
        widget.destroy() 
    main(root) 
 

 
def main(root): 
    global orientation_button, start_button, auto_place_button 
    size = 10 
    player_board = [[0 for _ in range(size)] for _ in range(size)] 
    enemy_board = generate_board(size) 
    hide_ships = True 
    left_frame = tk.Frame(root) 
    left_frame.grid(row=0, column=0, padx=10, pady=10) 
    right_frame = tk.Frame(root) 
    right_frame.grid(row=0, column=2, padx=10, pady=10) 
    middle_frame = tk.Frame(root) 
    middle_frame.grid(row=0, column=1, padx=10, pady=10) 
    player_battlefield = tk.Canvas(left_frame, width=500, height=500) 
    player_battlefield.pack() 
    display_board(player_battlefield, player_board) 
    enemy_battlefield = tk.Canvas(right_frame, width=500, height=500) 
    enemy_battlefield.pack() 
    display_board(enemy_battlefield, enemy_board, hide_ships=True) 
    status_label = tk.Label( 
        middle_frame, 
        text="Расставьте свои корабли и нажмите 'Начать игру'", 
        anchor="w", width=30 
    ) 
    status_label.pack() 
    remaining_label = tk.Label(middle_frame, text="", anchor="w") 
    remaining_label.pack() 
    update_remaining_ships_label(remaining_label) 
    orientation_button = tk.Button( 
        middle_frame, text="⇄ Изменить ориентацию", 
        command=change_orientation 
    ) 
    orientation_button.pack() 
    start_button = tk.Button( 
        middle_frame, text="Начать игру", width=30, 
        command=lambda: start_game_with_check( 
            player_board, player_battlefield, 
            enemy_board, enemy_battlefield, 
            root, status_label, hide_ships 
        ) 
    ) 
    start_button.pack() 
    new_game_button = tk.Button( 
        middle_frame, text="Новая игра", width=30, 
        command=lambda: reset_game(root) 
    ) 
 
   
    player_battlefield.bind("<Button-1>", lambda event: toggle_ship( 
        event, player_board, player_battlefield, remaining_label 
    )) 
 
    for ship in ships_config: 
        placed_ships[ship] = 0 
     
 
if __name__ == "__main__": 
    root = tk.Tk() 
    root.title("Морской бой") 
    main(root) 
    root.mainloop()