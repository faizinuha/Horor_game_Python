import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((200, 200, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.original_x = x
        self.original_y = y

    def update(self, walls=None):
        old_x, old_y = self.rect.x, self.rect.y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed

        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    # If collision, revert to old position
                    self.rect.x = old_x
                    self.rect.y = old_y
                    # Then try to move only in one direction and check again
                    # Horizontal movement check
                    if keys[pygame.K_LEFT]: self.rect.x -= self.speed
                    if keys[pygame.K_RIGHT]: self.rect.x += self.speed
                    for wall_h in walls:
                        if self.rect.colliderect(wall_h.rect):
                            self.rect.x = old_x
                            break
                    
                    # Vertical movement check
                    if keys[pygame.K_UP]: self.rect.y -= self.speed
                    if keys[pygame.K_DOWN]: self.rect.y += self.speed
                    for wall_v in walls:
                        if self.rect.colliderect(wall_v.rect):
                            self.rect.y = old_y
                            break

    def reset_position(self):
        self.rect.center = (self.original_x, self.original_y)


