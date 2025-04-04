import pygame
import sys
import math
import random
from enum import Enum
from pygame import gfxdraw


# Constants and Enums
class ActionType(Enum):
    BUILD_AIR_DEFENSE = 1
    BUILD_LAND_DEFENSE = 2
    BUILD_SEA_DEFENSE = 3
    AIR_ATTACK = 4
    LAND_ATTACK = 5
    SEA_ATTACK = 6


class GamePhase(Enum):
    CHOOSE_ACTION = 1
    CHOOSE_TARGET = 2
    ANIMATION = 3
    GAME_OVER = 4


# Dark Color Palette
DARK_BG = (20, 20, 25)
PANEL_BG = (40, 40, 50)
TEXT_COLOR = (220, 220, 230)
SELECTION_COLOR = (180, 160, 50)
PLAYER_COLOR = (100, 140, 180)
ENEMY_COLOR = (180, 100, 100)
BUILD_COLOR = (80, 120, 80)
BUILD_HOVER = (60, 100, 60)
ATTACK_COLOR = (120, 80, 80)
ATTACK_HOVER = (100, 60, 60)
HEALTH_GOOD = (80, 140, 80)
HEALTH_WARNING = (160, 120, 60)
HEALTH_DANGER = (160, 70, 70)
CONTINENT_COLOR = (50, 60, 70)
OCEAN_COLOR = (30, 40, 50)
BUTTON_NORMAL = (70, 70, 90)
BUTTON_HOVER = (90, 90, 110)
END_TURN_COLOR = (80, 80, 100)
END_TURN_HOVER = (100, 100, 120)


class Animation:
    def __init__(self, start_pos, end_pos, anim_type, duration=60):
        self.start_pos = start_pos
        self.current_pos = list(start_pos)
        self.end_pos = end_pos
        self.anim_type = anim_type
        self.duration = duration
        self.progress = 0
        self.active = True

        # Calculate movement vector
        self.dx = (end_pos[0] - start_pos[0]) / duration
        self.dy = (end_pos[1] - start_pos[1]) / duration

    def update(self):
        if self.progress < self.duration:
            self.progress += 1
            self.current_pos[0] += self.dx
            self.current_pos[1] += self.dy
        else:
            self.active = False

    def draw(self, surface):
        if not self.active:
            return

        progress_ratio = self.progress / self.duration

        if self.anim_type == "air":
            # Missile animation
            size = max(3, 8 * (1 - progress_ratio))
            pygame.draw.circle(surface, (200, 200, 200), (int(self.current_pos[0]), int(self.current_pos[1])),
                               int(size))
            pygame.draw.circle(surface, (255, 100, 50), (int(self.current_pos[0]), int(self.current_pos[1])),
                               int(size / 2))

            # Trail
            if self.progress > 3:
                prev_pos = (
                    int(self.current_pos[0] - self.dx * 3),
                    int(self.current_pos[1] - self.dy * 3)
                )
                pygame.draw.line(surface, (255, 150, 100, 150),
                                 prev_pos,
                                 (int(self.current_pos[0]), int(self.current_pos[1])), 2)

        elif self.anim_type == "land":
            # Soldier animation
            pygame.draw.circle(surface, (150, 150, 150), (int(self.current_pos[0]), int(self.current_pos[1])), 5)

            # Rifle
            angle = math.atan2(self.dy, self.dx)
            end_x = self.current_pos[0] + math.cos(angle) * 10
            end_y = self.current_pos[1] + math.sin(angle) * 10
            pygame.draw.line(surface, (100, 100, 100),
                             (int(self.current_pos[0]), int(self.current_pos[1])),
                             (int(end_x), int(end_y)), 3)

        elif self.anim_type == "sea":
            # Boat animation
            angle = math.atan2(self.dy, self.dx)

            # Hull
            hull_points = [
                (self.current_pos[0] + math.cos(angle) * 10, self.current_pos[1] + math.sin(angle) * 10),
                (self.current_pos[0] + math.cos(angle + math.pi / 2) * 5,
                 self.current_pos[1] + math.sin(angle + math.pi / 2) * 5),
                (self.current_pos[0] + math.cos(angle - math.pi / 2) * 5,
                 self.current_pos[1] + math.sin(angle - math.pi / 2) * 5)
            ]
            pygame.draw.polygon(surface, (120, 100, 80), hull_points)

            # Mast
            mast_top = (
                self.current_pos[0] - math.cos(angle) * 5,
                self.current_pos[1] - math.sin(angle) * 5
            )
            pygame.draw.line(surface, (80, 60, 40),
                             (int(self.current_pos[0]), int(self.current_pos[1])),
                             (int(mast_top[0]), int(mast_top[1])), 2)

        elif self.anim_type == "shield":
            # Shield defense animation
            alpha = min(255, 255 * (1 - progress_ratio * 2))
            shield_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (100, 150, 255, alpha), (20, 20), 15 + 5 * math.sin(progress_ratio * 10))
            pygame.draw.circle(shield_surface, (200, 220, 255, alpha), (20, 20), 10 + 3 * math.sin(progress_ratio * 10),
                               2)
            surface.blit(shield_surface, (int(self.current_pos[0] - 20), int(self.current_pos[1] - 20)))


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=TEXT_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, (60, 60, 70), self.rect, 2, border_radius=6)

        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


class City:
    def __init__(self, name, position, is_player=False):
        self.name = name
        self.position = position
        self.is_player = is_player
        self.health = 100
        self.air_defense = 0
        self.land_defense = 0
        self.sea_defense = 0
        self.attacks_remaining = 1
        self.builds_remaining = 1
        self.radius = 18
        self.shield_anim = None

    def perform_action(self, action, target=None):
        if action in [ActionType.BUILD_AIR_DEFENSE, ActionType.BUILD_LAND_DEFENSE, ActionType.BUILD_SEA_DEFENSE]:
            if self.builds_remaining <= 0:
                return False

            self.builds_remaining -= 1
            if action == ActionType.BUILD_AIR_DEFENSE:
                self.air_defense += 10
            elif action == ActionType.BUILD_LAND_DEFENSE:
                self.land_defense += 10
            elif action == ActionType.BUILD_SEA_DEFENSE:
                self.sea_defense += 10

            # Create shield animation
            self.shield_anim = Animation(self.position, self.position, "shield", 30)
            return True

        elif action in [ActionType.AIR_ATTACK, ActionType.LAND_ATTACK, ActionType.SEA_ATTACK] and target:
            if self.attacks_remaining <= 0:
                return False

            self.attacks_remaining -= 1
            damage = 25  # Base damage

            if action == ActionType.AIR_ATTACK:
                damage -= target.air_defense
                anim_type = "air"
            elif action == ActionType.LAND_ATTACK:
                damage -= target.land_defense
                anim_type = "land"
            elif action == ActionType.SEA_ATTACK:
                damage -= target.sea_defense
                anim_type = "sea"

            damage = max(5, damage)  # Minimum damage
            target.health -= damage

            # Create attack animation
            return Animation(self.position, target.position, anim_type)

        return False

    def reset_turn(self):
        self.attacks_remaining = 1
        self.builds_remaining = 1


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1400, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("World War Strategy Game")

        # Fonts
        self.font = pygame.font.SysFont('Segoe UI', 20)
        self.title_font = pygame.font.SysFont('Segoe UI', 26, bold=True)
        self.small_font = pygame.font.SysFont('Segoe UI', 16)

        # Game state
        self.cities = [
            City("Washington", (250, 320)),
            City("London", (600, 250)),
            City("Tokyo", (1050, 330), is_player=True),
            City("Beijing", (980, 310)),
            City("Moscow", (700, 230)),
        ]

        self.current_turn = 0
        self.game_phase = GamePhase.CHOOSE_ACTION
        self.selected_action = None
        self.message = ""
        self.message_timer = 0
        self.animations = []

        # UI Elements
        self.action_panel_width = 300
        self.map_width = self.WIDTH - self.action_panel_width

        # Action buttons
        panel_height = self.HEIGHT
        button_start_y = panel_height - 350

        self.action_buttons = [
            Button(20, button_start_y + 180, 260, 45, "Air Attack", ATTACK_COLOR, ATTACK_HOVER),
            Button(20, button_start_y + 235, 260, 45, "Land Attack", ATTACK_COLOR, ATTACK_HOVER),
            Button(20, button_start_y + 290, 260, 45, "Sea Attack", ATTACK_COLOR, ATTACK_HOVER),
            Button(20, button_start_y + 20, 260, 45, "Build Air Defense", BUILD_COLOR, BUILD_HOVER),
            Button(20, button_start_y + 75, 260, 45, "Build Land Defense", BUILD_COLOR, BUILD_HOVER),
            Button(20, button_start_y + 130, 260, 45, "Build Sea Defense", BUILD_COLOR, BUILD_HOVER)
        ]

        self.end_turn_button = Button(self.WIDTH - 150, self.HEIGHT - 70, 120, 50, "End Turn",
                                      END_TURN_COLOR, END_TURN_HOVER)

    def show_message(self, msg, duration=120):
        self.message = msg
        self.message_timer = duration

    def draw_map(self):
        # Draw ocean background
        self.screen.fill(OCEAN_COLOR)

        # Draw continents
        continents = [
            [(150, 200), (350, 170), (450, 230), (430, 400), (200, 400)],  # NA
            [(350, 400), (450, 500), (300, 550)],  # SA
            [(550, 200), (750, 170), (850, 230), (750, 330), (550, 280)],  # Europe
            [(550, 280), (750, 330), (850, 480), (650, 550), (550, 450)],  # Africa
            [(750, 170), (1150, 200), (1050, 350), (850, 400)],  # Asia
            [(950, 450), (1050, 470), (1100, 550), (1000, 570)]  # Australia
        ]

        for continent in continents:
            pygame.draw.polygon(self.screen, CONTINENT_COLOR, continent)
            pygame.draw.polygon(self.screen, (70, 80, 90), continent, 3)

    def draw_cities(self):
        for city in self.cities:
            if city.health <= 0:
                continue

            color = PLAYER_COLOR if city.is_player else ENEMY_COLOR

            # Draw city
            pygame.draw.circle(self.screen, color, city.position, city.radius)
            pygame.draw.circle(self.screen, (60, 60, 70), city.position, city.radius, 2)

            # Draw health bar
            bar_width = 50
            health_width = max(0, (city.health / 100) * bar_width)
            health_rect = pygame.Rect(city.position[0] - 25, city.position[1] - 35, bar_width, 6)
            pygame.draw.rect(self.screen, (60, 60, 70), health_rect, 1)

            if city.health > 60:
                health_color = HEALTH_GOOD
            elif city.health > 30:
                health_color = HEALTH_WARNING
            else:
                health_color = HEALTH_DANGER

            pygame.draw.rect(self.screen, health_color,
                             (city.position[0] - 25, city.position[1] - 35, health_width, 6))

            # Draw city name with subtle background
            name_text = self.small_font.render(city.name, True, TEXT_COLOR)
            name_pos = (city.position[0] - name_text.get_width() // 2, city.position[1] + city.radius + 5)

            text_bg = pygame.Rect(
                name_pos[0] - 5,
                name_pos[1] - 2,
                name_text.get_width() + 10,
                name_text.get_height() + 4
            )
            pygame.draw.rect(self.screen, (50, 50, 60, 200), text_bg, border_radius=3)
            pygame.draw.rect(self.screen, (70, 70, 80), text_bg, 1, border_radius=3)
            self.screen.blit(name_text, name_pos)

            # Draw shield animation if active
            if city.shield_anim and city.shield_anim.active:
                city.shield_anim.draw(self.screen)
                city.shield_anim.update()

    def draw_action_panel(self):
        # Panel background
        panel_rect = pygame.Rect(self.map_width, 0, self.action_panel_width, self.HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
        pygame.draw.rect(self.screen, (60, 60, 70), panel_rect, 2)

        # Draw title with divider
        title_text = self.title_font.render("Actions", True, TEXT_COLOR)
        self.screen.blit(title_text, (self.map_width + 30, 30))
        pygame.draw.line(self.screen, (70, 70, 80),
                         (self.map_width + 20, 70),
                         (self.WIDTH - 20, 70), 2)

        # Draw current city info
        current_city = self.cities[self.current_turn % len(self.cities)]
        city_title = self.font.render(f"{current_city.name}", True, TEXT_COLOR)
        self.screen.blit(city_title, (self.map_width + 30, 100))

        # Health indicator
        health_text = self.small_font.render(f"Health: {current_city.health}/100", True, TEXT_COLOR)
        self.screen.blit(health_text, (self.map_width + 30, 130))

        # Defense indicators
        defenses = [
            f"Air Defense: {current_city.air_defense}",
            f"Land Defense: {current_city.land_defense}",
            f"Sea Defense: {current_city.sea_defense}"
        ]

        for i, defense in enumerate(defenses):
            text = self.small_font.render(defense, True, TEXT_COLOR)
            self.screen.blit(text, (self.map_width + 40, 160 + i * 25))

        # Draw action buttons
        for button in self.action_buttons:
            button.draw(self.screen, self.font)

        # Draw end turn button
        self.end_turn_button.draw(self.screen, self.font)

    def draw_turn_indicator(self):
        current_city = self.cities[self.current_turn % len(self.cities)]
        turn_text = self.title_font.render(
            f"{current_city.name}'s Turn" + (" (YOU)" if current_city.is_player else " (Enemy)"),
            True, TEXT_COLOR
        )

        # Indicator background
        indicator_bg = pygame.Rect(
            20,
            20,
            turn_text.get_width() + 40,
            turn_text.get_height() + 20
        )

        color = (60, 80, 100) if current_city.is_player else (100, 60, 70)
        pygame.draw.rect(self.screen, color, indicator_bg, border_radius=10)
        pygame.draw.rect(self.screen, (80, 80, 90), indicator_bg, 2, border_radius=10)

        self.screen.blit(turn_text, (40, 35))

    def draw_message(self):
        if self.message and self.message_timer > 0:
            msg_text = self.font.render(self.message, True, TEXT_COLOR)

            # Message box
            msg_rect = pygame.Rect(
                self.WIDTH // 2 - msg_text.get_width() // 2 - 15,
                self.HEIGHT - 70,
                msg_text.get_width() + 30,
                40
            )

            pygame.draw.rect(self.screen, (60, 60, 80), msg_rect, border_radius=5)
            pygame.draw.rect(self.screen, (80, 80, 100), msg_rect, 2, border_radius=5)
            self.screen.blit(msg_text, (self.WIDTH // 2 - msg_text.get_width() // 2, self.HEIGHT - 60))

    def draw_animations(self):
        for anim in self.animations[:]:
            anim.draw(self.screen)
            anim.update()
            if not anim.active:
                self.animations.remove(anim)

    def handle_player_turn(self, mouse_pos, mouse_click):
        current_city = self.cities[self.current_turn % len(self.cities)]

        if self.game_phase == GamePhase.CHOOSE_ACTION:
            # Check action buttons (note reversed order now)
            for i, button in enumerate(self.action_buttons):
                if button.is_clicked(mouse_pos, mouse_click):
                    # Adjusted action mapping due to reordered buttons
                    action_mapping = [
                        ActionType.AIR_ATTACK,
                        ActionType.LAND_ATTACK,
                        ActionType.SEA_ATTACK,
                        ActionType.BUILD_AIR_DEFENSE,
                        ActionType.BUILD_LAND_DEFENSE,
                        ActionType.BUILD_SEA_DEFENSE
                    ]
                    action = action_mapping[i]

                    if action in [ActionType.AIR_ATTACK, ActionType.LAND_ATTACK, ActionType.SEA_ATTACK]:
                        self.selected_action = action
                        self.game_phase = GamePhase.CHOOSE_TARGET
                        self.show_message(f"Select target for {action.name.replace('_', ' ')}")
                    else:
                        if current_city.perform_action(action):
                            self.show_message(f"Built {action.name.replace('BUILD_', '').replace('_', ' ')}!")
                        else:
                            self.show_message("Cannot build now!")

            # Check end turn button
            if self.end_turn_button.is_clicked(mouse_pos, mouse_click):
                self.end_turn()

        elif self.game_phase == GamePhase.CHOOSE_TARGET:
            if mouse_click and mouse_pos[0] < self.map_width:
                for city in self.cities:
                    if city != current_city and city.health > 0:
                        distance = math.sqrt((mouse_pos[0] - city.position[0]) ** 2 +
                                             (mouse_pos[1] - city.position[1]) ** 2)
                        if distance < city.radius + 5:
                            anim = current_city.perform_action(self.selected_action, city)
                            if anim:
                                self.animations.append(anim)
                                self.game_phase = GamePhase.ANIMATION
                                damage = 25  # Base damage
                                if self.selected_action == ActionType.AIR_ATTACK:
                                    damage -= city.air_defense
                                elif self.selected_action == ActionType.LAND_ATTACK:
                                    damage -= city.land_defense
                                elif self.selected_action == ActionType.SEA_ATTACK:
                                    damage -= city.sea_defense

                                self.show_message(
                                    f"Attacked {city.name} with {self.selected_action.name.replace('_', ' ')} " +
                                    f"for {max(5, damage)} damage!"
                                )
                            else:
                                self.show_message("Cannot attack now!")
                            break

    def cpu_turn(self):
        current_city = self.cities[self.current_turn % len(self.cities)]

        # Simple AI: 50% chance to attack, 50% to build
        import random
        if random.random() < 0.5 and current_city.attacks_remaining > 0:
            # Find target (attack weakest city)
            targets = [c for c in self.cities if c != current_city and c.health > 0]
            if targets:
                target = min(targets, key=lambda x: x.health)
                attack_type = random.choice([
                    ActionType.AIR_ATTACK,
                    ActionType.LAND_ATTACK,
                    ActionType.SEA_ATTACK
                ])
                anim = current_city.perform_action(attack_type, target)
                if anim:
                    self.animations.append(anim)
                    self.game_phase = GamePhase.ANIMATION
                self.show_message(
                    f"{current_city.name} launched {attack_type.name.replace('_', ' ')} on {target.name}!")

        elif current_city.builds_remaining > 0:
            # Build random defense
            build_type = random.choice([
                ActionType.BUILD_AIR_DEFENSE,
                ActionType.BUILD_LAND_DEFENSE,
                ActionType.BUILD_SEA_DEFENSE
            ])
            current_city.perform_action(build_type)
            self.show_message(f"{current_city.name} built {build_type.name.replace('BUILD_', '').replace('_', ' ')}!")

        if self.game_phase != GamePhase.ANIMATION:
            self.end_turn()

    def end_turn(self):
        self.cities[self.current_turn % len(self.cities)].reset_turn()
        self.selected_action = None
        self.current_turn += 1
        self.game_phase = GamePhase.CHOOSE_ACTION

        # Check for winners
        remaining_players = sum(1 for city in self.cities if city.is_player and city.health > 0)
        remaining_enemies = sum(1 for city in self.cities if not city.is_player and city.health > 0)

        if remaining_players == 0:
            self.show_message("GAME OVER - You lost!", 300)
            self.game_phase = GamePhase.GAME_OVER
        elif remaining_enemies == 0:
            self.show_message("VICTORY - You won!", 300)
            self.game_phase = GamePhase.GAME_OVER

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True

            # Update button hover states
            if self.game_phase == GamePhase.CHOOSE_ACTION:
                for button in self.action_buttons:
                    button.check_hover(mouse_pos)
                self.end_turn_button.check_hover(mouse_pos)

            # Game logic
            current_city = self.cities[self.current_turn % len(self.cities)]

            if self.message_timer > 0:
                self.message_timer -= 1

            # Handle turns
            if current_city.health > 0:
                if current_city.is_player and self.game_phase != GamePhase.GAME_OVER:
                    if self.game_phase == GamePhase.ANIMATION and not self.animations:
                        self.game_phase = GamePhase.CHOOSE_ACTION
                    elif self.game_phase != GamePhase.ANIMATION:
                        self.handle_player_turn(mouse_pos, mouse_click)
                elif not current_city.is_player and self.game_phase == GamePhase.CHOOSE_ACTION:
                    pygame.time.delay(1000)  # Pause for player to see CPU turn
                    self.cpu_turn()

            # Drawing
            self.draw_map()
            self.draw_cities()
            self.draw_animations()
            self.draw_action_panel()
            self.draw_turn_indicator()
            self.draw_message()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()