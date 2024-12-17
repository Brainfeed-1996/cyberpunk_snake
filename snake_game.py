import pygame
import random
import sys
import os
import numpy as np
from pygame import mixer

# Initialisation de Pygame
pygame.init()
mixer.init()

# Constantes
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Couleurs (Thème Cyberpunk)
NEON_PINK = (255, 0, 255)
NEON_BLUE = (0, 255, 255)
NEON_GREEN = (0, 255, 0)
DARK_PURPLE = (25, 0, 51)
BLACK = (0, 0, 0)

# Configuration de la fenêtre
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Cyberpunk Snake')
clock = pygame.time.Clock()

# Chargement des sons
current_dir = os.path.dirname(os.path.abspath(__file__))
sounds_dir = os.path.join(current_dir, 'sounds')
os.makedirs(sounds_dir, exist_ok=True)

# Création des effets sonores basiques (on utilisera pygame.mixer.Sound.play())
eat_sound = mixer.Sound(os.path.join(sounds_dir, 'eat.wav')) if os.path.exists(os.path.join(sounds_dir, 'eat.wav')) else None

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-4, 0)
        self.lifetime = random.randint(20, 40)
        self.color = random.choice([NEON_PINK, NEON_BLUE, NEON_GREEN])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)

class Game:
    def __init__(self):
        self.reset()
        self.difficulty = 1
        self.particles = []

    def reset(self):
        self.snake = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.speed = 10

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            if food not in self.snake:
                return food

    def create_particles(self, x, y):
        for _ in range(20):
            self.particles.append(Particle(x * GRID_SIZE, y * GRID_SIZE))

    def update(self):
        if self.game_over:
            return

        # Mise à jour de la position du serpent
        new_head = (
            (self.snake[0][0] + self.direction[0]) % GRID_COUNT,
            (self.snake[0][1] + self.direction[1]) % GRID_COUNT
        )

        # Vérification de collision avec soi-même
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Vérification si le serpent mange la nourriture
        if new_head == self.food:
            if eat_sound:
                eat_sound.play()
            self.score += 10 * self.difficulty
            self.food = self.spawn_food()
            self.create_particles(new_head[0], new_head[1])
        else:
            self.snake.pop()

        # Mise à jour des particules
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

    def draw(self):
        screen.fill(BLACK)

        # Dessin de la grille (effet cyberpunk)
        for x in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(screen, (30, 30, 50), (x, 0), (x, WINDOW_SIZE))
        for y in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(screen, (30, 30, 50), (0, y), (WINDOW_SIZE, y))

        # Dessin du serpent
        for i, segment in enumerate(self.snake):
            color = NEON_BLUE if i == 0 else NEON_GREEN
            pygame.draw.rect(screen, color,
                           (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE,
                            GRID_SIZE-2, GRID_SIZE-2))

        # Dessin de la nourriture
        pygame.draw.rect(screen, NEON_PINK,
                        (self.food[0]*GRID_SIZE, self.food[1]*GRID_SIZE,
                         GRID_SIZE-2, GRID_SIZE-2))

        # Dessin des particules
        for particle in self.particles:
            particle.draw(screen)

        # Affichage du score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, NEON_PINK)
        screen.blit(score_text, (10, 10))

        # Affichage du niveau de difficulté
        diff_text = font.render(f'Niveau: {self.difficulty}', True, NEON_BLUE)
        screen.blit(diff_text, (10, 50))

        if self.game_over:
            game_over_text = font.render('Game Over! Appuyez sur R pour recommencer', True, NEON_PINK)
            screen.blit(game_over_text, (WINDOW_SIZE//4, WINDOW_SIZE//2))

        pygame.display.flip()

def main():
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != (0, 1):
                    game.direction = (0, -1)
                elif event.key == pygame.K_DOWN and game.direction != (0, -1):
                    game.direction = (0, 1)
                elif event.key == pygame.K_LEFT and game.direction != (1, 0):
                    game.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and game.direction != (-1, 0):
                    game.direction = (1, 0)
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    game.difficulty = event.key - pygame.K_0
                    game.speed = 10 + (game.difficulty - 1) * 5

        game.update()
        game.draw()
        clock.tick(game.speed)

if __name__ == "__main__":
    main()
