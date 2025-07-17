import pygame
import sys
from player import Player
from audio import AudioManager
from visuals import draw_environment
from entity import Ghost
from environment import Door, check_collision

# Inisialisasi pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Objek
player = Player(100, 100)
audio_manager = AudioManager()

doors = [
    Door(300, 100, "left"),
    Door(400, 100, "center"),
    Door(500, 100, "right")
]

ghosts = [Ghost(600, 400)]

# State permainan
question_mode = False
question_answered = False
selected_path = None
correct_path = "center"
message = ""

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player.handle_movement(keys)

    screen.fill(BLACK)
    draw_environment(screen)

    for door in doors:
        door.draw(screen)

    for ghost in ghosts:
        ghost.draw(screen)

    player.draw(screen)

    if not question_mode:
        for door in doors:
            if check_collision(player, door):
                question_mode = True
                message = "Pilih jalan yang benar (Left/Center/Right)"
                break
    else:
        draw_text(message, 200, 300)

        if not question_answered:
            if keys[pygame.K_l]:
                selected_path = "left"
                question_answered = True
            elif keys[pygame.K_c]:
                selected_path = "center"
                question_answered = True
            elif keys[pygame.K_r]:
                selected_path = "right"
                question_answered = True

        if question_answered:
            if selected_path == correct_path:
                message = "Benar! Jalan terbuka."
                # Logic buka jalan
            else:
                message = "Salah! Kamu mati."
                # Logic kematian (bisa restart atau quit)

    pygame.display.flip()
    clock.tick(60)
