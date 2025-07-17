
import pygame
import sys
import random
from player import Player
from environment import Environment
from entity import Entity
from audio import AudioManager
from visuals import Visuals

# Initialize Pygame
pygame.init()

# Audio Manager
audio_manager = AudioManager()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minimal Horror Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game states
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2

current_game_state = GAME_STATE_MENU

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# Player setup
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Environment setup
environment = Environment()

# Entity setup
entity = Entity(100, 100) # Initial position for the entity
all_sprites.add(entity)

# Visuals setup
visuals = Visuals(SCREEN_WIDTH, SCREEN_HEIGHT)
light_radius = 150 # Initial light radius

def draw_menu():
    SCREEN.fill(BLACK)
    title_text = font.render("Minimal Horror Game", True, WHITE)
    start_text = small_font.render("Press SPACE to Start", True, WHITE)
    SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    SCREEN.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

def draw_game_over():
    SCREEN.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    restart_text = small_font.render("Press R to Restart", True, WHITE)
    SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    SCREEN.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if current_game_state == GAME_STATE_MENU:
                if event.key == pygame.K_SPACE:
                    current_game_state = GAME_STATE_PLAYING
            elif current_game_state == GAME_STATE_GAME_OVER:
                if event.key == pygame.K_r:
                    current_game_state = GAME_STATE_PLAYING # Reset game state to playing
                    player.rect.x = SCREEN_WIDTH // 2 # Reset player position
                    player.rect.y = SCREEN_HEIGHT // 2
                    entity.rect.x = 100 # Reset entity position
                    entity.rect.y = 100

    if current_game_state == GAME_STATE_MENU:
        draw_menu()
    elif current_game_state == GAME_STATE_PLAYING:
        # Update
        player.update()
        entity.update(player.rect)

        # Play random sounds
        if random.randint(0, 500) == 0:
            audio_manager.play_sound("whisper")
        if random.randint(0, 300) == 0:
            audio_manager.play_sound("creak")

        # Collision detection for player and walls
        for wall in environment.wall_list:
            if player.rect.colliderect(wall.rect):
                # Simple collision response: move player back
                if player.rect.x < wall.rect.x:
                    player.rect.right = wall.rect.left
                if player.rect.x > wall.rect.x:
                    player.rect.left = wall.rect.right
                if player.rect.y < wall.rect.y:
                    player.rect.bottom = wall.rect.top
                if player.rect.y > wall.rect.y:
                    player.rect.top = wall.rect.bottom

        # Collision detection for player and entity
        if pygame.sprite.collide_rect(player, entity):
            current_game_state = GAME_STATE_GAME_OVER

        # Draw
        SCREEN.fill(BLACK)
        environment.draw(SCREEN)
        all_sprites.draw(SCREEN)
        visuals.draw_light(SCREEN, player.rect.center, light_radius)
        pygame.display.flip()

    elif current_game_state == GAME_STATE_GAME_OVER:
        draw_game_over()

pygame.quit()
sys.exit()


