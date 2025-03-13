import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 30)  # Dark blue background
FPS = 60

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = 50
PLAYER_COOLDOWN = 15  # Frames between missile firing

# Missile settings
MISSILE_SPEED = 8
MISSILE_SIZE = 10
MISSILE_COLOR = (255, 100, 0)  # Orange-red

# Asteroid settings
ASTEROID_SPEED_MIN = 2
ASTEROID_SPEED_MAX = 5
ASTEROID_SIZE_MIN = 20
ASTEROID_SIZE_MAX = 60
ASTEROID_SPAWN_RATE = 30  # Frames between asteroid spawns

# Star settings
STAR_SPEED = 3
STAR_SIZE = 20
STAR_SPAWN_RATE = 90  # Frames between star spawns

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Explorer")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.image = self.create_spaceship_image()
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = PLAYER_SPEED
        self.cooldown = 0
        
    def create_spaceship_image(self):
        # Create a cool custom spaceship design
        image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Main body (pointed triangle)
        body_color = (30, 144, 255)  # Dodger blue
        pygame.draw.polygon(image, body_color, [
            (self.size//2, 0),  # Front tip
            (0, self.size*0.8),  # Left rear
            (self.size//2, self.size*0.6),  # Middle indent
            (self.size, self.size*0.8)  # Right rear
        ])
        
        # Engines (red glow)
        engine_color = (255, 50, 50)  # Bright red
        pygame.draw.rect(image, engine_color, 
                         pygame.Rect(self.size*0.2, self.size*0.8, self.size*0.2, self.size*0.2))
        pygame.draw.rect(image, engine_color, 
                         pygame.Rect(self.size*0.6, self.size*0.8, self.size*0.2, self.size*0.2))
        
        # Cockpit (light blue)
        cockpit_color = (135, 206, 250)  # Light sky blue
        pygame.draw.ellipse(image, cockpit_color, 
                           pygame.Rect(self.size*0.4, self.size*0.25, self.size*0.2, self.size*0.2))
        
        # Wing highlights
        highlight_color = (173, 216, 230)  # Light blue
        pygame.draw.line(image, highlight_color, 
                         (self.size//2, self.size*0.2), (self.size*0.8, self.size*0.7), 2)
        pygame.draw.line(image, highlight_color, 
                         (self.size//2, self.size*0.2), (self.size*0.2, self.size*0.7), 2)
        
        return image
        
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
            
        # Update cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            
    def fire_missile(self):
        if self.cooldown == 0:
            self.cooldown = PLAYER_COOLDOWN
            missile_x = self.rect.centerx - MISSILE_SIZE // 2
            missile_y = self.rect.top
            return Missile(missile_x, missile_y)
        return None
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Missile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, MISSILE_SIZE, MISSILE_SIZE * 1.5)
        self.speed = MISSILE_SPEED
        
    def update(self):
        self.rect.y -= self.speed
        return self.rect.bottom < 0
        
    def draw(self, surface):
        # Draw missile body
        pygame.draw.rect(surface, MISSILE_COLOR, self.rect)
        
        # Draw missile tip
        pygame.draw.polygon(surface, (255, 200, 0), [
            (self.rect.left, self.rect.top + MISSILE_SIZE * 0.5),
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.top + MISSILE_SIZE * 0.5)
        ])
        
        # Draw exhaust trail
        trail_color = (255, 200, 100, 128)  # Semi-transparent yellow-orange
        trail_surface = pygame.Surface((MISSILE_SIZE, MISSILE_SIZE), pygame.SRCALPHA)
        pygame.draw.polygon(trail_surface, trail_color, [
            (0, 0),
            (MISSILE_SIZE // 2, MISSILE_SIZE),
            (MISSILE_SIZE, 0)
        ])
        surface.blit(trail_surface, (self.rect.left, self.rect.bottom))

class PowerMissile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, MISSILE_SIZE * 1.5, MISSILE_SIZE * 2)
        self.speed = MISSILE_SPEED + 1
        
    def update(self):
        self.rect.y -= self.speed
        return self.rect.bottom < 0
        
    def draw(self, surface):
        # Draw enhanced missile with electric effect
        core_color = (50, 150, 255)  # Blue core
        outer_color = (150, 200, 255)  # Light blue outer
        
        # Main body (larger)
        pygame.draw.rect(surface, outer_color, self.rect)
        
        # Inner core
        inner_rect = pygame.Rect(
            self.rect.left + self.rect.width * 0.25,
            self.rect.top,
            self.rect.width * 0.5,
            self.rect.height
        )
        pygame.draw.rect(surface, core_color, inner_rect)
        
        # Electric effect (random lines)
        for _ in range(3):
            start_x = random.randint(self.rect.left, self.rect.right)
            end_x = random.randint(self.rect.left, self.rect.right)
            pygame.draw.line(surface, (255, 255, 255), 
                            (start_x, self.rect.top + 5), 
                            (end_x, self.rect.bottom - 5), 2)
        
        # Enhanced tip
        pygame.draw.polygon(surface, (200, 230, 255), [
            (self.rect.left, self.rect.top + MISSILE_SIZE * 0.5),
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.top + MISSILE_SIZE * 0.5)
        ])
        
        # Enhanced trail
        trail_color = (100, 200, 255, 150)  # Semi-transparent blue
        trail_surface = pygame.Surface((self.rect.width * 2, self.rect.height), pygame.SRCALPHA)
        pygame.draw.polygon(trail_surface, trail_color, [
            (self.rect.width // 2, 0),
            (0, self.rect.height),
            (self.rect.width, self.rect.height)
        ])
        surface.blit(trail_surface, 
                    (self.rect.left - self.rect.width // 4, self.rect.bottom))


class Asteroid:
    def __init__(self):
        self.size = random.randint(ASTEROID_SIZE_MIN, ASTEROID_SIZE_MAX)
        self.image = self.create_asteroid_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.rect.y = -self.size
        self.speed = random.randint(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        
    def create_asteroid_image(self):
        # Create a realistic asteroid with irregular shape and texture
        image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Base color (gray/brown)
        base_color = (139, 69, 19)  # Brown
        
        # Generate points for an irregular polygon
        num_points = random.randint(8, 12)
        points = []
        center = (self.size // 2, self.size // 2)
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            distance = random.uniform(0.6, 1.0) * self.size // 2
            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)
            points.append((x, y))
            
        # Draw the asteroid body
        pygame.draw.polygon(image, base_color, points)
        
        # Add craters and texture
        for _ in range(num_points // 2):
            crater_size = random.randint(self.size // 10, self.size // 6)
            crater_x = random.randint(crater_size, self.size - crater_size)
            crater_y = random.randint(crater_size, self.size - crater_size)
            
            # Only draw craters if they're within the asteroid
            center_to_crater = math.sqrt((crater_x - center[0])**2 + (crater_y - center[1])**2)
            if center_to_crater < (self.size // 2) * 0.7:
                crater_color = (100, 50, 50)  # Darker color for craters
                pygame.draw.circle(image, crater_color, (crater_x, crater_y), crater_size)
                
                # Add highlight to crater (3D effect)
                highlight_color = (169, 99, 49)  # Lighter brown
                pygame.draw.circle(image, highlight_color, 
                                   (crater_x - crater_size//4, crater_y - crater_size//4), 
                                   crater_size//4)
                
        return image
        
    def update(self):
        self.rect.y += self.speed
        
        # Rotate asteroid for more dynamic movement
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
            
        return self.rect.top > SCREEN_HEIGHT
        
    def draw(self, surface):
        # Rotate the asteroid image
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rotated_rect)

class Explosion:
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.current_frame = 0
        self.max_frames = 12
        self.frames_per_update = 2
        self.frame_counter = 0
        
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frames_per_update:
            self.current_frame += 1
            self.frame_counter = 0
        return self.current_frame >= self.max_frames
        
    def draw(self, surface):
        # Calculate explosion size based on current frame
        current_size = int(self.size * (1 - self.current_frame / self.max_frames))
        
        # Draw explosion as a series of circles with decreasing opacity
        colors = [
            (255, 200, 0, 255 - (255 * self.current_frame // self.max_frames)),  # Yellow
            (255, 100, 0, 200 - (200 * self.current_frame // self.max_frames)),  # Orange
            (255, 0, 0, 150 - (150 * self.current_frame // self.max_frames))     # Red
        ]
        
        for i, color in enumerate(colors):
            explosion_surf = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            factor = 0.6 + (i * 0.2)  # Size factor for different layers
            pygame.draw.circle(explosion_surf, color, 
                              (current_size, current_size), 
                              int(current_size * factor))
            surface.blit(explosion_surf, 
                        (self.position[0] - current_size, self.position[1] - current_size))

class Star:
    def __init__(self):
        self.image = self.create_star_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - STAR_SIZE)
        self.rect.y = -STAR_SIZE
        self.speed = STAR_SPEED
        
    def create_star_image(self):
        # Create a golden star
        image = pygame.Surface((STAR_SIZE, STAR_SIZE), pygame.SRCALPHA)
        
        # Generate points for a 5-pointed star
        points = []
        center = (STAR_SIZE // 2, STAR_SIZE // 2)
        outer_radius = STAR_SIZE // 2
        inner_radius = STAR_SIZE // 4
        
        for i in range(10):
            angle = math.pi / 2 + 2 * math.pi * i / 10
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center[0] + radius * math.cos(angle)
            y = center[1] - radius * math.sin(angle)
            points.append((x, y))
            
        # Draw the star with a gradient from gold to yellow
        main_color = (255, 215, 0)  # Gold
        pygame.draw.polygon(image, main_color, points)
        
        # Add glow effect
        glow_surf = pygame.Surface((STAR_SIZE + 10, STAR_SIZE + 10), pygame.SRCALPHA)
        glow_color = (255, 255, 200, 100)  # Semi-transparent yellow
        pygame.draw.circle(glow_surf, glow_color, 
                          (STAR_SIZE // 2 + 5, STAR_SIZE // 2 + 5), 
                          STAR_SIZE // 2 + 5)
        
        # Create the final image with glow
        final_image = pygame.Surface((STAR_SIZE + 10, STAR_SIZE + 10), pygame.SRCALPHA)
        final_image.blit(glow_surf, (0, 0))
        final_image.blit(image, (5, 5))
        
        return final_image
        
    def update(self):
        self.rect.y += self.speed
        return self.rect.top > SCREEN_HEIGHT
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class StarField:
    def __init__(self):
        self.stars = []
        self.num_stars = 100
        self.initialize_stars()
        
    def initialize_stars(self):
        for _ in range(self.num_stars):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(1, 3),
                'brightness': random.randint(100, 255)
            })
    
    def update(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, surface):
        for star in self.stars:
            brightness = star['brightness']
            pygame.draw.circle(surface, (brightness, brightness, brightness), 
                             (int(star['x']), int(star['y'])), 
                             star['size'])

# Add this class after the Star class
class PowerStar:
    def __init__(self):
        self.size = STAR_SIZE
        self.image = self.create_power_star_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.rect.y = -self.size
        self.speed = STAR_SPEED - 1  # Slower than regular stars
        self.glow_factor = 0  # For pulsing effect
        self.glow_direction = 1  # 1 for increasing, -1 for decreasing
        
    def create_power_star_image(self):
        # Create a silver power star
        base_image = pygame.Surface((self.size + 10, self.size + 10), pygame.SRCALPHA)
        
        # Generate points for a 5-pointed star
        points = []
        center = (self.size // 2 + 5, self.size // 2 + 5)
        outer_radius = self.size // 2
        inner_radius = self.size // 4
        
        for i in range(10):
            angle = math.pi / 2 + 2 * math.pi * i / 10
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center[0] + radius * math.cos(angle)
            y = center[1] - radius * math.sin(angle)
            points.append((x, y))
            
        # Draw the star with silver color
        star_color = (192, 192, 192)  # Silver
        pygame.draw.polygon(base_image, star_color, points)
        
        # Add metallic highlight
        highlight_points = []
        for i in range(5):
            idx = i * 2
            highlight_points.append(points[idx])
            
        highlight_color = (220, 220, 220)  # Lighter silver
        if len(highlight_points) >= 3:  # Need at least 3 points for a polygon
            pygame.draw.polygon(base_image, highlight_color, highlight_points)
            
        return base_image
        
    def update(self):
        self.rect.y += self.speed
        
        # Update glow effect
        self.glow_factor += 0.1 * self.glow_direction
        if self.glow_factor >= 1.0:
            self.glow_direction = -1
        elif self.glow_factor <= 0.0:
            self.glow_direction = 1
            
        return self.rect.top > SCREEN_HEIGHT
        
    def draw(self, surface):
        # Draw with pulsing glow effect
        glow_size = int(self.size + 20 * self.glow_factor)
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_color = (200, 200, 255, 100)  # Blue-ish glow
        
        pygame.draw.circle(glow_surf, glow_color, 
                          (glow_size // 2, glow_size // 2), 
                          glow_size // 2)
        
        # Position glow and base image
        glow_x = self.rect.centerx - glow_size // 2
        glow_y = self.rect.centery - glow_size // 2
        surface.blit(glow_surf, (glow_x, glow_y))
        surface.blit(self.image, self.rect)

class Heart:
    def __init__(self, x, y):
        self.size = 20
        self.image = self.create_heart_image()
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.speed = 2
        self.pulse_value = 0
        self.pulse_dir = 1
        
    def create_heart_image(self):
        image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Draw heart shape
        heart_color = (255, 0, 0)  # Red
        
        # Draw the two circles for the top of the heart
        pygame.draw.circle(image, heart_color, 
                          (self.size // 4, self.size // 4), 
                          self.size // 4)
        pygame.draw.circle(image, heart_color, 
                          (self.size - self.size // 4, self.size // 4), 
                          self.size // 4)
        
        # Draw the bottom triangle part
        pygame.draw.polygon(image, heart_color, [
            (0, self.size // 4),
            (self.size // 2, self.size),
            (self.size, self.size // 4)
        ])
        
        return image
        
    def update(self):
        self.rect.y += self.speed
        
        # Pulse effect
        self.pulse_value += 0.05 * self.pulse_dir
        if self.pulse_value >= 1.0:
            self.pulse_dir = -1
        elif self.pulse_value <= 0.0:
            self.pulse_dir = 1
            
        return self.rect.top > SCREEN_HEIGHT
        
    def draw(self, surface):
        # Draw with pulsing glow effect
        pulse_size = int(self.size * (1.2 + 0.2 * self.pulse_value))
        glow_surf = pygame.Surface((pulse_size, pulse_size), pygame.SRCALPHA)
        glow_color = (255, 100, 100, 100)  # Red glow
        
        pygame.draw.circle(glow_surf, glow_color, 
                          (pulse_size // 2, pulse_size // 2), 
                          pulse_size // 2)
        
        # Position glow and heart image
        glow_x = self.rect.centerx - pulse_size // 2
        glow_y = self.rect.centery - pulse_size // 2
        surface.blit(glow_surf, (glow_x, glow_y))
        surface.blit(self.image, self.rect)

# Add this class after the Star class
class AlienBoss:
    def __init__(self):
        self.size = 100  # Larger size
        self.image = self.create_alien_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = 50
        self.speed = 4
        self.health = 15  # More health
        self.direction = 1  # 1 for right, -1 for left
        self.shoot_cooldown = 0
        self.shoot_delay = 25  # Faster shooting
        self.energy_pulse = 0  # For energy field effect
        
    def create_alien_image(self):
        # Create intimidating dark alien spaceship
        image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Main body (angular and aggressive)
        body_color = (20, 20, 20)  # Almost black
        
        # Ship body - menacing shape
        points = [
            (self.size//2, 0),  # Front tip
            (self.size//5, self.size//3),  # Left wing front
            (0, self.size//2),  # Left wing tip
            (self.size//5, self.size*2//3),  # Left wing rear
            (self.size//3, self.size*3//4),  # Left rear
            (self.size*2//3, self.size*3//4),  # Right rear
            (self.size*4//5, self.size*2//3),  # Right wing rear
            (self.size, self.size//2),  # Right wing tip
            (self.size*4//5, self.size//3),  # Right wing front
        ]
        pygame.draw.polygon(image, body_color, points)
        
        # Energy core (pulsing in the update method)
        core_color = (150, 0, 0)  # Deep red
        pygame.draw.circle(image, core_color, 
                          (self.size//2, self.size//2), 
                          self.size//6)
        
        # Detail lines (tech patterns)
        line_color = (70, 70, 70)  # Dark gray
        
        # Wing patterns
        pygame.draw.line(image, line_color, 
                        (self.size//5, self.size//3), 
                        (self.size//5, self.size*2//3), 2)
        pygame.draw.line(image, line_color, 
                        (self.size*4//5, self.size//3), 
                        (self.size*4//5, self.size*2//3), 2)
        
        # Front "windshield" pattern
        pygame.draw.polygon(image, (40, 40, 40), [
            (self.size*2//5, self.size//5),
            (self.size//2, self.size//10),
            (self.size*3//5, self.size//5),
            (self.size*3//5, self.size*2//5),
            (self.size//2, self.size//2),
            (self.size*2//5, self.size*2//5)
        ])
        
        # Engine exhausts (red glow)
        exhaust_color = (200, 0, 0)
        pygame.draw.rect(image, exhaust_color, 
                        pygame.Rect(self.size*1//4, self.size*3//4, self.size//6, self.size//8))
        pygame.draw.rect(image, exhaust_color, 
                        pygame.Rect(self.size*5//8, self.size*3//4, self.size//6, self.size//8))
        
        # Weapon mounts
        weapon_color = (50, 50, 50)
        pygame.draw.circle(image, weapon_color, 
                          (self.size//4, self.size*2//3), self.size//12)
        pygame.draw.circle(image, weapon_color, 
                          (self.size*3//4, self.size*2//3), self.size//12)
        
        return image
        
    def update(self):
        # Move side to side
        self.rect.x += self.speed * self.direction
        
        # Change direction if reaching screen edge
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
            
        # Handle shooting cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Update energy pulse effect
        self.energy_pulse = (self.energy_pulse + 1) % 20
            
    def fire_missile(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            # Fire from both weapon mounts
            missiles = []
            missile_left_x = self.rect.left + self.size // 4 - MISSILE_SIZE // 2
            missile_right_x = self.rect.left + self.size * 3 // 4 - MISSILE_SIZE // 2
            missile_y = self.rect.bottom - 10
            
            missiles.append(AlienMissile(missile_left_x, missile_y))
            missiles.append(AlienMissile(missile_right_x, missile_y))
            return missiles
        return None
        
    def draw(self, surface):
        # Draw energy field effect
        if self.energy_pulse < 10:
            field_size = self.size + 10 + self.energy_pulse
            field_surf = pygame.Surface((field_size, field_size), pygame.SRCALPHA)
            field_color = (100, 0, 0, 100 - self.energy_pulse * 10)  # Fading red
            pygame.draw.circle(field_surf, field_color, 
                             (field_size // 2, field_size // 2), 
                             field_size // 2)
            surface.blit(field_surf, 
                       (self.rect.centerx - field_size // 2, 
                        self.rect.centery - field_size // 2))
        
        # Draw the ship
        surface.blit(self.image, self.rect)
        
        # Draw health bar above alien
        health_width = self.size * (self.health / 15)
        pygame.draw.rect(surface, (100, 0, 0), 
                        pygame.Rect(self.rect.x, self.rect.y - 10, self.size, 5))
        pygame.draw.rect(surface, (255, 0, 0), 
                        pygame.Rect(self.rect.x, self.rect.y - 10, health_width, 5))
        
# Add this class after the AlienBoss class
class AlienMissile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, MISSILE_SIZE, MISSILE_SIZE * 1.5)
        self.speed = MISSILE_SPEED - 2  # Slightly slower than player missiles
        
    def update(self):
        self.rect.y += self.speed
        return self.rect.top > SCREEN_HEIGHT
        
    def draw(self, surface):
        # Draw alien missile (green)
        pygame.draw.rect(surface, (50, 255, 50), self.rect)
        
        # Draw missile tip
        pygame.draw.polygon(surface, (150, 255, 150), [
            (self.rect.left, self.rect.bottom - MISSILE_SIZE * 0.5),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.right, self.rect.bottom - MISSILE_SIZE * 0.5)
        ])
        
        # Draw exhaust trail (green)
        trail_color = (100, 255, 100, 128)
        trail_surface = pygame.Surface((MISSILE_SIZE, MISSILE_SIZE), pygame.SRCALPHA)
        pygame.draw.polygon(trail_surface, trail_color, [
            (0, MISSILE_SIZE),
            (MISSILE_SIZE // 2, 0),
            (MISSILE_SIZE, MISSILE_SIZE)
        ])
        surface.blit(trail_surface, (self.rect.left, self.rect.top - MISSILE_SIZE))

# Replace the Game class with this updated version
class Game:
    def __init__(self):
        self.player = Player()
        self.missiles = []
        self.asteroids = []
        self.stars = []
        self.power_stars = []
        self.hearts = []
        self.explosions = []
        self.alien_missiles = []
        self.alien_boss = None
        self.boss_appears_at = 700  # Points threshold
        self.boss_spawn_interval = 700  # Points between boss spawns
        self.score = 0
        self.lives = 5  # Updated to 5 lives
        self.game_over = False
        self.asteroid_timer = 0
        self.star_timer = 0
        self.power_star_timer = 0
        self.asteroid_spawn_rate = ASTEROID_SPAWN_RATE * 1.5  # Reduced frequency
        self.power_star_spawn_rate = 450  # Reduced frequency
        self.powered_up = False
        self.power_up_time = 0
        self.power_up_duration = 30 * FPS  # 30 seconds at 60 FPS
        self.font = pygame.font.SysFont(None, 36)
        self.star_field = StarField()  # Add starfield
        
    def spawn_objects(self):
        # Spawn asteroids
        self.asteroid_timer += 1
        if self.asteroid_timer >= self.asteroid_spawn_rate:
            self.asteroids.append(Asteroid())
            self.asteroid_timer = 0
            
        # Spawn stars
        self.star_timer += 1
        if self.star_timer >= STAR_SPAWN_RATE:
            self.stars.append(Star())
            self.star_timer = 0
            
        # Spawn power stars (more rare)
        self.power_star_timer += 1
        if self.power_star_timer >= self.power_star_spawn_rate:
            self.power_stars.append(PowerStar())
            self.power_star_timer = 0
            
        # Check if it's time to spawn a boss
        if self.score >= self.boss_appears_at and self.alien_boss is None:
            self.alien_boss = AlienBoss()
            self.boss_appears_at += self.boss_spawn_interval
    
    def fire_power_missiles(self):
        # Fire a more powerful missile when powered up
        if self.player.cooldown == 0:
            self.player.cooldown = PLAYER_COOLDOWN
            # Fire power missile
            missile_x = self.player.rect.centerx - MISSILE_SIZE // 2
            missile_y = self.player.rect.top
            self.missiles.append(PowerMissile(missile_x, missile_y))
            
    def update(self):
        if self.game_over:
            return
            
        # Update starfield
        self.star_field.update()
            
        # Update player
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        
        # Handle missile firing
        if keys[pygame.K_SPACE]:
            if self.powered_up:
                self.fire_power_missiles()
            else:
                missile = self.player.fire_missile()
                if missile:
                    self.missiles.append(missile)
        
        # Update power-up timer
        if self.powered_up:
            self.power_up_time += 1
            if self.power_up_time >= self.power_up_duration:
                self.powered_up = False
                self.power_up_time = 0
        
        # Spawn new objects
        self.spawn_objects()
        
        # Update missiles
        for missile in self.missiles[:]:
            if missile.update():
                self.missiles.remove(missile)
        
        # Update alien missiles
        for missile in self.alien_missiles[:]:
            if missile.update():
                self.alien_missiles.remove(missile)
            elif self.player.rect.colliderect(missile.rect):
                self.alien_missiles.remove(missile)
                self.lives -= 1
                self.explosions.append(Explosion((self.player.rect.centerx, self.player.rect.centery), 30))
                if self.lives <= 0:
                    self.game_over = True
        
        # Update hearts
        for heart in self.hearts[:]:
            if heart.update():
                self.hearts.remove(heart)
            elif self.player.rect.colliderect(heart.rect):
                self.hearts.remove(heart)
                self.lives += 1
                # Play a sound or special effect for life up
        
        # Update asteroids and check collisions
        for asteroid in self.asteroids[:]:
            if asteroid.update():
                self.asteroids.remove(asteroid)
            elif self.player.rect.colliderect(asteroid.rect):
                self.asteroids.remove(asteroid)
                self.explosions.append(Explosion(asteroid.rect.center, asteroid.size))
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
            else:
                # Check missile-asteroid collisions
                for missile in self.missiles[:]:
                    if missile.rect.colliderect(asteroid.rect):
                        self.missiles.remove(missile)
                        self.asteroids.remove(asteroid)
                        self.explosions.append(Explosion(asteroid.rect.center, asteroid.size))
                        # Power missiles give more points
                        if isinstance(missile, PowerMissile):
                            self.score += 30
                        else:
                            self.score += 20
                        break
        
        # Update regular stars
        for star in self.stars[:]:
            if star.update():
                self.stars.remove(star)
            elif self.player.rect.colliderect(star.rect):
                self.stars.remove(star)
                self.score += 10
        
        # Update power stars
        for power_star in self.power_stars[:]:
            if power_star.update():
                self.power_stars.remove(power_star)
            elif self.player.rect.colliderect(power_star.rect):
                self.power_stars.remove(power_star)
                self.powered_up = True
                self.power_up_time = 0
                self.score += 25
        
        # Update alien boss if present
        if self.alien_boss:
            self.alien_boss.update()
            
            # Boss firing
            alien_missiles = self.alien_boss.fire_missile()
            if alien_missiles:
                self.alien_missiles.extend(alien_missiles)
                
            # Check player missiles hitting the boss
            for missile in self.missiles[:]:
                if missile.rect.colliderect(self.alien_boss.rect):
                    self.missiles.remove(missile)
                    # Power missiles do more damage
                    if isinstance(missile, PowerMissile):
                        self.alien_boss.health -= 2
                    else:
                        self.alien_boss.health -= 1
                    self.explosions.append(Explosion((missile.rect.centerx, missile.rect.centery), 20))
                    
                    # Boss destroyed
                    if self.alien_boss.health <= 0:
                        self.explosions.append(Explosion(self.alien_boss.rect.center, self.alien_boss.size))
                        self.score += 100
                        # Drop heart when boss is defeated
                        self.hearts.append(Heart(self.alien_boss.rect.centerx, self.alien_boss.rect.centery))
                        self.alien_boss = None
                        break
                
        # Update explosions
        for explosion in self.explosions[:]:
            if explosion.update():
                self.explosions.remove(explosion)
                
    def draw(self):
        # Clear screen
        screen.fill(BACKGROUND_COLOR)
        
        # Draw starfield
        self.star_field.draw(screen)
        
        # Draw stars
        for star in self.stars:
            star.draw(screen)
            
        # Draw power stars
        for power_star in self.power_stars:
            power_star.draw(screen)
            
        # Draw hearts
        for heart in self.hearts:
            heart.draw(screen)
            
        # Draw missiles
        for missile in self.missiles:
            missile.draw(screen)
            
        # Draw alien missiles
        for missile in self.alien_missiles:
            missile.draw(screen)
            
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(screen)
            
        # Draw alien boss if present
        if self.alien_boss:
            self.alien_boss.draw(screen)
            
        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(screen)
            
        # Draw player
        self.player.draw(screen)
        
        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        control_text = self.font.render("← → ↑ ↓: Move   SPACE: Fire", True, (200, 200, 200))
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(control_text, (SCREEN_WIDTH - control_text.get_width() - 10, 10))
        
        # Draw power-up status if active
        if self.powered_up:
            power_up_text = self.font.render("POWER-UP ACTIVE!", True, (100, 200, 255))
            time_left = (self.power_up_duration - self.power_up_time) // FPS
            timer_text = self.font.render(f"Time: {time_left}s", True, (100, 200, 255))
            screen.blit(power_up_text, (SCREEN_WIDTH // 2 - power_up_text.get_width() // 2, 10))
            screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 50))
        
        # Draw alien boss approaching message if relevant
        if self.alien_boss and self.alien_boss.rect.y < 80:
            warning_text = self.font.render("WARNING: ALIEN BOSS APPROACHING!", True, (255, 50, 50))
            screen.blit(warning_text, (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, 100))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, (255, 200, 0))
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            screen.blit(final_score_text, final_score_rect)
            
        # Update display
        pygame.display.flip()
        
    def restart(self):
        self.__init__()

def main():
    game = Game()
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game.restart()
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update game state
        game.update()
        
        # Render game
        game.draw()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
