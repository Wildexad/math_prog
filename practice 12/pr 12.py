import pygame
import random
import math
import os

# Инициализация Pygame
pygame.init()

# Размеры игрового окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Настройки игры
FPS = 60
ROCKET_RELOAD_TIME = 500  # Время перезарядки ракет (в миллисекундах)
EXPLOSION_DURATION = 300  # Длительность взрыва (в миллисекундах)
ENERGY_REGEN_TIME = 1000  # Время восстановления энергии (в миллисекундах)
MAX_ROCKETS = 5  # Максимальное количество выстрелов

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра: Звездолет и кометы")
clock = pygame.time.Clock()

# Загрузка изображений
starship_img = pygame.image.load("starship.png")
rocket_img = pygame.image.load("rocket.png")
comet_img = pygame.image.load("comet.png")
explosion_img = pygame.image.load("explosion.png")
asteroid_img = pygame.image.load("asteroid.png")
bonus_img = pygame.image.load("bonus.png")

# Загрузка звуков
explosion_sound = pygame.mixer.Sound("explosion.wav")
shoot_sound = pygame.mixer.Sound("shoot.wav")
bonus_sound = pygame.mixer.Sound("bonus.wav")

# Масштабирование изображений
starship_img = pygame.transform.scale(starship_img, (50, 50))
rocket_img = pygame.transform.scale(rocket_img, (10, 30))
comet_img = pygame.transform.scale(comet_img, (50, 50))
explosion_img = pygame.transform.scale(explosion_img, (60, 60))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
bonus_img = pygame.transform.scale(bonus_img, (30, 30))

# Путь к файлу с рекордами
HIGHSCORES_FILE = "highscores.txt"

# Функция для сохранения рекордов
def save_highscore(score):
    if os.path.exists(HIGHSCORES_FILE):
        with open(HIGHSCORES_FILE, "r") as f:
            highscores = [int(line.strip()) for line in f.readlines()]
    else:
        highscores = []

    highscores.append(score)
    highscores.sort(reverse=True)
    highscores = highscores[:5]

    with open(HIGHSCORES_FILE, "w") as f:
        for score in highscores:
            f.write(f"{score}\n")

# Функция для чтения рекордов
def read_highscores():
    if os.path.exists(HIGHSCORES_FILE):
        with open(HIGHSCORES_FILE, "r") as f:
            highscores = [int(line.strip()) for line in f.readlines()]
    else:
        highscores = []
    return highscores

# Игровой объект: звездолет
class Starship:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.speed = 5
        self.energy = MAX_ROCKETS
        self.last_energy_regen_time = pygame.time.get_ticks()
        self.last_shoot_time = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed

    def draw(self):
        screen.blit(starship_img, (self.x, self.y))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.energy > 0 and current_time - self.last_shoot_time >= ROCKET_RELOAD_TIME:
            self.energy -= 1
            self.last_shoot_time = current_time
            shoot_sound.play()
            return Rocket(self.x + self.width // 2 - 5, self.y)
        return None

    def regenerate_energy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_energy_regen_time > ENERGY_REGEN_TIME:
            if self.energy < MAX_ROCKETS:
                self.energy += 1
            self.last_energy_regen_time = current_time

# Игровой объект: ракета
class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.active = True

    def move(self):
        self.y -= self.speed
        if self.y < 0:
            self.active = False

    def draw(self):
        if self.active:
            screen.blit(rocket_img, (self.x, self.y))

# Игровой объект: комета
class Comet:
    def __init__(self, speed, size):
        self.x = random.randint(0, SCREEN_WIDTH - 50)
        self.y = random.randint(-100, -30)
        self.speed = speed
        self.size = size

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(comet_img, (self.x, self.y))

# Игровой объект: астероид
class Asteroid:
    def __init__(self, speed):
        self.x = random.randint(0, SCREEN_WIDTH - 50)
        self.y = random.randint(-100, -30)
        self.speed = speed
        self.size = 50

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(asteroid_img, (self.x, self.y))

# Игровой объект: бонус
class Bonus:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - 30)
        self.y = random.randint(-100, -30)
        self.size = 30
        self.active = True

    def move(self):
        self.y += 3  # Скорость падения бонусов

    def draw(self):
        if self.active:
            screen.blit(bonus_img, (self.x, self.y))

# Игровой объект: взрыв
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()

    def draw(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < EXPLOSION_DURATION:
            screen.blit(explosion_img, (self.x - 10, self.y - 10))
            return True
        return False

# Проверка столкновений
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Функция для отображения таблицы рекордов
def show_highscores():
    highscores = read_highscores()
    font = pygame.font.Font(None, 36)
    
    screen.fill(WHITE)
    title_text = font.render("Таблица рекордов", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    y_offset = 100
    for i, score in enumerate(highscores):
        score_text = font.render(f"{i+1}. {score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 40
    
    back_text = font.render("Нажмите Esc для выхода", True, BLACK)
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, y_offset + 20))
    
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

# Основной игровой цикл
def main():
    running = True
    starship = Starship()
    rockets = []
    comets = []
    asteroids = []
    bonuses = []
    explosions = []
    score = 0
    last_rocket_time = 0
    last_comet_time = 0
    last_asteroid_time = 0
    last_bonus_time = 0

    comet_speed = 3
    comet_spawn_time = 2000
    comet_size = 50
    asteroid_speed = 3
    bonus_spawn_time = 5000

    while running:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление звездолетом
        starship.move(keys)

        # Стрельба ракетами
        if keys[pygame.K_SPACE]:
            rocket = starship.shoot()
            if rocket:
                rockets.append(rocket)

        # Регенерация энергии
        starship.regenerate_energy()

        # Спавн комет
        current_time = pygame.time.get_ticks()
        if current_time - last_comet_time > comet_spawn_time:
            comets.append(Comet(comet_speed, comet_size))
            last_comet_time = current_time

        # Спавн астероидов
        if current_time - last_asteroid_time > 3000:
            asteroids.append(Asteroid(asteroid_speed))
            last_asteroid_time = current_time

        # Спавн бонусов
        if current_time - last_bonus_time > bonus_spawn_time:
            bonuses.append(Bonus())
            last_bonus_time = current_time

        # Обновление и рисование объектов
        for rocket in rockets[:]:
            rocket.move()
            if not rocket.active:
                rockets.remove(rocket)
            rocket.draw()

        for comet in comets[:]:
            comet.move()
            if comet.y > SCREEN_HEIGHT:
                comets.remove(comet)
            comet.draw()

            comet_rect = pygame.Rect(comet.x, comet.y, comet.size, comet.size)
            for rocket in rockets[:]:
                rocket_rect = pygame.Rect(rocket.x, rocket.y, 10, 30)
                if check_collision(comet_rect, rocket_rect):
                    rockets.remove(rocket)
                    comets.remove(comet)
                    explosions.append(Explosion(comet.x, comet.y))
                    explosion_sound.play()
                    score += 1
                    break

            starship_rect = pygame.Rect(starship.x, starship.y, starship.width, starship.height)
            if check_collision(comet_rect, starship_rect):
                print("Game Over! Final Score:", score)
                save_highscore(score)
                show_highscores()
                running = False

        for asteroid in asteroids[:]:
            asteroid.move()
            if asteroid.y > SCREEN_HEIGHT:
                asteroids.remove(asteroid)
            asteroid.draw()

            asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.size, asteroid.size)
            if check_collision(asteroid_rect, starship_rect):
                print("Game Over! Final Score:", score)
                save_highscore(score)
                show_highscores()
                running = False

        for bonus in bonuses[:]:
            bonus.move()
            if bonus.y > SCREEN_HEIGHT:
                bonuses.remove(bonus)
            bonus.draw()

            bonus_rect = pygame.Rect(bonus.x, bonus.y, bonus.size, bonus.size)
            if check_collision(bonus_rect, starship_rect):
                bonuses.remove(bonus)
                score += 5
                bonus_sound.play()

        for explosion in explosions[:]:
            if not explosion.draw():
                explosions.remove(explosion)

        starship.draw()

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        energy_text = font.render(f"Energy: {starship.energy}/{MAX_ROCKETS}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(energy_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
