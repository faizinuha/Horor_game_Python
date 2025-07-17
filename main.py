import pygame
import sys
import random
from player import Player
from environment import Environment
from entity import NPC, QuestGiver, Item, Chest
from audio import AudioManager
from visuals import Visuals
from menu import Menu
from dialogue import DialogueBox
from quest_system import QuestSystem

# Init
pygame.init()
audio_manager = AudioManager()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Adventure")

# State
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
current_game_state = "MENU"

# Menu setup
menu = Menu(SCREEN, font, small_font, SCREEN_WIDTH, SCREEN_HEIGHT, audio_manager)

# Dialogue setup
dialogue_box = DialogueBox(SCREEN, small_font, SCREEN_WIDTH, SCREEN_HEIGHT)

# Quest system
quest_system = QuestSystem()

# Player
player = Player(100, 500)
all_sprites = pygame.sprite.Group(player)

# NPCs
npcs = pygame.sprite.Group()

# Village NPCs
village_elder = QuestGiver("Elder", 200, 200, [
    "Welcome to our village, young adventurer!",
    "We have been troubled by monsters lately...",
    "Could you help us by collecting 5 herbs from the forest?",
    "They grow near the old oak trees."
], "collect_herbs", {"herbs": 5})

blacksmith = NPC("Blacksmith", 400, 180, [
    "I can forge you better weapons!",
    "Bring me some iron ore and I'll make you a sword.",
    "The mines are to the east of here."
])

merchant = NPC("Merchant", 600, 220, [
    "Welcome to my shop!",
    "I have potions and supplies for your journey.",
    "Come back when you have some gold!"
])

forest_guide = NPC("Guide", 150, 350, [
    "The forest can be dangerous at night.",
    "Watch out for the wolves!",
    "Stay on the path and you'll be safe."
])

# Wandering NPCs
villager1 = NPC("Villager", 300, 300, [
    "Good day, traveler!",
    "The weather has been lovely lately.",
    "I hope you enjoy your stay in our village."
])

villager2 = NPC("Farmer", 500, 400, [
    "My crops are growing well this season.",
    "The soil here is very fertile.",
    "Would you like to buy some vegetables?"
])

child_npc = NPC("Child", 250, 450, [
    "Have you seen my ball?",
    "I was playing near the well...",
    "Mom says not to talk to strangers, but you look nice!"
])

old_woman = NPC("Old Woman", 450, 300, [
    "Back in my day, this village was much smaller.",
    "So many new faces these days...",
    "Be careful out there, young one."
])
npcs.add(village_elder, blacksmith, merchant, forest_guide, villager1, villager2, child_npc, old_woman)
all_sprites.add(npcs)

# Items and collectibles
items = pygame.sprite.Group()
# Add some herbs for the quest
for i in range(8):
    herb_x = random.randint(100, 700)
    herb_y = random.randint(100, 500)
    herb = Item("herb", herb_x, herb_y)
    items.add(herb)

# Add some coins
for i in range(5):
    coin_x = random.randint(150, 650)
    coin_y = random.randint(150, 450)
    coin = Item("coin", coin_x, coin_y)
    items.add(coin)

# Add chests
chest1 = Chest(350, 500, [{"type": "coin", "amount": 10}, {"type": "potion", "amount": 1}])
chest2 = Chest(550, 350, [{"type": "herb", "amount": 3}])
items.add(chest1, chest2)

all_sprites.add(items)

environment = Environment()
visuals = Visuals(SCREEN_WIDTH, SCREEN_HEIGHT)

# Cutscene variables
cutscene_active = False
cutscene_step = 0
cutscene_timer = 0
cutscene_texts = [
    "Long ago, in a peaceful village...",
    "A young adventurer arrived seeking glory...",
    "Little did they know what awaited them...",
    "Your adventure begins now!"
]

# Game variables
camera_x = 0
camera_y = 0

def draw_game_over():
    SCREEN.fill((20, 20, 40))
    text = font.render("GAME OVER", True, (255, 100, 100))
    restart = small_font.render("Press R to Restart", True, (255, 255, 255))
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
    SCREEN.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 350))
    pygame.display.flip()

def draw_controller_info():
    SCREEN.fill((20, 40, 60))
    title = font.render("Controls", True, (255, 255, 255))
    wasd_info = small_font.render("Movement: WASD or Arrow Keys", True, (255, 255, 255))
    interact_info = small_font.render("Interact with NPCs: SPACE (when near)", True, (255, 255, 255))
    quest_info = small_font.render("View Quests: Q", True, (255, 255, 255))
    inventory_info = small_font.render("Inventory: I", True, (255, 255, 255))
    back_info = small_font.render("Press ESC to go back", True, (255, 255, 255))

    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    SCREEN.blit(wasd_info, (SCREEN_WIDTH // 2 - wasd_info.get_width() // 2, 200))
    SCREEN.blit(interact_info, (SCREEN_WIDTH // 2 - interact_info.get_width() // 2, 240))
    SCREEN.blit(quest_info, (SCREEN_WIDTH // 2 - quest_info.get_width() // 2, 280))
    SCREEN.blit(inventory_info, (SCREEN_WIDTH // 2 - inventory_info.get_width() // 2, 320))
    SCREEN.blit(back_info, (SCREEN_WIDTH // 2 - back_info.get_width() // 2, 400))
    pygame.display.flip()

def draw_settings_menu():
    SCREEN.fill((40, 20, 60))
    title = font.render("Settings", True, (255, 255, 255))
    volume_info = small_font.render(f"Volume: {int(audio_manager.volume * 100)}%", True, (255, 255, 255))
    volume_controls = small_font.render("Use +/- to adjust volume", True, (200, 200, 200))
    graphics_info = small_font.render("Graphics: Pixel Perfect", True, (255, 255, 255))
    back_info = small_font.render("Press ESC to go back", True, (255, 255, 255))

    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    SCREEN.blit(volume_info, (SCREEN_WIDTH // 2 - volume_info.get_width() // 2, 220))
    SCREEN.blit(volume_controls, (SCREEN_WIDTH // 2 - volume_controls.get_width() // 2, 250))
    SCREEN.blit(graphics_info, (SCREEN_WIDTH // 2 - graphics_info.get_width() // 2, 320))
    SCREEN.blit(back_info, (SCREEN_WIDTH // 2 - back_info.get_width() // 2, 400))
    pygame.display.flip()

def draw_cutscene():
    SCREEN.fill((10, 10, 20))
    
    # Draw a simple scene background
    pygame.draw.rect(SCREEN, (34, 139, 34), (0, 400, SCREEN_WIDTH, 200))  # Grass
    pygame.draw.circle(SCREEN, (255, 255, 0), (700, 100), 50)  # Sun
    
    # Draw village silhouette
    pygame.draw.rect(SCREEN, (101, 67, 33), (200, 300, 80, 100))  # House 1
    pygame.draw.polygon(SCREEN, (139, 69, 19), [(200, 300), (240, 250), (280, 300)])  # Roof 1
    pygame.draw.rect(SCREEN, (101, 67, 33), (350, 320, 100, 80))  # House 2
    pygame.draw.polygon(SCREEN, (139, 69, 19), [(350, 320), (400, 270), (450, 320)])  # Roof 2
    
    # Draw player walking
    player_x = 50 + (cutscene_timer * 2) % (SCREEN_WIDTH - 100)
    pygame.draw.rect(SCREEN, (100, 150, 255), (player_x, 450, 20, 30))  # Player body
    pygame.draw.circle(SCREEN, (255, 220, 177), (player_x + 10, 440), 8)  # Player head
    
    # Draw text
    if cutscene_step < len(cutscene_texts):
        text = small_font.render(cutscene_texts[cutscene_step], True, (255, 255, 255))
        text_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, 100)
        pygame.draw.rect(SCREEN, (0, 0, 0, 128), text_rect)
        pygame.draw.rect(SCREEN, (255, 255, 255), text_rect, 2)
        SCREEN.blit(text, (text_rect.x + 10, text_rect.y + 10))
    
    skip_text = small_font.render("Press SPACE to skip", True, (200, 200, 200))
    SCREEN.blit(skip_text, (SCREEN_WIDTH - skip_text.get_width() - 20, SCREEN_HEIGHT - 40))
    
    pygame.display.flip()

def check_npc_interaction():
    for npc in npcs:
        distance = ((player.rect.centerx - npc.rect.centerx) ** 2 + 
                   (player.rect.centery - npc.rect.centery) ** 2) ** 0.5
        if distance < 60:  # Interaction range
            return npc
    return None

def check_item_pickup():
    for item in items:
        distance = ((player.rect.centerx - item.rect.centerx) ** 2 + 
                   (player.rect.centery - item.rect.centery) ** 2) ** 0.5
        if distance < 40:  # Pickup range
            return item
    return None

def draw_quest_log():
    SCREEN.fill((20, 20, 40))
    title = font.render("Quest Log", True, (255, 255, 255))
    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
    
    y_offset = 150
    active_quests = quest_system.get_active_quests()
    
    if not active_quests:
        no_quests = small_font.render("No active quests", True, (150, 150, 150))
        SCREEN.blit(no_quests, (SCREEN_WIDTH // 2 - no_quests.get_width() // 2, y_offset))
    else:
        for quest in active_quests:
            quest_text = small_font.render(f"• {quest['name']}", True, (255, 255, 100))
            SCREEN.blit(quest_text, (100, y_offset))
            
            desc_text = small_font.render(quest['description'], True, (200, 200, 200))
            SCREEN.blit(desc_text, (120, y_offset + 30))
            
            # Show progress
            if quest['type'] == 'collect':
                progress = quest_system.get_quest_progress(quest['id'])
                target = sum(quest['requirements'].values())
                progress_text = small_font.render(f"Progress: {progress}/{target}", True, (150, 255, 150))
                SCREEN.blit(progress_text, (120, y_offset + 60))
            
            y_offset += 120
    
    back_info = small_font.render("Press Q to close", True, (255, 255, 255))
    SCREEN.blit(back_info, (SCREEN_WIDTH // 2 - back_info.get_width() // 2, SCREEN_HEIGHT - 50))
    pygame.display.flip()

# Main game loop
running = True
clock = pygame.time.Clock()
show_quest_log = False

while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_game_state == "MENU":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    selected_option = menu.get_selected_option()
                    if selected_option == "Start":
                        current_game_state = "CUTSCENE"
                        cutscene_active = True
                        cutscene_step = 0
                        cutscene_timer = 0
                        audio_manager.play_sound("menu_select")
                    elif selected_option == "Controller":
                        current_game_state = "CONTROLLER_INFO"
                    elif selected_option == "Settings":
                        current_game_state = "SETTINGS"
                    elif selected_option == "Exit":
                        running = False
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    menu.navigate(-1)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    menu.navigate(1)
            
            elif current_game_state == "CUTSCENE":
                if event.key == pygame.K_SPACE:
                    if cutscene_step < len(cutscene_texts) - 1:
                        cutscene_step += 1
                        cutscene_timer = 0
                    else:
                        current_game_state = "PLAYING"
                        cutscene_active = False
            
            elif current_game_state == "PLAYING":
                if event.key == pygame.K_SPACE and not dialogue_box.visible:
                    nearby_npc = check_npc_interaction()
                    if nearby_npc:
                        dialogue_box.set_dialogues(nearby_npc.dialogues)
                        audio_manager.play_sound("talk")
                        if isinstance(nearby_npc, QuestGiver) and not quest_system.has_quest(nearby_npc.quest_id):
                            quest_system.add_quest(nearby_npc.quest_id, nearby_npc.quest_name, 
                                                 nearby_npc.quest_description, nearby_npc.quest_requirements)
                    else:
                        # Check for item pickup
                        nearby_item = check_item_pickup()
                        if nearby_item:
                            quest_system.add_item_to_inventory(nearby_item.item_type)
                            audio_manager.play_sound("item_pickup")
                            items.remove(nearby_item)
                            all_sprites.remove(nearby_item)
                
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN] and dialogue_box.visible:
                    dialogue_box.next_dialogue()
                
                elif event.key == pygame.K_q:
                    show_quest_log = not show_quest_log
                
                elif event.key == pygame.K_i:
                    # TODO: Implement inventory
                    pass
            
            elif current_game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    current_game_state = "PLAYING"
                    player.reset_position()
                    environment.reset_levels()
            
            elif current_game_state == "CONTROLLER_INFO":
                if event.key == pygame.K_ESCAPE:
                    current_game_state = "MENU"
            
            elif current_game_state == "SETTINGS":
                if event.key == pygame.K_ESCAPE:
                    current_game_state = "MENU"
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    audio_manager.adjust_volume(0.1)
                elif event.key == pygame.K_MINUS:
                    audio_manager.adjust_volume(-0.1)

    # Update game state
    if current_game_state == "MENU":
        menu.draw_menu()

    elif current_game_state == "CUTSCENE":
        cutscene_timer += dt
        if cutscene_timer > 3000:  # 3 seconds per text
            if cutscene_step < len(cutscene_texts) - 1:
                cutscene_step += 1
                cutscene_timer = 0
            else:
                current_game_state = "PLAYING"
                cutscene_active = False
        draw_cutscene()

    elif current_game_state == "PLAYING":
        if show_quest_log:
            draw_quest_log()
        else:
            # Only update if dialogue is not visible
            if not dialogue_box.visible:
                all_walls = environment.get_current_walls()
                player.update(all_walls)
                
                # Update wandering NPCs
                for npc in npcs:
                    if hasattr(npc, 'update'):
                        npc.update()
                
                # Simple camera follow
                camera_x = player.rect.centerx - SCREEN_WIDTH // 2
                camera_y = player.rect.centery - SCREEN_HEIGHT // 2
                camera_x = max(0, min(camera_x, 1600 - SCREEN_WIDTH))  # Limit camera
                camera_y = max(0, min(camera_y, 1200 - SCREEN_HEIGHT))

            # Draw everything
            SCREEN.fill((34, 139, 34))  # Grass background
            
            # Draw environment with camera offset
            environment.draw(SCREEN, camera_x, camera_y)
            
            # Draw sprites with camera offset
            for sprite in all_sprites:
                screen_x = sprite.rect.x - camera_x
                screen_y = sprite.rect.y - camera_y
                SCREEN.blit(sprite.image, (screen_x, screen_y))
            
            # Draw UI elements
            visuals.draw_ui_elements(SCREEN, 100, 50)
            
            # Draw minimap
            npc_positions = [(npc.rect.centerx, npc.rect.centery) for npc in npcs]
            visuals.draw_minimap(SCREEN, (player.rect.centerx, player.rect.centery), npc_positions)
            
            # Draw interaction prompt
            if not dialogue_box.visible:
                nearby_npc = check_npc_interaction()
                if nearby_npc:
                    prompt = small_font.render("Press SPACE to talk", True, (255, 255, 255))
                    prompt_rect = prompt.get_rect()
                    prompt_rect.centerx = SCREEN_WIDTH // 2
                    prompt_rect.y = 50
                    pygame.draw.rect(SCREEN, (0, 0, 0, 128), prompt_rect.inflate(20, 10))
                    SCREEN.blit(prompt, prompt_rect)
                else:
                    nearby_item = check_item_pickup()
                    if nearby_item:
                        prompt = small_font.render(f"Press SPACE to pick up {nearby_item.item_type}", True, (255, 255, 255))
                        prompt_rect = prompt.get_rect()
                        prompt_rect.centerx = SCREEN_WIDTH // 2
                        prompt_rect.y = 50
                        pygame.draw.rect(SCREEN, (0, 0, 0, 128), prompt_rect.inflate(20, 10))
                        SCREEN.blit(prompt, prompt_rect)
            
            dialogue_box.draw()
            
            # Draw UI
            quest_hint = small_font.render("Press Q for quests", True, (200, 200, 200))
            SCREEN.blit(quest_hint, (10, 10))
            
            pygame.display.flip()

    elif current_game_state == "GAME_OVER":
        draw_game_over()

    elif current_game_state == "CONTROLLER_INFO":
        draw_controller_info()

    elif current_game_state == "SETTINGS":
        draw_settings_menu()

pygame.quit()
sys.exit()