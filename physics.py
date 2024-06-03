from Objects.particle import *

class PhysicsEngine:
    def __init__(self):
        self.particles = []
        self.max_particles = 10


    def update_forces(self):
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
                    
                    

    def update_particles(self, dt):
        for particle in self.particles:
            particle.update(dt)
            

    # make physics engine proceed one time tick (dt)
    def tick(self, dt):
        self.update_forces()
        self.update_particles(dt)
    
    def add_particle(self, x, y):
        new_particle = Particle(x, y)
        self.particles.append(new_particle)
        
    def max_particles_reached(self):
        return len(self.particles) > self.max_particles-1
    
    def get_particles(self):
        return self.particles