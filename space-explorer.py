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

class Game:
    def __init__(self):
        self.player = Player()
        self.missiles = []
        self.asteroids = []
        self.stars = []
        self.explosions = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.asteroid_timer = 0
        self.star_timer = 0
        self.font = pygame.font.SysFont(None, 36)
        
    def spawn_objects(self):
        # Spawn asteroids
        self.asteroid_timer += 1
        if self.asteroid_timer >= ASTEROID_SPAWN_RATE:
            self.asteroids.append(Asteroid())
            self.asteroid_timer = 0
            
        # Spawn stars
        self.star_timer += 1
        if self.star_timer >= STAR_SPAWN_RATE:
            self.stars.append(Star())
            self.star_timer = 0
            
    def update(self):
        if self.game_over:
            return
            
        # Update player
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        
        # Handle missile firing
        if keys[pygame.K_SPACE]:
            missile = self.player.fire_missile()
            if missile:
                self.missiles.append(missile)
        
        # Spawn new objects
        self.spawn_objects()
        
        # Update missiles
        for missile in self.missiles[:]:
            if missile.update():
                self.missiles.remove(missile)
        
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
                        self.score += 20
                        break
        
        # Update stars
        for star in self.stars[:]:
            if star.update():
                self.stars.remove(star)
            elif self.player.rect.colliderect(star.rect):
                self.stars.remove(star)
                self.score += 10
                
        # Update explosions
        for explosion in self.explosions[:]:
            if explosion.update():
                self.explosions.remove(explosion)
                
    def draw(self):
        # Clear screen
        screen.fill(BACKGROUND_COLOR)
        
        # Draw stars
        for star in self.stars:
            star.draw(screen)
            
        # Draw missiles
        for missile in self.missiles:
            missile.draw(screen)
            
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(screen)
            
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
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)
            
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
