import pygame

class Particle:
    def __init__(self, x, y, mass=100, radius=10, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        # Initialize velocity and acceleration
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

    def update(self, dt):
        # Update velocity based on acceleration
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Update position based on velocity
        self.x += self.vx * dt
        self.y += self.vy * dt

    def apply_force(self, fx, fy):
        # Update acceleration based on force
        self.ax = fx
        self.ay = fy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

     

    def reset_force(self):
        # Reset acceleration
        self.ax = 0
        self.ay = 0

   
        