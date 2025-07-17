
import pygame
import sys
from player import Player
from environment import Environment
from entity import Door, Ghost
from audio import AudioManager
from visuals import Visuals
from menu import Menu
from dialogue import DialogueBox

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

# Menu setup
menu = Menu(SCREEN, font, small_font, SCREEN_WIDTH, SCREEN_HEIGHT)

# Dialogue setup
dialogue_box = DialogueBox(SCREEN, small_font, SCREEN_WIDTH, SCREEN_HEIGHT)

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

# Intro sequence variables
intro_sequence_active = False
intro_target_y = SCREEN_HEIGHT - 200 # Player moves up a bit

# Scenes
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
                current_game_state = "INTRO_SEQUENCE"
                intro_sequence_active = True
            elif current_game_state == "GAME_OVER" and event.key == pygame.K_r:
                current_game_state = "PLAYING"
                player.reset_position()
                ghost.reset_position()
            elif event.key == pygame.K_RETURN and dialogue_box.visible:
                if dialogue_box.next_dialogue():
                    # Dialogue ended, start game or next phase
                    pass # Game will continue normally after dialogue

    if current_game_state == "MENU":
        menu.draw_menu()

    elif current_game_state == "INTRO_SEQUENCE":
        if player.rect.y > intro_target_y:
            player.rect.y -= player.speed # Move player up
        else:
            if intro_sequence_active:
                dialogue_box.set_dialogues([
                    "Where am I?",
                    "This place... it feels wrong.",
                    "I need to get out of here."
                ])
                intro_sequence_active = False
            current_game_state = "PLAYING" # Transition to playing after intro movement and dialogue setup

        SCREEN.fill((0, 0, 0))
        environment.draw(SCREEN)
        all_sprites.draw(SCREEN)
        visuals.draw_light(SCREEN, player.rect.center, light_radius)
        dialogue_box.draw()
        pygame.display.flip()

    elif current_game_state == "PLAYING":
        player.update(environment.wall_list)
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
        dialogue_box.draw()
        pygame.display.flip()

    elif current_game_state == "GAME_OVER":
        draw_game_over()

pygame.quit()
sys.exit()


