
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

def draw_controller_info():
    SCREEN.fill((0, 0, 0))
    title = font.render("Controller", True, (255, 255, 255))
    wasd_info = small_font.render("Movement: WASD or Arrow Keys", True, (255, 255, 255))
    mouse_info = small_font.render("Interaction: Mouse Click (Not yet implemented)", True, (255, 255, 255))
    back_info = small_font.render("Press ESC to go back", True, (255, 255, 255))

    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    SCREEN.blit(wasd_info, (SCREEN_WIDTH // 2 - wasd_info.get_width() // 2, 250))
    SCREEN.blit(mouse_info, (SCREEN_WIDTH // 2 - mouse_info.get_width() // 2, 300))
    SCREEN.blit(back_info, (SCREEN_WIDTH // 2 - back_info.get_width() // 2, 400))
    pygame.display.flip()

def draw_settings_menu():
    SCREEN.fill((0, 0, 0))
    title = font.render("Settings", True, (255, 255, 255))
    back_info = small_font.render("Press ESC to go back", True, (255, 255, 255))

    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    SCREEN.blit(back_info, (SCREEN_WIDTH // 2 - back_info.get_width() // 2, 400))
    pygame.display.flip()

# Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_game_state == "MENU":
                if event.key == pygame.K_SPACE:
                    selected_option = menu.get_selected_option()
                    if selected_option == "Start":
                        current_game_state = "INTRO_SEQUENCE"
                        intro_sequence_active = True
                    elif selected_option == "Controller":
                        current_game_state = "CONTROLLER_INFO"
                    elif selected_option == "Settings":
                        current_game_state = "SETTINGS"
                    elif selected_option == "Exit":
                        running = False
                elif event.key == pygame.K_UP:
                    menu.navigate(-1)
                elif event.key == pygame.K_DOWN:
                    menu.navigate(1)
            elif current_game_state == "GAME_OVER" and event.key == pygame.K_r:
                current_game_state = "PLAYING"
                player.reset_position()
                ghost.reset_position()
                environment.reset_levels()
            elif event.key == pygame.K_RETURN and dialogue_box.visible:
                if dialogue_box.next_dialogue():
                    pass
            elif current_game_state == "CONTROLLER_INFO" and event.key == pygame.K_ESCAPE:
                current_game_state = "MENU"
            elif current_game_state == "SETTINGS" and event.key == pygame.K_ESCAPE:
                current_game_state = "MENU"

    if current_game_state == "MENU":
        menu.draw_menu()

    elif current_game_state == "INTRO_SEQUENCE":
        if player.rect.y > intro_target_y:
            player.rect.y -= player.speed
        else:
            if intro_sequence_active:
                dialogue_box.set_dialogues([
                    "Where am I?",
                    "This place... it feels wrong.",
                    "I need to get out of here."
                ])
                intro_sequence_active = False
            current_game_state = "PLAYING"

        SCREEN.fill((0, 0, 0))
        environment.draw(SCREEN)
        all_sprites.draw(SCREEN)
        visuals.draw_light(SCREEN, player.rect.center, light_radius)
        dialogue_box.draw()
        pygame.display.flip()

    elif current_game_state == "PLAYING":
        player.update(environment.get_current_walls())
        ghost.update(player.rect)

        # Check for level completion (e.g., all doors opened, or reaching an exit)
        # For now, let's assume reaching the top of the screen advances the level
        if player.rect.y < 50: # Example condition for level completion
            if environment.next_level():
                player.reset_position() # Reset player for new level
                ghost.reset_position() # Reset ghost for new level
            else:
                # All levels completed, maybe a win screen or restart
                current_game_state = "GAME_OVER" # For now, go to game over

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

    elif current_game_state == "CONTROLLER_INFO":
        
        draw_controller_info()

    elif current_game_state == "SETTINGS":
        draw_settings_menu()

pygame.quit()
sys.exit()


