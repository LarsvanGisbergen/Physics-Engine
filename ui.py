import math
import pygame
import sys

import pygame
import sys
from physics import *

class PygameWindow:
    def __init__(self, width, height):      
        pygame.init()
        
        # Set up the window
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        pygame.display.set_caption("Pygame Particle Example")
        
        self.first_click_pos = None
        
        self.WHITE = (255, 255, 255)
        
        self.running = True

        self.physics = PhysicsEngine()
        
        self.font = pygame.font.Font(None, 24)  # Example font and font size
        self.instructions = {
            "left_click": "Left-click: Place a particle",
            "right_click": "Right-click: Place a particle, Right-click 2: Release particle with initial velocity and direction"
        }

        
        
    def draw(self):
        self.screen.fill(self.WHITE)
        
        # Draw instructions at the top of the screen
        instructions_surface = self.font.render(self.instructions["left_click"] + " | " +
                                                self.instructions["right_click"], True, (0, 0, 0))
        instructions_rect = instructions_surface.get_rect()
        instructions_rect.topleft = (0, 0)
        self.screen.blit(instructions_surface, instructions_rect)
        
        for particle in self.physics.get_particles():
            particle.draw(self.screen)
        
        # Update the display
        pygame.display.flip()

    def on_click(self, pos, button):
        # Particles capped
        if self.physics.max_particles_reached():
            return

        if button == 1:  # Left-click
            # Create a new particle at the cursor position with no initial velocity
            x, y = pos
            self.physics.add_particle_with_coords(x, y)
            self.first_click_pos = None

        elif button == 3:  # Right-click
            if self.first_click_pos is None:
                # Register the first right-click
                self.first_click_pos = pos
            else:
                x1, y1 = self.first_click_pos
                x2, y2 = pos
                self.physics.add_particle_with_initial_velocity(x1, y1, x2, y2)
                self.first_click_pos = None
        
        
        

    def run(self, framerate):
        clock = pygame.time.Clock()
        dt = clock.tick(framerate) / 1000.0  # Delta time in seconds
       
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event.pos, event.button)
            
            self.physics.cleanup_particles(self.screen_height, self.screen_width)
            self.physics.tick(dt)
            self.draw()
            
        
        # Quit Pygame
        pygame.quit()
        sys.exit()