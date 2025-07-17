import pygame
import sys
from player import Player
from environment import Environment
from entity import Door, Ghost
from audio import AudioManager
from visuals import Visuals

# Init
pygame.init()
audio_manager = AudioManager()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Horror Game")

# State
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)
current_game_state = "MENU"

# Player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
all_sprites = pygame.sprite.Group(player)

# Game objects
doors = [
    Door("left", 150, 100, correct=False),
    Door("center", 350, 100, correct=True),
    Door("right", 550, 100, correct=False)
]
all_sprites.add(*doors)

ghost = Ghost(100, 100)
all_sprites.add(ghost)

environment = Environment()
visuals = Visuals(SCREEN_WIDTH, SCREEN_HEIGHT)
light_radius = 150

# Scenes
def draw_menu():
    SCREEN.fill((0, 0, 0))
    title = font.render("Horror Game", True, (255, 255, 255))
    start = small_font.render("Press SPACE to Start", True, (255, 255, 255))
    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 250))
    SCREEN.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, 350))
    pygame.display.flip()

def draw_game_over():
    SCREEN.fill((0, 0, 0))
    text = font.render("YOU DIED", True, (255, 0, 0))
    restart = small_font.render("Press R to Restart", True, (255, 255, 255))
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    SCREEN.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 350))
    pygame.display.flip()

# Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_game_state == "MENU" and event.key == pygame.K_SPACE:
                current_game_state = "PLAYING"
            elif current_game_state == "GAME_OVER" and event.key == pygame.K_r:
                current_game_state = "PLAYING"
                player.reset_position()
                ghost.reset_position()

    if current_game_state == "MENU":
        draw_menu()

    elif current_game_state == "PLAYING":
        player.update()
        ghost.update(player.rect)

        for door in doors:
            if player.rect.colliderect(door.rect):
                if door.correct:
                    doors.remove(door)
                    all_sprites.remove(door)
                    break
                else:
                    audio_manager.play_sound("scream")
                    current_game_state = "GAME_OVER"

        SCREEN.fill((0, 0, 0))
        environment.draw(SCREEN)
        all_sprites.draw(SCREEN)
        visuals.draw_light(SCREEN, player.rect.center, light_radius)
        pygame.display.flip()

    elif current_game_state == "GAME_OVER":
        draw_game_over()

pygame.quit()
sys.exit()
