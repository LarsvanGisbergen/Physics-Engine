from Objects.particle import *
import numpy as np

class PhysicsEngine:
    def __init__(self):
        self.particles = []
        self.max_particles = 5


    def update_forces(self):
        if len(self.particles) < 2:
            return

        to_remove = set()
        new_particles = []

        for i, particle in enumerate(self.particles):
            force_x = 0
            force_y = 0

            for j, other_particle in enumerate(self.particles):
                if i == j or particle in to_remove or other_particle in to_remove:
                    continue

                delta_x = particle.x - other_particle.x
                delta_y = particle.y - other_particle.y
                r_square = delta_x**2 + delta_y**2

                if r_square == 0 or r_square < max(particle.radius, other_particle.radius)**2:
                    to_remove.add(particle)
                    to_remove.add(other_particle)
                    new_mass = particle.mass + other_particle.mass
                    
                    # Calculate the new radius based on the areas
                    new_area = np.pi * (particle.radius**2 + other_particle.radius**2)
                    new_radius = (new_area / np.pi)**0.5
                    
                    new_vx = (particle.vx * particle.mass + other_particle.vx * other_particle.mass) / new_mass
                    new_vy = (particle.vy * particle.mass + other_particle.vy * other_particle.mass) / new_mass
                    
                    # Determine the position of the new particle
                    if particle.radius >= other_particle.radius:
                        new_x = particle.x
                        new_y = particle.y
                    else:
                        new_x = other_particle.x
                        new_y = other_particle.y
                    
                    new_particle = Particle(new_x, new_y, new_mass, new_radius)
                    new_particle.vx = new_vx
                    new_particle.vy = new_vy
                    new_particles.append(new_particle)
                    break

                force = particle.mass * other_particle.mass / r_square
                force_x -= delta_x * force / r_square
                force_y -= delta_y * force / r_square

            if particle not in to_remove:
                particle.vx += force_x / particle.mass
                particle.vy += force_y / particle.mass

        self.particles = [p for p in self.particles if p not in to_remove] + new_particles


                    
    def update_particles(self, dt):
        for particle in self.particles:
            particle.update(dt)
            
    # make physics engine proceed one time tick (dt)
    def tick(self, dt):
        self.update_forces()
        self.update_particles(dt)
    
    def add_particle_with_coords(self, x, y):
        new_particle = Particle(x, y)
        self.particles.append(new_particle)
    
    def add_particle(self, particle: Particle):
        self.particles.append(particle)
        
    # x1,y1 is particle placement position, x2,y2 is velocity vector position
    def add_particle_with_initial_velocity(self, x1, y1, x2, y2):           
        dx = x2 - x1
        dy = y2 - y1
        velocity_scale = 0.01  
        vx = dx * velocity_scale
        vy = dy * velocity_scale
        particle = Particle(x1, y1)
        particle.vx = vx
        particle.vy = vy
        self.add_particle(particle)
        
    def max_particles_reached(self):
        return len(self.particles) > self.max_particles-1
    
    def get_particles(self):
        return self.particles
    
    # remove particles that are out of visual bounds
    def cleanup_particles(self, screen_height, screen_width):
         particles_to_remove = []
         
         for particle in self.particles:
            if (particle.x - particle.radius < 0 or particle.x + particle.radius > screen_width or
                particle.y - particle.radius < 0 or particle.y + particle.radius > screen_height):
                particles_to_remove.append(particle)

         for particle in particles_to_remove:
            self.particles.remove(particle)
            