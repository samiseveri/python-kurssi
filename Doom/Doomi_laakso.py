import pygame
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HALF_HEIGHT = SCREEN_HEIGHT // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)

# Game settings
FOV = math.pi / 3  # Field of view (60 degrees)
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
CELL_SIZE = 64
PLAYER_SPEED = 5
ROTATION_SPEED = 0.05

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyDoom")
clock = pygame.time.Clock()

# Game map (1 = wall, 0 = empty space)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

MAP_WIDTH = len(MAP[0]) * CELL_SIZE
MAP_HEIGHT = len(MAP) * CELL_SIZE

# Player settings
player_x = CELL_SIZE * 1.5
player_y = CELL_SIZE * 1.5
player_angle = 0


# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.speed = 1
        self.health = 100
        self.color = RED

    def update(self, player_x, player_y):
        # Simple AI: move toward player
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            dx /= dist
            dy /= dist

            # Check if path to player is clear (very simple)
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed

            cell_x, cell_y = int(new_x // CELL_SIZE), int(new_y // CELL_SIZE)
            if 0 <= cell_x < len(MAP[0]) and 0 <= cell_y < len(MAP):
                if MAP[cell_y][cell_x] == 0:
                    self.x = new_x
                    self.y = new_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


# Create some enemies
enemies = [
    Enemy(CELL_SIZE * 5.5, CELL_SIZE * 5.5),
    Enemy(CELL_SIZE * 2.5, CELL_SIZE * 6.5)
]

# Weapon settings
weapon_img = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.rect(weapon_img, (150, 150, 150), (20, 40, 60, 20))
pygame.draw.rect(weapon_img, (100, 100, 100), (30, 30, 40, 10))
weapon_rect = weapon_img.get_rect()
weapon_rect.centerx = SCREEN_WIDTH // 2
weapon_rect.bottom = SCREEN_HEIGHT - 20

shooting = False
shot_frame = 0


# Raycasting function
def cast_ray(angle):
    # Normalize angle
    angle %= 2 * math.pi

    # Ray direction
    ray_cos = math.cos(angle)
    ray_sin = math.sin(angle)

    # Vertical check
    v_depth = 0
    v_x = 0
    v_y = 0

    if ray_cos > 0.001:  # Looking right
        v_x = (int(player_x / CELL_SIZE) + 1) * CELL_SIZE
        v_y = player_y + (v_x - player_x) * (ray_sin / ray_cos)
        x_step = CELL_SIZE
        y_step = x_step * (ray_sin / ray_cos)
    elif ray_cos < -0.001:  # Looking left
        v_x = (int(player_x / CELL_SIZE)) * CELL_SIZE - 0.0001
        v_y = player_y + (v_x - player_x) * (ray_sin / ray_cos)
        x_step = -CELL_SIZE
        y_step = x_step * (ray_sin / ray_cos)
    else:  # Looking straight up or down
        v_depth = MAX_DEPTH
        v_x = player_x
        v_y = player_y

    if abs(ray_cos) > 0.001:
        while v_depth < MAX_DEPTH:
            cell_x = int(v_x / CELL_SIZE)
            cell_y = int(v_y / CELL_SIZE)

            if 0 <= cell_x < len(MAP[0]) and 0 <= cell_y < len(MAP):
                if MAP[cell_y][cell_x] == 1:
                    v_depth = math.sqrt((v_x - player_x) ** 2 + (v_y - player_y) ** 2)
                    break

                v_x += x_step
                v_y += y_step
                v_depth = MAX_DEPTH
            else:
                v_depth = MAX_DEPTH
                break

    # Horizontal check
    h_depth = 0
    h_x = 0
    h_y = 0

    if ray_sin > 0.001:  # Looking down
        h_y = (int(player_y / CELL_SIZE) + 1) * CELL_SIZE
        h_x = player_x + (h_y - player_y) * (ray_cos / ray_sin)
        y_step = CELL_SIZE
        x_step = y_step * (ray_cos / ray_sin)
    elif ray_sin < -0.001:  # Looking up
        h_y = (int(player_y / CELL_SIZE)) * CELL_SIZE - 0.0001
        h_x = player_x + (h_y - player_y) * (ray_cos / ray_sin)
        y_step = -CELL_SIZE
        x_step = y_step * (ray_cos / ray_sin)
    else:  # Looking straight left or right
        h_depth = MAX_DEPTH
        h_x = player_x
        h_y = player_y

    if abs(ray_sin) > 0.001:
        while h_depth < MAX_DEPTH:
            cell_x = int(h_x / CELL_SIZE)
            cell_y = int(h_y / CELL_SIZE)

            if 0 <= cell_x < len(MAP[0]) and 0 <= cell_y < len(MAP):
                if MAP[cell_y][cell_x] == 1:
                    h_depth = math.sqrt((h_x - player_x) ** 2 + (h_y - player_y) ** 2)
                    break

                h_x += x_step
                h_y += y_step
                h_depth = MAX_DEPTH
            else:
                h_depth = MAX_DEPTH
                break

    # Return the closest wall
    if v_depth < h_depth:
        return v_depth, v_x, v_y, 'v'
    else:
        return h_depth, h_x, h_y, 'h'


# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                shooting = True
                shot_frame = 5

    # Handle continuous key presses
    keys = pygame.key.get_pressed()

    # Rotate player
    if keys[K_LEFT]:
        player_angle -= ROTATION_SPEED
    if keys[K_RIGHT]:
        player_angle += ROTATION_SPEED

    # Move player
    move_x = 0
    move_y = 0

    if keys[K_w]:  # Forward
        move_x += math.cos(player_angle) * PLAYER_SPEED
        move_y += math.sin(player_angle) * PLAYER_SPEED
    if keys[K_s]:  # Backward
        move_x -= math.cos(player_angle) * PLAYER_SPEED
        move_y -= math.sin(player_angle) * PLAYER_SPEED
    if keys[K_a]:  # Strafe left
        move_x += math.cos(player_angle - math.pi / 2) * PLAYER_SPEED
        move_y += math.sin(player_angle - math.pi / 2) * PLAYER_SPEED
    if keys[K_d]:  # Strafe right
        move_x += math.cos(player_angle + math.pi / 2) * PLAYER_SPEED
        move_y += math.sin(player_angle + math.pi / 2) * PLAYER_SPEED

    # Check collision
    new_x = player_x + move_x
    new_y = player_y + move_y

    cell_x = int(new_x / CELL_SIZE)
    cell_y = int(new_y / CELL_SIZE)

    if 0 <= cell_x < len(MAP[0]) and 0 <= cell_y < len(MAP):
        if MAP[cell_y][cell_x] == 0:
            player_x = new_x
            player_y = new_y

    # Update enemies
    for enemy in enemies:
        enemy.update(player_x, player_y)

    # Handle shooting
    if shooting:
        shot_frame -= 1
        if shot_frame <= 0:
            shooting = False

            # Check if we hit an enemy
            for enemy in enemies[:]:
                # Simple hit detection
                dx = enemy.x - player_x
                dy = enemy.y - player_y
                dist = math.sqrt(dx * dx + dy * dy)

                angle_to_enemy = math.atan2(dy, dx)
                angle_diff = (angle_to_enemy - player_angle) % (2 * math.pi)
                if angle_diff > math.pi:
                    angle_diff -= 2 * math.pi

                if abs(angle_diff) < 0.2 and dist < 200:
                    enemy.health -= 50
                    if enemy.health <= 0:
                        enemies.remove(enemy)

    # Clear screen
    screen.fill(BLACK)

    # Draw ceiling
    pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, HALF_HEIGHT))

    # Draw floor
    pygame.draw.rect(screen, BROWN, (0, HALF_HEIGHT, SCREEN_WIDTH, HALF_HEIGHT))

    # Raycasting - ALWAYS CAST RAYS (not just when shooting)
    ray_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        depth, ray_x, ray_y, wall_type = cast_ray(ray_angle)

        # Fix fish-eye effect
        depth *= math.cos(player_angle - ray_angle)

        # Calculate wall height
        wall_height = (CELL_SIZE * SCREEN_HEIGHT) / (depth + 0.0001)
        if wall_height > SCREEN_HEIGHT:
            wall_height = SCREEN_HEIGHT

        # Draw wall slice
        wall_x = ray * (SCREEN_WIDTH / NUM_RAYS)
        wall_y = (SCREEN_HEIGHT - wall_height) / 2

        # Color based on wall type and distance
        if wall_type == 'v':
            color = (max(0, 255 - depth * 0.5), 0, 0)  # Vertical walls (red)
        else:
            color = (max(0, 200 - depth * 0.5), 0, 0)  # Horizontal walls (darker red)

        pygame.draw.rect(screen, color, (wall_x, wall_y, (SCREEN_WIDTH / NUM_RAYS) + 1, wall_height))

        ray_angle += FOV / NUM_RAYS

    # Draw weapon
    if shooting:
        # Draw muzzle flash
        pygame.draw.circle(screen, (255, 255, 0),
                           (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100), 20 + shot_frame * 5)

    screen.blit(weapon_img, weapon_rect)

    # Draw minimap (for debugging)
    map_scale = 0.2
    for y in range(len(MAP)):
        for x in range(len(MAP[0])):
            if MAP[y][x] == 1:
                pygame.draw.rect(screen, WHITE,
                                 (x * CELL_SIZE * map_scale, y * CELL_SIZE * map_scale,
                                  CELL_SIZE * map_scale, CELL_SIZE * map_scale))

    # Draw player on minimap
    pygame.draw.circle(screen, GREEN,
                       (int(player_x * map_scale), int(player_y * map_scale)), 5)

    # Draw player direction
    end_x = player_x * map_scale + math.cos(player_angle) * 20
    end_y = player_y * map_scale + math.sin(player_angle) * 20
    pygame.draw.line(screen, GREEN,
                     (player_x * map_scale, player_y * map_scale),
                     (end_x, end_y), 2)

    # Draw enemies on minimap
    for enemy in enemies:
        pygame.draw.circle(screen, RED,
                           (int(enemy.x * map_scale), int(enemy.y * map_scale)),
                           int(enemy.size * map_scale))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()