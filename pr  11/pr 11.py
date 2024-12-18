import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60
ROCKET_RELOAD_TIME = 500 
MAX_ROCKETS = 3
COMET_SPAWN_TIME = 2000 
EXPLOSION_DURATION = 200 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра: Звездолет и кометы")
clock = pygame.time.Clock()

starship_img = pygame.image.load("starship.png")
rocket_img = pygame.image.load("rocket.png")
comet_img = pygame.image.load("comet.png")
explosion_img = pygame.image.load("explosion.png")

starship_img = pygame.transform.scale(starship_img, (50, 50))
rocket_img = pygame.transform.scale(rocket_img, (10, 30))
comet_img = pygame.transform.scale(comet_img, (50, 50))
explosion_img = pygame.transform.scale(explosion_img, (100  , 60))

class Starship:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.speed = 5

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

class Comet:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - 50)
        self.y = random.randint(-100, -30)
        self.speed = random.randint(3, 6)
        self.size = 50

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(comet_img, (self.x, self.y))

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

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def main():
    running = True
    starship = Starship()
    rockets = []
    comets = []
    explosions = []
    score = 0
    last_rocket_time = 0
    last_comet_time = 0

    while running:
        screen.fill(WHITE) 
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

 
        starship.move(keys)


        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if len(rockets) < MAX_ROCKETS and current_time - last_rocket_time > ROCKET_RELOAD_TIME:
                rockets.append(Rocket(starship.x + starship.width // 2 - 5, starship.y))
                last_rocket_time = current_time


        current_time = pygame.time.get_ticks()
        if current_time - last_comet_time > COMET_SPAWN_TIME:
            comets.append(Comet())
            last_comet_time = current_time

  
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
                    score += 1
                    break

            starship_rect = pygame.Rect(starship.x, starship.y, starship.width, starship.height)
            if check_collision(comet_rect, starship_rect):
                print("Game Over! Final Score:", score)
                running = False

        for explosion in explosions[:]:
            if not explosion.draw():
                explosions.remove(explosion)

        starship.draw()

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)  # Черный текст
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
