import pygame
import sys
import random
import math
from enum import Enum


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
    GAME_OVER = 3


# Color Palette
DARK_BG = (20, 20, 25)
PANEL_BG = (40, 40, 50)
TEXT_COLOR = (220, 220, 230)
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
            return True

        elif action in [ActionType.AIR_ATTACK, ActionType.LAND_ATTACK, ActionType.SEA_ATTACK] and target:
            if self.attacks_remaining <= 0:
                return False

            self.attacks_remaining -= 1
            damage = 25  # Base damage

            if action == ActionType.AIR_ATTACK:
                damage -= target.air_defense
            elif action == ActionType.LAND_ATTACK:
                damage -= target.land_defense
            elif action == ActionType.SEA_ATTACK:
                damage -= target.sea_defense

            damage = max(5, damage)  # Minimum damage
            target.health -= damage
            return True

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
        self.title_font = pygame.font.SysFont('Segoe UI', 24, bold=True)
        self.small_font = pygame.font.SysFont('Segoe UI', 16)

        # Game state
        self.cities = [
            City("Washington", (250, 320)),
            City("London", (500, 250)),
            City("Tokyo", (900, 330), is_player=True),
            City("Beijing", (800, 310)),
            City("Moscow", (600, 230)),
        ]

        self.current_turn = 0
        self.game_phase = GamePhase.CHOOSE_ACTION
        self.selected_action = None
        self.message = ""
        self.message_timer = 0

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

    def get_next_active_city_index(self, start_index):
        """Find the next city that is still alive (health > 0)"""
        num_cities = len(self.cities)
        for i in range(1, num_cities + 1):
            index = (start_index + i) % num_cities
            if self.cities[index].health > 0:
                return index
        return None  # All cities are dead (shouldn't happen as game would end first)

    def draw_map(self):
        self.screen.fill(OCEAN_COLOR)
        continents = [
            [(150, 200), (350, 170), (450, 230), (430, 400), (200, 400)],
            [(350, 400), (450, 500), (300, 550)],
            [(550, 200), (750, 170), (850, 230), (750, 330), (550, 280)],
            [(550, 280), (750, 330), (850, 480), (650, 550), (550, 450)],
            [(750, 170), (1100, 200), (1000, 350), (850, 400)],
            [(950, 450), (1050, 470), (1100, 550), (1000, 570)]
        ]
        for continent in continents:
            pygame.draw.polygon(self.screen, CONTINENT_COLOR, continent)
            pygame.draw.polygon(self.screen, (70, 80, 90), continent, 3)

    def draw_cities(self):
        for city in self.cities:
            if city.health <= 0:
                continue

            color = PLAYER_COLOR if city.is_player else ENEMY_COLOR
            pygame.draw.circle(self.screen, color, city.position, city.radius)
            pygame.draw.circle(self.screen, (60, 60, 70), city.position, city.radius, 2)

            # Health bar
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

            # City name
            name_text = self.small_font.render(city.name, True, TEXT_COLOR)
            name_pos = (city.position[0] - name_text.get_width() // 2, city.position[1] + city.radius + 5)
            text_bg = pygame.Rect(name_pos[0] - 5, name_pos[1] - 2,
                                  name_text.get_width() + 10, name_text.get_height() + 4)
            pygame.draw.rect(self.screen, (50, 50, 60), text_bg, border_radius=3)
            pygame.draw.rect(self.screen, (70, 70, 80), text_bg, 1, border_radius=3)
            self.screen.blit(name_text, name_pos)

    def draw_action_panel(self):
        panel_rect = pygame.Rect(self.map_width, 0, self.action_panel_width, self.HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
        pygame.draw.rect(self.screen, (60, 60, 70), panel_rect, 2)

        title_text = self.title_font.render("Actions", True, TEXT_COLOR)
        self.screen.blit(title_text, (self.map_width + 30, 30))
        pygame.draw.line(self.screen, (70, 70, 80),
                         (self.map_width + 20, 70),
                         (self.WIDTH - 20, 70), 2)

        current_city = self.cities[self.current_turn % len(self.cities)]
        city_title = self.font.render(f"{current_city.name}", True, TEXT_COLOR)
        self.screen.blit(city_title, (self.map_width + 30, 100))

        health_text = self.small_font.render(f"Health: {current_city.health}/100", True, TEXT_COLOR)
        self.screen.blit(health_text, (self.map_width + 30, 130))

        defenses = [
            f"Air Defense: {current_city.air_defense}",
            f"Land Defense: {current_city.land_defense}",
            f"Sea Defense: {current_city.sea_defense}"
        ]

        for i, defense in enumerate(defenses):
            text = self.small_font.render(defense, True, TEXT_COLOR)
            self.screen.blit(text, (self.map_width + 40, 160 + i * 25))

        for button in self.action_buttons:
            button.draw(self.screen, self.font)

        self.end_turn_button.draw(self.screen, self.font)

    def draw_turn_indicator(self):
        current_city = self.cities[self.current_turn % len(self.cities)]
        turn_text = self.title_font.render(
            f"{current_city.name}'s Turn" + (" (YOU)" if current_city.is_player else " (Enemy)"),
            True, TEXT_COLOR
        )

        indicator_bg = pygame.Rect(20, 20, turn_text.get_width() + 40, turn_text.get_height() + 20)
        color = (60, 80, 100) if current_city.is_player else (100, 60, 70)
        pygame.draw.rect(self.screen, color, indicator_bg, border_radius=10)
        pygame.draw.rect(self.screen, (80, 80, 90), indicator_bg, 2, border_radius=10)
        self.screen.blit(turn_text, (40, 35))

    def draw_message(self):
        if self.message and self.message_timer > 0:
            msg_text = self.font.render(self.message, True, TEXT_COLOR)
            msg_rect = pygame.Rect(
                self.WIDTH // 2 - msg_text.get_width() // 2 - 15,
                self.HEIGHT - 70,
                msg_text.get_width() + 30,
                40
            )
            pygame.draw.rect(self.screen, (60, 60, 80), msg_rect, border_radius=5)
            pygame.draw.rect(self.screen, (80, 80, 100), msg_rect, 2, border_radius=5)
            self.screen.blit(msg_text, (self.WIDTH // 2 - msg_text.get_width() // 2, self.HEIGHT - 60))

    def handle_player_turn(self, mouse_pos, mouse_click):
        current_city = self.cities[self.current_turn % len(self.cities)]

        if self.game_phase == GamePhase.CHOOSE_ACTION:
            for i, button in enumerate(self.action_buttons):
                if button.is_clicked(mouse_pos, mouse_click):
                    if i < 3:  # Attacks
                        attack_types = [ActionType.AIR_ATTACK, ActionType.LAND_ATTACK, ActionType.SEA_ATTACK]
                        self.selected_action = attack_types[i]
                        self.game_phase = GamePhase.CHOOSE_TARGET
                        self.show_message(f"Select target for {self.selected_action.name.replace('_', ' ')}")
                    else:  # Builds
                        build_types = [ActionType.BUILD_AIR_DEFENSE, ActionType.BUILD_LAND_DEFENSE,
                                       ActionType.BUILD_SEA_DEFENSE]
                        build_action = build_types[i - 3]
                        if current_city.perform_action(build_action):
                            self.show_message(f"Built {build_action.name.replace('BUILD_', '').replace('_', ' ')}!")
                        else:
                            self.show_message("Cannot build now!")

            if self.end_turn_button.is_clicked(mouse_pos, mouse_click):
                self.end_turn()

        elif self.game_phase == GamePhase.CHOOSE_TARGET:
            if mouse_click and mouse_pos[0] < self.map_width:
                for city in self.cities:
                    if city != current_city and city.health > 0:
                        distance = math.sqrt((mouse_pos[0] - city.position[0]) ** 2 +
                                             (mouse_pos[1] - city.position[1]) ** 2)
                        if distance < city.radius + 5:
                            if current_city.perform_action(self.selected_action, city):
                                damage = 25
                                if self.selected_action == ActionType.AIR_ATTACK:
                                    damage -= city.air_defense
                                elif self.selected_action == ActionType.LAND_ATTACK:
                                    damage -= city.land_defense
                                elif self.selected_action == ActionType.SEA_ATTACK:
                                    damage -= city.sea_defense

                                damage = max(5, damage)
                                self.show_message(
                                    f"Attacked {city.name} with {self.selected_action.name.replace('_', ' ')} " +
                                    f"for {damage} damage!"
                                )
                                self.game_phase = GamePhase.CHOOSE_ACTION
                            else:
                                self.show_message("Cannot attack now!")
                            break

    def cpu_turn(self):
        current_city = self.cities[self.current_turn % len(self.cities)]

        if random.random() < 0.5 and current_city.attacks_remaining > 0:
            targets = [c for c in self.cities if c != current_city and c.health > 0]
            if targets:
                target = min(targets, key=lambda x: x.health)
                attack_type = random.choice([
                    ActionType.AIR_ATTACK,
                    ActionType.LAND_ATTACK,
                    ActionType.SEA_ATTACK
                ])
                if current_city.perform_action(attack_type, target):
                    damage = 25
                    if attack_type == ActionType.AIR_ATTACK:
                        damage -= target.air_defense
                    elif attack_type == ActionType.LAND_ATTACK:
                        damage -= target.land_defense
                    elif attack_type == ActionType.SEA_ATTACK:
                        damage -= target.sea_defense

                    damage = max(5, damage)
                    self.show_message(
                        f"{current_city.name} launched {attack_type.name.replace('_', ' ')} on {target.name}!"
                    )
        elif current_city.builds_remaining > 0:
            build_type = random.choice([
                ActionType.BUILD_AIR_DEFENSE,
                ActionType.BUILD_LAND_DEFENSE,
                ActionType.BUILD_SEA_DEFENSE
            ])
            if current_city.perform_action(build_type):
                self.show_message(
                    f"{current_city.name} built {build_type.name.replace('BUILD_', '').replace('_', ' ')}!")

        self.end_turn()

    def end_turn(self):
        # Reset current city's turn
        self.cities[self.current_turn % len(self.cities)].reset_turn()
        self.selected_action = None

        # Find next active city
        next_index = self.get_next_active_city_index(self.current_turn)
        if next_index is None:
            # Shouldn't happen as game should end before all cities are dead
            self.current_turn += 1
        else:
            # Skip dead cities by moving to next active one
            if next_index <= self.current_turn:
                # We've wrapped around, check for game over
                remaining_players = sum(1 for city in self.cities if city.is_player and city.health > 0)
                remaining_enemies = sum(1 for city in self.cities if not city.is_player and city.health > 0)

                if remaining_players == 0:
                    self.show_message("GAME OVER - You lost!", 300)
                    self.game_phase = GamePhase.GAME_OVER
                    return
                elif remaining_enemies == 0:
                    self.show_message("VICTORY - You won!", 300)
                    self.game_phase = GamePhase.GAME_OVER
                    return

            self.current_turn = next_index

        self.game_phase = GamePhase.CHOOSE_ACTION

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True

            current_city = self.cities[self.current_turn % len(self.cities)]

            if self.message_timer > 0:
                self.message_timer -= 1

            if current_city.health > 0:
                if current_city.is_player and self.game_phase != GamePhase.GAME_OVER:
                    self.handle_player_turn(mouse_pos, mouse_click)
                elif self.game_phase != GamePhase.GAME_OVER:
                    pygame.time.delay(1000)
                    self.cpu_turn()

            self.draw_map()
            self.draw_cities()
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