
import math
import random
import time
import turtle


NUM_PARTICIPANTS = random.randint(3, 4)  
CIRCLE_RADIUS = 100
TURTLE_OFFSET = 10  
TOTAL_LAPS = 1 
STEP_DELAY = 0.001  

def create_participants(num):
    participants = []
    colors = ["red", "blue", "green", "orange", "purple"]
    for i in range(num):
        participant = {
            "name": f"Участник {i + 1}",
            "angle": 0, 
            "speed": random.uniform(1, 3),  
            "direction": 1,  
            "laps": 0,  
            "color": colors[i % len(colors)],  
            "turtle": None  
        }
        participants.append(participant)
    return participants

participants = create_participants(NUM_PARTICIPANTS)

def setup_screen():
    screen = turtle.Screen()
    screen.title("Circular Race Simulation")
    screen.bgcolor("white")
    screen.setup(width=600, height=600)
    return screen


def draw_track():
    track_drawer = turtle.Turtle()
    track_drawer.hideturtle()
    track_drawer.penup()
    track_drawer.goto(0, -CIRCLE_RADIUS)
    track_drawer.pendown()
    track_drawer.circle(CIRCLE_RADIUS)
    track_drawer.penup()
    track_drawer.goto(0, -(CIRCLE_RADIUS + 20))  
    track_drawer.pendown()
    track_drawer.circle(CIRCLE_RADIUS + 20)


def draw_track():
    track_drawer = turtle.Turtle()
    track_drawer.hideturtle()
    track_drawer.penup()
    track_drawer.goto(0, -CIRCLE_RADIUS)
    track_drawer.pendown()
    track_drawer.circle(CIRCLE_RADIUS)
    track_drawer.penup()
    track_drawer.goto(0, -(CIRCLE_RADIUS + 20))  
    track_drawer.pendown()
    track_drawer.circle(CIRCLE_RADIUS + 20)

   
    track_drawer.penup()
    start_x, start_y = calculate_coordinates(0, CIRCLE_RADIUS)  
    track_drawer.goto(start_x - 10, start_y)  
    track_drawer.setheading(0) 
    track_drawer.pendown()
    track_drawer.forward(40) 

def setup_turtles(participants):
    for participant in participants:
        t = turtle.Turtle()
        t.shape("turtle")
        t.color(participant["color"])
        t.penup()
        x, y = calculate_coordinates(participant["angle"], CIRCLE_RADIUS + TURTLE_OFFSET)
        t.goto(x, y) 
        t.setheading(participant["angle"] * 180 / math.pi)
        participant["turtle"] = t


def update_position(participant):
    
    participant["angle"] += participant["direction"] * participant["speed"] / CIRCLE_RADIUS


    if participant["angle"] < 0:
        participant["angle"] += 2 * math.pi
    elif participant["angle"] >= 2 * math.pi:
        participant["angle"] -= 2 * math.pi
        participant["laps"] += 1  


    x, y = calculate_coordinates(participant["angle"], CIRCLE_RADIUS + TURTLE_OFFSET)
    participant["turtle"].goto(x, y)
    participant["turtle"].setheading(participant["angle"] * 180 / math.pi)

def calculate_coordinates(angle, radius):
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y


def check_finish(participant):
   
    if participant["angle"] < 0.1 and participant["laps"] == TOTAL_LAPS:
        return True
    return False

def print_status(participants):
    print("\nСтатус гонки:")
    for participant in participants:
        x, y = calculate_coordinates(participant["angle"], CIRCLE_RADIUS)
        print(f"{participant['name']}: Позиции ({x:.2f}, {y:.2f}), Круг: {participant['laps']}")


def display_final_standings(participants):
    
    participants.sort(key=lambda p: (-p["laps"], -p["angle"]))

   
    results_turtle = turtle.Turtle()
    results_turtle.hideturtle()
    results_turtle.penup()
    results_turtle.goto(-200, 200)
    results_turtle.write("Результаты:", align="left", font=("Arial", 16, "bold"))

    for i, participant in enumerate(participants):
        results_turtle.goto(-200, 200 - (i + 1) * 30)
        results_turtle.write(
            f"{i + 1}. {participant['name']} - Круг: {participant['laps']}", 
            align="left", 
            font=("Arial", 14, "normal")
        )

 
    print("\nГонка окончена! Результаты:")
    for i, participant in enumerate(participants):
        print(f"{i + 1}. {participant['name']} - Laps: {participant['laps']}")

def determine_leader(participants):
    leader = max(participants, key=lambda p: (p["laps"], p["angle"]))
    return leader

def display_leader(leader):
    leader_turtle.clear()
    leader_turtle.write(
        f"Лидер : {leader['name']}",
        align="center",
        font=("Arial", 16, "bold")
    )


def run_race(participants):
    print("Начало гонки!\n")

    global leader_turtle  
    screen = setup_screen()
    draw_track()
    setup_turtles(participants)

   
    leader_turtle = turtle.Turtle()
    leader_turtle.hideturtle()
    leader_turtle.penup()
    leader_turtle.goto(0, 250) 

    finished = False
    while not finished:
        for participant in participants:
            if participant["laps"] < TOTAL_LAPS:
                update_position(participant)

                
                if random.randint(1, 10) == 1:  
                    participant["speed"] = random.uniform(1, 3)

               
                if check_finish(participant):
                    finished = True
                    break

        leader = determine_leader(participants)
        display_leader(leader)

        print_status(participants)
        time.sleep(STEP_DELAY)


    display_final_standings(participants)

    screen.mainloop()

run_race(participants)
