# main.py - Main entry point for the game
import pygame
import random
import math
import sys
import os
#from menu import Menu
# menu.py - Game menu implementation

class AnimatedBackground:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Create a list of animated dots
        self.dots = []
        self.num_dots = 50
        self.dot_size = 4
        self.dot_speed = 2
        self.dot_color = (0, 0, 255)  # Blue dots
        
        # Initialize dots with random positions and directions
        for _ in range(self.num_dots):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            dx = random.choice([-self.dot_speed, self.dot_speed])
            dy = random.choice([-self.dot_speed, self.dot_speed])
            self.dots.append({
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'alpha': random.randint(50, 255)  # Random transparency
            })
    
    def update(self):
        # Update dot positions
        for dot in self.dots:
            dot['x'] += dot['dx']
            dot['y'] += dot['dy']
            
            # Bounce off screen edges
            if dot['x'] <= 0 or dot['x'] >= self.width:
                dot['dx'] *= -1
            if dot['y'] <= 0 or dot['y'] >= self.height:
                dot['dy'] *= -1
            
            # Update transparency for a pulsing effect
            dot['alpha'] = (dot['alpha'] + 5) % 255
    
    def draw(self):
        # Create a surface for the background
        background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 180))  # Semi-transparent black background
        
        # Draw dots
        for dot in self.dots:
            color = (*self.dot_color, dot['alpha'])
            pygame.draw.circle(background, color, (int(dot['x']), int(dot['y'])), self.dot_size)
        
        # Draw the background
        self.screen.blit(background, (0, 0))

class Button:
    def __init__(self, screen, text, pos, size, callback=None, param=None):
        self.screen = screen
        self.text = text
        self.x, self.y = pos
        self.width, self.height = size
        self.callback = callback
        self.param = param
        self.hovered = False
        
        # Colors
        self.normal_color = (255, 255, 0)  # Pac-Man yellow
        self.hover_color = (255, 165, 0)   # Orange
        self.text_color = (0, 0, 0)        # Black
        
        # Font
        self.font = pygame.font.SysFont('Arial', 36)  # Increased font size
        self.text_surf = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        
    def draw(self):
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(self.screen, color, (self.x, self.y, self.width, self.height), 0, 10)
        pygame.draw.rect(self.screen, (0, 0, 255), (self.x, self.y, self.width, self.height), 2, 10)
        self.screen.blit(self.text_surf, self.text_rect)
    
    def check_hover(self, pos):
        prev_hover = self.hovered
        self.hovered = (self.x <= pos[0] <= self.x + self.width and 
                        self.y <= pos[1] <= self.y + self.height)
        return self.hovered != prev_hover  # Return True if state changed
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            if self.callback:
                if self.param is not None:
                    self.callback(self.param)
                else:
                    self.callback()
            return True
        return False

class Menu:
    def __init__(self, screen, start_game_callback):
        self.screen = screen
        self.start_game_callback = start_game_callback
        self.buttons = []
        self.logo_font = pygame.font.SysFont('Arial', 96, bold=True)
        self.info_font = pygame.font.SysFont('Arial', 32)
        
        # Create animated background
        self.background = AnimatedBackground(screen)
        
        # Create level selection buttons
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        button_width = 250
        button_height = 50
        button_spacing = 20
        
        # Title position
        self.title_y = screen_height // 4 - 50
        
        # Description position
        self.desc_y = self.title_y + 100
        
        # Instructions position
        self.instructions_y = screen_height - 100
        
        # Calculate starting y-position for the grid of level buttons
        start_y = self.desc_y + 100
        
        # Create a grid of level buttons (2 rows x 5 columns)
        for row in range(2):
            for col in range(5):
                level = row * 5 + col + 1
                x = (screen_width - (button_width * 5 + button_spacing * 4)) // 2 + col * (button_width + button_spacing)
                y = start_y + row * (button_height + button_spacing)
                
                self.buttons.append(
                    Button(
                        screen, 
                        f"Level {level}",
                        (x, y),
                        (button_width, button_height),
                        self.start_game_callback,
                        level
                    )
                )
    
    def update(self):
        # Update background animation
        self.background.update()
        
        # Check for button hover
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
    
    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return
    
    def draw(self):
        # Draw animated background
        self.background.draw()
        
        # Draw title
        title_surf = self.logo_font.render("PAC-MAN ADVENTURE", True, (255, 255, 0))
        title_rect = title_surf.get_rect(center=(self.screen.get_width()//2, self.title_y))
        self.screen.blit(title_surf, title_rect)
        
        # Draw description
        description = "Navigate through mazes, eat dots, and avoid ghosts!"
        desc_surf = self.info_font.render(description, True, (255, 255, 255))
        desc_rect = desc_surf.get_rect(center=(self.screen.get_width()//2, self.desc_y))
        self.screen.blit(desc_surf, desc_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw()
        
        # Draw instructions
        instructions = "Use arrow keys to control Pac-Man. Press ESC to return to menu."
        inst_surf = self.info_font.render(instructions, True, (200, 200, 200))
        inst_rect = inst_surf.get_rect(center=(self.screen.get_width()//2, self.instructions_y))
        self.screen.blit(inst_surf, inst_rect)


#from game import Game
# game.py - Core game mechanics
#from entities import PacMan, Ghost, Pellet, PowerPellet
# entities.py - Game entities such as Pac-Man, ghosts, and pellets

class PacMan:
    def __init__(self, x, y, size):
        self.start_x = x
        self.start_y = y
        self.size = size
        self.reset()
        
        # Animation variables
        self.mouth_angle = 0
        self.mouth_opening = True
        self.animation_speed = 10
        
        # Movement variables
        self.speed = 3  # Movement speed
        self.grid_size = size  # Size of one grid cell
        self.moving = False
        self.direction = (0, 0)  # Current direction
        self.next_direction = (0, 0)  # Next direction to try
        self.position = [float(x), float(y)]  # Precise position for smooth movement
        self.last_position = [float(x), float(y)]  # Store last valid position
        self.grid_x = int(x / size)  # Current grid position
        self.grid_y = int(y / size)  # Current grid position
        self.last_direction = (0, 0)  # Store last direction for smoother movement
    
    def reset(self):
        self.rect = pygame.Rect(self.start_x, self.start_y, self.size, self.size)
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.last_direction = (0, 0)
        self.moving = False
        self.position = [float(self.start_x), float(self.start_y)]
        self.last_position = [float(self.start_x), float(self.start_y)]
        self.grid_x = int(self.start_x / self.size)
        self.grid_y = int(self.start_y / self.size)
    
    def set_direction(self, dx, dy):
        # Store the new direction
        self.next_direction = (dx, dy)
        self.moving = True
    
    def update(self, walls):
        # Try to move in the next direction if it's different from current
        if self.next_direction != self.direction and self.moving:
            next_x = self.position[0] + self.next_direction[0] * self.speed
            next_y = self.position[1] + self.next_direction[1] * self.speed
            next_rect = pygame.Rect(next_x, next_y, self.size, self.size)
            
            can_move = True
            for wall in walls:
                if next_rect.colliderect(wall):
                    can_move = False
                    break
            
            if can_move:
                self.direction = self.next_direction
                self.last_direction = self.direction
        
        # Move in the current direction
        if self.direction != (0, 0) and self.moving:
            next_x = self.position[0] + self.direction[0] * self.speed
            next_y = self.position[1] + self.direction[1] * self.speed
            next_rect = pygame.Rect(next_x, next_y, self.size, self.size)
            
            can_move = True
            for wall in walls:
                if next_rect.colliderect(wall):
                    can_move = False
                    break
            
            if can_move:
                self.last_position = self.position.copy()  # Store last valid position
                self.position[0] = next_x
                self.position[1] = next_y
                self.rect.x = int(self.position[0])
                self.rect.y = int(self.position[1])
                self.grid_x = int(self.position[0] / self.grid_size)
                self.grid_y = int(self.position[1] / self.grid_size)
            else:
                # If we hit a wall, snap to the last valid position
                self.position = self.last_position.copy()
                self.rect.x = int(self.position[0])
                self.rect.y = int(self.position[1])
                self.grid_x = int(self.position[0] / self.grid_size)
                self.grid_y = int(self.position[1] / self.grid_size)
                self.moving = False
                self.direction = (0, 0)
                self.next_direction = (0, 0)
        
        # Update mouth animation
        if self.mouth_opening:
            self.mouth_angle += self.animation_speed
            if self.mouth_angle >= 45:
                self.mouth_opening = False
        else:
            self.mouth_angle -= self.animation_speed
            if self.mouth_angle <= 0:
                self.mouth_opening = True
    
    def draw(self, screen):
        # Calculate the center of the character
        center = (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2)
        
        # Draw Pac-Man as a yellow circle with a mouth
        pygame.draw.circle(screen, (255, 255, 0), center, self.rect.width//2)
        
        # Calculate mouth angle based on direction
        angle = 0
        if self.direction == (1, 0):  # Right
            angle = 0
        elif self.direction == (0, 1):  # Down
            angle = 90
        elif self.direction == (-1, 0):  # Left
            angle = 180
        elif self.direction == (0, -1):  # Up
            angle = 270
        
        # Draw the mouth as a pie slice
        if self.direction != (0, 0):  # Only draw mouth if moving
            pygame.draw.polygon(screen, (0, 0, 0), [
                center,
                (center[0] + math.cos(math.radians(angle - self.mouth_angle)) * self.rect.width//2,
                 center[1] + math.sin(math.radians(angle - self.mouth_angle)) * self.rect.width//2),
                (center[0] + math.cos(math.radians(angle + self.mouth_angle)) * self.rect.width//2,
                 center[1] + math.sin(math.radians(angle + self.mouth_angle)) * self.rect.width//2)
            ])

class Ghost:
    def __init__(self, x, y, size, color):
        self.start_x = x
        self.start_y = y
        self.size = size
        self.color = color
        self.scared_color = (0, 0, 255)  # Blue when scared
        self.reset()
        
        # Ghost behavior type
        self.behavior_type = random.choice(["chase", "random", "patrol"])
        self.patrol_points = []
        self.current_patrol_point = 0
        
        # Create patrol points
        for _ in range(4):
            self.patrol_points.append((
                random.randint(100, 700),
                random.randint(100, 500)
            ))
    
    def reset(self):
        self.rect = pygame.Rect(self.start_x, self.start_y, self.size, self.size)
        self.direction = (0, 0)
        self.speed = 0.8  # Reduced from 1.5 to 0.8 for slower movement
    
    def update(self, walls, pacman, scared=False):
        # Adjust speed based on scared state
        actual_speed = self.speed * 0.3 if scared else self.speed  # Reduced scared speed from 0.5 to 0.3
        
        # Determine direction based on behavior type
        if scared:
            # Run away from Pac-Man when scared
            self.flee_from_pacman(pacman)
        else:
            if self.behavior_type == "chase":
                self.chase_pacman(pacman)
            elif self.behavior_type == "random":
                self.move_randomly()
            elif self.behavior_type == "patrol":
                self.patrol()
        
        # Try to move in the current direction
        next_rect = self.rect.copy()
        next_rect.x += self.direction[0] * actual_speed
        next_rect.y += self.direction[1] * actual_speed
        
        # Check for wall collisions
        collision = False
        for wall in walls:
            if next_rect.colliderect(wall):
                collision = True
                break
        
        if not collision:
            self.rect = next_rect
        else:
            # If we hit a wall, choose a new direction
            self.choose_new_direction(walls)
    
    def chase_pacman(self, pacman):
        # Find direction to Pac-Man
        dx = pacman.rect.centerx - self.rect.centerx
        dy = pacman.rect.centery - self.rect.centery
        
        # Normalize to get unit direction
        length = max(0.1, math.sqrt(dx*dx + dy*dy))
        dx /= length
        dy /= length
        
        # Simplify to cardinal directions
        if abs(dx) > abs(dy):
            self.direction = (1 if dx > 0 else -1, 0)
        else:
            self.direction = (0, 1 if dy > 0 else -1)
    
    def flee_from_pacman(self, pacman):
        # Find direction away from Pac-Man
        dx = self.rect.centerx - pacman.rect.centerx
        dy = self.rect.centery - pacman.rect.centery
        
        # Normalize to get unit direction
        length = max(0.1, math.sqrt(dx*dx + dy*dy))
        dx /= length
        dy /= length
        
        # Simplify to cardinal directions
        if abs(dx) > abs(dy):
            self.direction = (1 if dx > 0 else -1, 0)
        else:
            self.direction = (0, 1 if dy > 0 else -1)
    
    def move_randomly(self):
        if random.random() < 0.02:  # 2% chance to change direction each frame
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            self.direction = random.choice(directions)
    
    def patrol(self):
        if not self.patrol_points:
            return
            
        target = self.patrol_points[self.current_patrol_point]
        
        # Calculate direction to target
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        
        # Check if we're close to the target
        if abs(dx) < 10 and abs(dy) < 10:
            # Move to next patrol point
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)
            return
        
        # Normalize to get unit direction
        length = max(0.1, math.sqrt(dx*dx + dy*dy))
        dx /= length
        dy /= length
        
        # Simplify to cardinal directions
        if abs(dx) > abs(dy):
            self.direction = (1 if dx > 0 else -1, 0)
        else:
            self.direction = (0, 1 if dy > 0 else -1)
    
    def choose_new_direction(self, walls):
        # Try each direction until we find one that doesn't cause a collision
        possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(possible_directions)
        
        for direction in possible_directions:
            next_rect = self.rect.copy()
            next_rect.x += direction[0] * self.speed
            next_rect.y += direction[1] * self.speed
            
            collision = False
            for wall in walls:
                if next_rect.colliderect(wall):
                    collision = True
                    break
            
            if not collision:
                self.direction = direction
                break
    
    def draw(self, screen, scared=False):
        color = self.scared_color if scared else self.color
        
        # Draw the main body (semi-circle)
        pygame.draw.circle(screen, color, (self.rect.centerx, self.rect.centery - self.size//4), self.size//2)
        
        # Draw the lower part (wavy bottom)
        wave_rect = pygame.Rect(
            self.rect.x,
            self.rect.centery - self.size//4,
            self.size,
            self.size//2
        )
        pygame.draw.rect(screen, color, wave_rect)
        
        # Draw the bottom waves
        wave_height = self.size//6
        wave_width = self.size//3
        
        for i in range(3):
            x_start = self.rect.x + i * wave_width
            pygame.draw.circle(
                screen,
                (0, 0, 0),  # Background color (for the gaps)
                (x_start + wave_width//2, self.rect.bottom),
                wave_height
            )
        
        # Draw eyes
        eye_size = self.size//5
        eye_y = self.rect.centery - self.size//4
        
        # Eye whites
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.centerx - eye_size, eye_y), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.centerx + eye_size, eye_y), eye_size)
        
        # Eye pupils - position based on direction
        pupil_offset_x = self.direction[0] * eye_size//2
        pupil_offset_y = self.direction[1] * eye_size//2
        
        if scared:
            pygame.draw.circle(screen, (0, 0, 0), (self.rect.centerx - eye_size, eye_y), eye_size//2)
            pygame.draw.circle(screen, (0, 0, 0), (self.rect.centerx + eye_size, eye_y), eye_size//2)
        else:
            # Normal pupil eyes
            pygame.draw.circle(
                screen, 
                (0, 0, 255), 
                (self.rect.centerx - eye_size + pupil_offset_x, eye_y + pupil_offset_y), 
                eye_size//2
            )
            pygame.draw.circle(
                screen, 
                (0, 0, 255), 
                (self.rect.centerx + eye_size + pupil_offset_x, eye_y + pupil_offset_y), 
                eye_size//2
            )

class Pellet:
    def __init__(self, x, y, tile_size):
        self.size = tile_size // 5
        self.rect = pygame.Rect(
            x + tile_size//2 - self.size//2,
            y + tile_size//2 - self.size//2,
            self.size,
            self.size
        )
    
    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            self.rect.center,
            self.size // 2
        )

class PowerPellet:
    def __init__(self, x, y, tile_size):
        self.size = tile_size // 2
        self.rect = pygame.Rect(
            x + tile_size//2 - self.size//2,
            y + tile_size//2 - self.size//2,
            self.size,
            self.size
        )
        self.animation_counter = 0
        self.visible = True
    
    def draw(self, screen):
        # Make the power pellet flash
        self.animation_counter += 1
        if self.animation_counter >= 30:
            self.animation_counter = 0
            self.visible = not self.visible
        
        if self.visible:
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                self.rect.center,
                self.size // 2
            )


# from level import load_level
# level.py - Level loading and management

# Define 10 different maze layouts
LEVEL_LAYOUTS = [
    # Level 1 - Simple classic layout
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W............WW............W",
        "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
        "WoWWWW.WWWWW.WW.WWWWW.WWWWoW",
        "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
        "W..........................W",
        "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
        "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
        "W......WW....WW....WW......W",
        "WWWWWW.WWWWW WW WWWWW.WWWWWW",
        "WWWWWW.WWWWW WW WWWWW.WWWWWW",
        "WWWWWW.WW          WW.WWWWWW",
        "WWWWWW.WW WWWGGWWW WW.WWWWWW",
        "WWWWWW.WW W      W WW.WWWWWW",
        "      .   W      W   .      ",
        "WWWWWW.WW W      W WW.WWWWWW",
        "WWWWWW.WW WWWWWWWW WW.WWWWWW",
        "WWWWWW.WW          WW.WWWWWW",
        "WWWWWW.WW WWWWWWWW WW.WWWWWW",
        "WWWWWW.WW WWWWWWWW WW.WWWWWW",
        "W............WW............W",
        "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
        "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
        "Wo..WW................WW..oW",
        "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",
        "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",
        "W......WW....WW....WW......W",
        "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
        "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
        "W...........P............W.W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 2 - More complex layout
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W.........................oW",
        "W.WWWWWW.WWWWW.WWWWW.WWWWW.W",
        "W.WWWWWW.WWWWW.WWWWW.WWWWW.W",
        "W.WW.....WW....WW....WW....W",
        "W.WW.WWW.WW.WWWWW.WWWWW.WW.W",
        "W.WW.WWW.WW.WWWWW.WWWWW.WW.W",
        "W....WWW.............WWW...W",
        "WWWW.WWW.WWW.WWW.WWW.WWW.WWW",
        "WWWW.WWW.WWW.WWW.WWW.WWW.WWW",
        "W....WWW.WWW.....WWW.WWW...W",
        "W.WWWWWW.WWWWW.WWWWW.WWWWW.W",
        "W.WWWWWW.WWWWW.WWWWW.WWWWW.W",
        "Wo........G...P...G.......oW",
        "WWWWWWWW.WWWWW.WWWWW.WWWWWWW",
        "WWWWWWWW.WWWWW.WWWWW.WWWWWWW",
        "W.............W............W",
        "W.WWW.WWWWWWW.W.WWWWWWW.WWW.",
        "W.WWW.WWWWWWW.W.WWWWWWW.WWW.",
        "W.WWW.........W.........WWW.",
        "W.WWW.WWWWWWWWWWWWWWWWW.WWW.",
        "W.WWW.WWWWWWWWWWWWWWWWW.WWW.",
        "W.....WWWWWWWWWWWWWWWWW.....",
        "WWWWW.WWWWWWWWWWWWWWWWW.WWWW",
        "WWWWW.WWWWWWWWWWWWWWWWW.WWWW",
        "WWWWW...................WWWW",
        "WWWWWoWWWWWWWWWWWWWWWWWoWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 3 - Spiral maze
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W..........................W",
        "W.WWWWWWWWWWWWWWWWWWWWWWWW.W",
        "W.WP.......................W",
        "W.W.WWWWWWWWWWWWWWWWWWWWW.W",
        "W.W.W.....................W",
        "W.W.W.WWWWWWWWWWWWWWWWWW.W.W",
        "W.W.W.W...................W",
        "W.W.W.W.WWWWWWWWWWWWWWWW.W.W",
        "W.W.W.W.W.................W",
        "W.W.W.W.W.WWWWWWWWWWWWWW.W.W",
        "W.W.W.W.W.W...............W",
        "W.W.W.W.W.W.WWWWWWWWWWWW.W.W",
        "W.W.W.W.W.W.W....G.......W.W",
        "W.W.W.W.W.W.W.WWWWWWWWWW.W.W",
        "WGW.W.W.W.W.W.W.........W.W",
        "W...W.W.W.W.W.W.WWWWWWW.W.W",
        "WWW.W.W.W.W.W.W.W.....W.W.W",
        "W...W.W.W.W.W.W.WGW.W.W.W.W",
        "W.WWW.W.W.W.W.W...W.W.W.W.W",
        "W.....W.W.W.W.WWW.W.W.W.W.W",
        "WWWWWWW.W.W.W...W.W.W.W.W.W",
        "W.......W.W.WWW.W.W.W.W.W.W",
        "W.WWWWWWW.W...W.W.W.W.W.W.W",
        "W.........WWW.W.W.W.W.W...W",
        "WWWWWWWWWW....W.W.W.W.WWW.W",
        "Wo............W.W.W.W.....W",
        "WWWWWWWWWWWWWWW.W.W.WWWWWWW",
        "Wo..............W.........oW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 4 - Open center
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W..........................W",
        "W.WWWW.WWWWW.WWWW.WWWWW.WW.W",
        "WoWWWW.WWWWW.WWWW.WWWWW.WWoW",
        "W.WWWW...WWW.WWWW.WWW...WW.W",
        "W......W....WWWWWW....W....W",
        "WWWWWW.WWWW........WWWW.WWWW",
        "WWWWWW.WWWWW.WWWW.WWWWW.WWWW",
        "WWWWWW.WWWWW.WWWW.WWWWW.WWWW",
        "WWWWWW.WW.............WW.WWWW",
        "WWWWWW.WW.WWWWWWWWWW.WW.WWWW",
        "WWWWWW.WW.WWWWWWWWWW.WW.WWWW",
        "WWWWWW.WW.WW      WW.WW.WWWW",
        "      .   WW      WW   .    ",
        "WWWWWW.WW WW  GG  WW WW.WWWW",
        "WWWWWW.WW WW  GG  WW WW.WWWW",
        "WWWWWW.WW WW      WW WW.WWWW",
        "WWWWWW.WW WWWWWWWWWW WW.WWWW",
        "WWWWWW.WW          P WW.WWWW",
        "WWWWWW.WW WWWWWWWWWWWWW.WWWW",
        "WWWWWW.WW WWWWWWWWWWWWW.WWWW",
        "W......WW.............WW...W",
        "W.WWWW.WWWWW.WWWW.WWWWW.WW.W",
        "W.WWWW.WWWWW.WWWW.WWWWW.WW.W",
        "Wo.WWW...........WWW...WWoW",
        "WWW.WWWWWWWWWWWWWWWWWWW.WWWW",
        "WWW..........................W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 5 - Checkerboard
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.........................oW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "Wo........................W",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W...G.....................oW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W...P.....G................W",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W.........................oW",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "Wo.........................W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 6 - Pathways
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W..........................W",
        "W.WWWWWWWWWWWWWWWWWWWWWWWW.W",
        "W.W........................W",
        "W.W.WWWWWWWWWWWWWWWWWWWWWW.W",
        "W.W.W......................W",
        "W.W.W.WWWWWWWWWWWWWWWWWWWW.W",
        "W.W.W.W....................W",
        "W.W.W.W.WWWWWWWWWWWWWWWWWW.W",
        "W.W.W.W.W................W.W",
        "W.W.W.W.W.WWWWWWWWWWWWWW.W.W",
        "W.W.W.W.W.W...g..........W.W",
        "W.W.W.W.W.W.WWWWWW.WWWWW.W.W",
        "W.W.W.W.W.W.WP........GW.W.W",
        "W.W.W.W.W.W.WWW.WWWWWWWW.W.W",
        "W.W.W.W.W.W..............W.W",
        "W.W.W.W.W.WWWWWWWWWWWWWW.W.W",
        "W.W.W.W.W................W.W",
        "W.W.W.W.WWWWWWWWWWWWWWWW.W.W",
        "W.W.W.W..................W.W",
        "W.W.W.WWWWWWWWWWWWWWWWWW.W.W",
        "W.W.W.....................W.W",
        "W.W.WWWWWWWWWWWWWWWWWWWW.W.W",
        "W.W.......................W.W",
        "W.WWWWWWWWWWWWWWWWWWWWWW.W.W",
        "W.........................W.W",
        "WoWWWWWWWWWWWWWWWWWWWWWWWWoW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 7 - Chambers
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W...........W............W.W",
        "W.WWWWWWWWW.W.WWWWWWWWWW.W.W",
        "W.W.......W.W.W........W.W.W",
        "W.W.WWWWW.W.W.W.WWWWWW.W.W.W",
        "W.W.W...W.W.W.W.W....W.W.W.W",
        "W.W.W.W.W.W.W.W.W.WW.W.W.W.W",
        "W.W.W.W.W.W.W.W.W.WW.W.W.W.W",
        "W...W.W.W...W...W.WW.W...W.W",
        "WWWWW.W.WWWWWWWWW.WW.WWWWW.W",
        "Wo....W...........WW.....oW",
        "WWWWWWWWWWWWWWWWW.WWWWWWWWWW",
        "W.............W...W........W",
        "W.WWWWWWWWWWW.W.WWW.WWWWWW.W",
        "W.W...........W...W.W....W.W",
        "W.W.WWWWWWWWWWWWW.W.W.WW.W.W",
        "W.W.W.............W.W.WW.W.W",
        "W.W.W.WWWWWWWWWWWWW.W.WW.W.W",
        "W.W.W.W...........GW.WW.W.W",
        "W.W.W.W.WWWWWWWWWWW..WW.W.W",
        "W.W.W.W.WP..G........WW.W.W",
        "W.W.W.W.WWWWWWWWWWWWWWW.W.W",
        "W.W.W.W...............W.W.W",
        "W.W.W.WWWWWWWWWWWWWWW.W.W.W",
        "W.W.W.................W.W.W",
        "W.W.WWWWWWWWWWWWWWWWWWW.W.W",
        "W.W.......................W",
        "WoWWWWWWWWWWWWWWWWWWWWWWWWoW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 8 - Scattered Walls
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W.................G........W",
        "W.WWWW.WWWWW.WWWWW.WWWW.WW.W",
        "W.WWWW.WWWWW.WWWWW.WWWW.WW.W",
        "W..........................W",
        "WWW.WWWWW.WWWWW.WWWWW.WWW.WW",
        "WWW.WWWWW.WWWWW.WWWWW.WWW.WW",
        "W..........................W",
        "W.WWWW.WWWWW.WWWWW.WWWW.WW.W",
        "W.WWWW.WWWWW.WWWWW.WWWW.WW.W",
        "W.......................W..W",
        "WWW.WWWWW.WWWWW.WWWWW.WWW.WW",
        "WWW.WWWWW.WWWWW.WWWWW.WWW.WW",
        "WP.........................W",
        "WWW.WWWWW.WWWWW.WWWWW.WWW.WW",
        "WWW.WWWWW.WWWWW.WWWWW.WWW.WW",
        "W..........................W",
        "W.WWWW.WWWWW.WWWWW.WWWW.WW.W",
        "W.WWWW.WWWWW.WWWWW.WWWW.WW.W",
        "W...G.....................W",
        "WWW.WWWWW.WWWWW.WWWWW.WWW.WW",
        "WWW.WWWWW.WWWWW.WWWWW.WWW.WW",
        "W.........................oW",
        "W.WWWW.WWWWW.WWWWW.WWWW.WW.W",
        "W.WWWW.WWWWW.WWWWW.WWWW.WW.W",
        "Wo.........................W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 9 - Zigzag
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.........................oW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "Wo........................W",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W...G.....................oW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W...P.....G................W",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W.........................oW",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "Wo.........................W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    
    # Level 10 - Final Challenge
    [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.........................oW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "Wo........................W",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W...G.....................oW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W..........................W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W...P.....G................W",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "WWWW.WWWW.WWWW.WWWW.WWWW.WWW",
        "W.........................oW",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "W.WWWW.WWWW.WWWW.WWWW.WWWW.W",
        "Wo.........................W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]
]

def load_level(level_num):
    if 1 <= level_num <= len(LEVEL_LAYOUTS):
        map_data = LEVEL_LAYOUTS[level_num - 1]
        wall_rects = []
        
        # Create wall rectangles based on the map data
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                if cell == 'W':
                    # Create wall rectangle with proper grid alignment and width 15
                    wall_rect = pygame.Rect(
                        x * 20,  # x position
                        y * 20,  # y position
                        15,      # width of 15
                        15       # height of 15
                    )
                    # Center the wall rectangle
                    wall_rect.x += 2.5  # Shift right by 2.5 pixels
                    wall_rect.y += 2.5  # Shift down by 2.5 pixels
                    wall_rects.append(wall_rect)
        
        return map_data, wall_rects
    else:
        # Return a default level if the level number is invalid
        return LEVEL_LAYOUTS[0], []


class Game:
    def __init__(self, screen, level_num, level_complete_callback, game_over_callback):
        self.screen = screen
        self.level_num = level_num
        self.level_complete_callback = level_complete_callback
        self.game_over_callback = game_over_callback
        
        # Game properties
        self.score = 0
        self.lives = 3
        self.paused = False
        
        # Define wall colors for each level
        self.wall_colors = [
            (0, 0, 255),    # Level 1 - Blue
            (255, 0, 0),    # Level 2 - Red
            (0, 255, 0),    # Level 3 - Green
            (255, 255, 0),  # Level 4 - Yellow
            (255, 0, 255),  # Level 5 - Magenta
            (0, 255, 255),  # Level 6 - Cyan
            (255, 165, 0),  # Level 7 - Orange
            (128, 0, 128),  # Level 8 - Purple
            (0, 128, 0),    # Level 9 - Dark Green
            (255, 192, 203) # Level 10 - Pink
        ]
        
        # Load level
        self.map_data, self.wall_rects = load_level(level_num)
        self.tile_size = 20  # Size of each tile in the map
        
        # Calculate map offset to center it on screen
        map_width = len(self.map_data[0]) * self.tile_size
        map_height = len(self.map_data) * self.tile_size
        self.map_offset_x = (screen.get_width() - map_width) // 2
        self.map_offset_y = (screen.get_height() - map_height) // 2
        
        # Create game entities
        self.create_entities()
        
        # Font for score display
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Game state
        self.game_active = True
        self.power_pellet_active = False
        self.power_timer = 0
        
    def create_entities(self):
        # Create Pac-Man, ghosts, pellets based on the map data
        self.pacman = None
        self.ghosts = []
        self.pellets = []
        self.power_pellets = []
        
        # Parse the map_data to create entities
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                # Convert grid position to screen position
                screen_x = self.map_offset_x + x * self.tile_size
                screen_y = self.map_offset_y + y * self.tile_size
                
                if cell == 'P':  # Pac-Man
                    self.pacman = PacMan(screen_x, screen_y, self.tile_size)
                elif cell == 'G':  # Ghost
                    # Create ghosts with different colors and behaviors
                    ghost_colors = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]
                    color = ghost_colors[len(self.ghosts) % len(ghost_colors)]
                    self.ghosts.append(Ghost(screen_x, screen_y, self.tile_size, color))
                elif cell == '.':  # Pellet
                    self.pellets.append(Pellet(screen_x, screen_y, self.tile_size))
                elif cell == 'O':  # Power Pellet
                    self.power_pellets.append(PowerPellet(screen_x, screen_y, self.tile_size))
        
        # Create outer boundary walls with correct offsets
        map_width = len(self.map_data[0]) * self.tile_size
        map_height = len(self.map_data) * self.tile_size
        
        # Add outer walls to wall_rects with increased distance from maze
        boundary_offset = 30  # Increased distance from maze
        self.wall_rects = [
            pygame.Rect(self.map_offset_x - boundary_offset, self.map_offset_y - boundary_offset, 
                       map_width + (boundary_offset * 2), 15),  # Top
            pygame.Rect(self.map_offset_x - boundary_offset, self.map_offset_y + map_height + boundary_offset - 15, 
                       map_width + (boundary_offset * 2), 15),  # Bottom
            pygame.Rect(self.map_offset_x - boundary_offset, self.map_offset_y - boundary_offset, 
                       15, map_height + (boundary_offset * 2)),  # Left
            pygame.Rect(self.map_offset_x + map_width + boundary_offset - 15, self.map_offset_y - boundary_offset, 
                       15, map_height + (boundary_offset * 2))  # Right
        ]
        
        # Add maze walls with correct offsets
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == 'W':
                    wall_rect = pygame.Rect(
                        self.map_offset_x + x * self.tile_size + 2.5,  # Shift right by 2.5 pixels
                        self.map_offset_y + y * self.tile_size + 2.5,  # Shift down by 2.5 pixels
                        15,  # Width of 15
                        15   # Height of 15
                    )
                    self.wall_rects.append(wall_rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            elif self.pacman and not self.paused:
                # Handle arrow key controls for Pac-Man
                if event.key == pygame.K_LEFT:
                    self.pacman.set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.pacman.set_direction(1, 0)
                elif event.key == pygame.K_UP:
                    self.pacman.set_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.pacman.set_direction(0, 1)
        elif event.type == pygame.KEYUP and self.pacman and not self.paused:
            # Keep the current direction when key is released
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                # Only stop if the released key matches the current direction
                if (event.key == pygame.K_LEFT and self.pacman.direction == (-1, 0)) or \
                   (event.key == pygame.K_RIGHT and self.pacman.direction == (1, 0)) or \
                   (event.key == pygame.K_UP and self.pacman.direction == (0, -1)) or \
                   (event.key == pygame.K_DOWN and self.pacman.direction == (0, 1)):
                    self.pacman.set_direction(0, 0)
                    self.pacman.moving = False
    
    def update(self):
        if self.paused or not self.game_active:
            return
            
        # Update Pac-Man
        if self.pacman:
            self.pacman.update(self.wall_rects)
            
            # Check for pellet collisions
            for pellet in self.pellets[:]:
                if self.pacman.rect.colliderect(pellet.rect):
                    self.pellets.remove(pellet)
                    self.score += 10
            
            # Check for power pellet collisions
            for power_pellet in self.power_pellets[:]:
                if self.pacman.rect.colliderect(power_pellet.rect):
                    self.power_pellets.remove(power_pellet)
                    self.score += 50
                    self.power_pellet_active = True
                    self.power_timer = 300  # 5 seconds at 60 FPS
            
            # Check for ghost collisions
            for ghost in self.ghosts:
                if self.pacman.rect.colliderect(ghost.rect):
                    if self.power_pellet_active:
                        # Eat the ghost
                        ghost.reset()
                        self.score += 200
                    else:
                        # Lose a life
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_active = False
                            self.game_over_callback(self.score)
                        else:
                            self.reset_positions()
        
        # Update ghosts
        for ghost in self.ghosts:
            # Adjust ghost behavior based on power pellet
            scared = self.power_pellet_active
            if scared and self.power_timer < 60:  # Flash during the last second
                scared = self.power_timer % 10 < 5
            
            ghost.update(self.wall_rects, self.pacman, scared)
        
        # Update power pellet timer
        if self.power_pellet_active:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_pellet_active = False
        
        # Check if level is complete (all pellets eaten)
        if len(self.pellets) == 0 and len(self.power_pellets) == 0:
            self.game_active = False
            self.level_complete_callback(self.score)
    
    def reset_positions(self):
        # Reset Pac-Man and ghosts to their starting positions
        if self.pacman:
            self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
    
    def draw(self):
        # Get the wall color for the current level
        wall_color = self.wall_colors[self.level_num - 1]
        
        # Draw maze walls
        for wall_rect in self.wall_rects:
            # Draw walls with the map offset and level-specific color
            pygame.draw.rect(self.screen, wall_color, wall_rect)
        
        # Draw pellets
        for pellet in self.pellets:
            pellet.draw(self.screen)
        
        # Draw power pellets
        for power_pellet in self.power_pellets:
            power_pellet.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen, self.power_pellet_active)
        
        # Draw Pac-Man
        if self.pacman:
            self.pacman.draw(self.screen)
        
        # Draw score and lives
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level_num}", True, (255, 255, 255))
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (20, 50))
        self.screen.blit(level_text, (20, 80))
        
        # Draw paused message if game is paused
        if self.paused:
            paused_font = pygame.font.SysFont('Arial', 48)
            paused_text = paused_font.render("PAUSED", True, (255, 255, 255))
            text_rect = paused_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
            self.screen.blit(paused_text, text_rect)


# Initialize Pygame
pygame.init()
pygame.font.init()

# Game constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
TITLE = "Pac-Man Adventure"

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
LEVEL_COMPLETE = 3

class PacManGame:
    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.state = MENU
        self.level = 1
        self.score = 0
        self.lives = 3
        
        # Create game components
        self.menu = Menu(self.screen, self.start_game)
        self.game = None
        
        # Load sounds
        self.load_sounds()
        
    def load_sounds(self):
        # Create sounds directory if it doesn't exist
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
            
        # Sound effects would be loaded here
        # self.start_sound = pygame.mixer.Sound('sounds/start.wav')
        # etc.
        
    def start_game(self, level=1):
        self.level = level
        self.game = Game(self.screen, level, self.end_level, self.game_over)
        self.state = PLAYING
        # self.start_sound.play()
        
    def end_level(self, score):
        self.score += score
        self.level += 1
        if self.level > 10:
            self.level = 1
            self.state = MENU
        else:
            self.state = LEVEL_COMPLETE
    
    def game_over(self, score):
        self.score += score
        self.state = GAME_OVER
    
    def run(self):
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.state == MENU:
                    self.menu.handle_event(event)
                elif self.state == PLAYING:
                    self.game.handle_event(event)
                elif self.state == GAME_OVER:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.state = MENU
                elif self.state == LEVEL_COMPLETE:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.start_game(self.level)
            
            # Update game state
            if self.state == MENU:
                self.menu.update()
            elif self.state == PLAYING:
                self.game.update()
            
            # Draw everything
            self.screen.fill((0, 0, 0))
            
            if self.state == MENU:
                self.menu.draw()
            elif self.state == PLAYING:
                self.game.draw()
            elif self.state == GAME_OVER:
                self.draw_game_over()
            elif self.state == LEVEL_COMPLETE:
                self.draw_level_complete()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def draw_game_over(self):
        font = pygame.font.SysFont('Arial', 48)
        game_over_text = font.render('GAME OVER', True, (255, 0, 0))
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        continue_text = font.render('Press Enter to continue', True, (255, 255, 255))
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 100))
    
    def draw_level_complete(self):
        font = pygame.font.SysFont('Arial', 48)
        level_text = font.render(f'Level {self.level-1} Complete!', True, (255, 255, 0))
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        continue_text = font.render('Press Enter to continue to next level', True, (255, 255, 255))
        
        self.screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 100))

# Run the game
if __name__ == "__main__":
    game = PacManGame()
    game.run()