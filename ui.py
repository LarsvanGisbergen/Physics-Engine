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
        
        self.WHITE = (255, 255, 255)
        
        self.running = True

        self.physics = PhysicsEngine()
        
        
        

    def draw(self):
        self.screen.fill(self.WHITE)
        
        for particle in self.physics.get_particles():
            particle.draw(self.screen)
        
        # Update the display
        pygame.display.flip()

    def on_click(self, pos):
        # particles capped
        if self.physics.max_particles_reached():
            return
        
        # Create a new particle at the cursor position
        x, y = pos
        self.physics.add_particle(x,y)
        
        
        

    def run(self, framerate):
        clock = pygame.time.Clock()
        dt = clock.tick(framerate) / 1000.0  # Delta time in seconds
       
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event.pos)
            
            self.physics.tick(dt)
            self.draw()
            
        
        # Quit Pygame
        pygame.quit()
        sys.exit()