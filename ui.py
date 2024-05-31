import math
import pygame
import sys

import pygame
import sys
from Objects.particle import Particle

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
        
        # List to hold particles
        self.particles = []
        self.max_particles = 10

    def draw(self):
        self.screen.fill(self.WHITE)
        
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Update the display
        pygame.display.flip()

    def on_click(self, pos):
        # particles capped
        if len(self.particles) > self.max_particles-1:
            return
        
        # Create a new particle at the cursor position
        x, y = pos
        new_particle = Particle(x, y)
        self.particles.append(new_particle)

    def run(self, framerate):
        clock = pygame.time.Clock()
        
       
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event.pos)
            
            dt = clock.tick(framerate) / 1000.0  # Delta time in seconds


            # gravity
            for particle in self.particles:
                if len(self.particles) < 2:
                    continue
                force_x = 0
                force_y = 0
                for other_particle in self.particles:
                    if particle is other_particle:
                        continue                   
                    mass_square = particle.mass * other_particle.mass
                    delta_x = particle.x - other_particle.x
                    delta_y = particle.y - other_particle.y
                    r_square = delta_x**2 + delta_y**2
                    if r_square == 0 or r_square < particle.radius**2 or r_square < other_particle.radius**2:
                        self.particles.remove(particle)
                        self.particles.remove(other_particle)
                        new_radius = max(particle.radius, other_particle.radius) + 0.2*min(particle.radius, other_particle.radius)
                        collision_particle = Particle(particle.x,particle.y,particle.mass+other_particle.mass, new_radius)
                        collision_particle.vx = particle.vx + other_particle.vx
                        collision_particle.vy = particle.vy + other_particle.vy
                        self.particles.append(collision_particle)
                        break
                    force = mass_square/r_square
                    force_per_unit = force / r_square
                    force_x -= delta_x*force_per_unit
                    force_y -= delta_y*force_per_unit

                particle.apply_force(force_x, force_y)
                particle.update(dt)
            

            # draw particles
            for particle in self.particles:  
                particle.draw(self.screen)

                
            self.draw()
            
        
        # Quit Pygame
        pygame.quit()
        sys.exit()