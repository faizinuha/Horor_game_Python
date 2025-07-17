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
<<<<<<< HEAD

    def update(self, walls=None):
        old_x, old_y = self.rect.x, self.rect.y

=======

    def update(self, walls=None):
        dx, dy = 0, 0
>>>>>>> 521db75eeebef683aef995afc4fd1073e78d107c
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: dx = -self.speed
        if keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_UP]: dy = -self.speed
        if keys[pygame.K_DOWN]: dy = self.speed

        # Move horizontally and check for collisions
        self.rect.x += dx
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0:  # Moving right, hit the left side of the wall
                        self.rect.right = wall.rect.left
                    elif dx < 0:  # Moving left, hit the right side of the wall
                        self.rect.left = wall.rect.right

        # Move vertically and check for collisions
        self.rect.y += dy
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dy > 0:  # Moving down, hit the top side of the wall
                        self.rect.bottom = wall.rect.top
                    elif dy < 0:  # Moving up, hit the bottom side of the wall
                        self.rect.top = wall.rect.bottom

<<<<<<< HEAD
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

=======
>>>>>>> 521db75eeebef683aef995afc4fd1073e78d107c
    def reset_position(self):
        self.rect.center = (self.original_x, self.original_y)


