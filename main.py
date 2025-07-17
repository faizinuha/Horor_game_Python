import pygame
from audio import AudioManager
from player import Player
from entity import Ghost
from environment import Environment

pygame.init()

# Window setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Horor Game - Jalan Tiga Takdir")

# Font
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (180, 0, 0)

# Game states
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
GAME_STATE_CHOICE = 3

current_game_state = GAME_STATE_MENU

# Audio
try:
    audio_manager = AudioManager()
    audio_manager.play_music("bg_music.mp3")
except Exception as e:
    print(f"[WARNING] Audio disabled: {e}")

# Player & Entities
player = Player()
entity = Ghost()
environment = Environment()

clock = pygame.time.Clock()
running = True

def draw_text(text, x, y, size=36, color=WHITE):
    f = pygame.font.SysFont("Arial", size)
    t = f.render(text, True, color)
    SCREEN.blit(t, (x, y))

def draw_menu():
    SCREEN.fill(BLACK)
    draw_text("👻 HOROR GAME - PILIH JALANMU", 120, 100)
    draw_text("Tekan [SPACE] untuk mulai", 220, 300, 28)
    pygame.display.flip()

def draw_game_over():
    SCREEN.fill(BLACK)
    draw_text("💀 GAME OVER 💀", 280, 200, 48, RED)
    draw_text("Tekan [R] untuk kembali ke menu", 180, 350, 24)
    pygame.display.flip()

def draw_choice():
    SCREEN.fill(BLACK)
    draw_text("⚠️ Persimpangan Jalan ⚠️", 240, 100)
    draw_text("Pilih arah yang benar untuk melanjutkan...", 140, 160, 24)
    draw_text("1. Kiri (←)", 300, 250, 28)
    draw_text("2. Tengah (↑)", 300, 310, 28)
    draw_text("3. Kanan (→)", 300, 370, 28)
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if current_game_state == GAME_STATE_MENU:
                if event.key == pygame.K_SPACE:
                    current_game_state = GAME_STATE_PLAYING
                    player.rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

            elif current_game_state == GAME_STATE_GAME_OVER:
                if event.key == pygame.K_r:
                    current_game_state = GAME_STATE_MENU

            elif current_game_state == GAME_STATE_CHOICE:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    try: audio_manager.play_sound("death.mp3")
                    except: pass
                    current_game_state = GAME_STATE_GAME_OVER
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    current_game_state = GAME_STATE_PLAYING
                    player.rect.x = SCREEN_WIDTH // 2
                    player.rect.y = SCREEN_HEIGHT - 80
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    try: audio_manager.play_sound("scream.mp3")
                    except: pass
                    current_game_state = GAME_STATE_GAME_OVER

    if current_game_state == GAME_STATE_MENU:
        draw_menu()

    elif current_game_state == GAME_STATE_PLAYING:
        player.update()
        entity.update(player.rect)
        environment.update()

        SCREEN.fill((30, 30, 30))
        environment.draw(SCREEN)
        player.draw(SCREEN)
        entity.draw(SCREEN)
        pygame.display.flip()

        # Trigger persimpangan di lokasi tertentu
        if player.rect.y < 100:
            current_game_state = GAME_STATE_CHOICE

    elif current_game_state == GAME_STATE_CHOICE:
        draw_choice()

    elif current_game_state == GAME_STATE_GAME_OVER:
        draw_game_over()

    clock.tick(60)

pygame.quit()
