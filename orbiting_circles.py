import pygame
import math
from pygame.math import Vector2
import pygame.gfxdraw
import pygame.transform
import random

SPRING_CONSTANT = 4
SQRT_SPRING_CONSTANT = math.sqrt(SPRING_CONSTANT)

def smooth_damp(target: float, current: float, velocity: float, deltaTime: float) -> tuple[float, float]:
	distance = target - current
	spring_force = distance * SPRING_CONSTANT
	damping_force = -velocity * 2 * SQRT_SPRING_CONSTANT
	force = spring_force + damping_force 
	velocity += force * deltaTime
	displacement = velocity * deltaTime
	return (current + displacement, velocity)
	
def smooth_damp_v2(target: Vector2, current: Vector2, velocity: Vector2, deltaTime: float) -> tuple[Vector2, Vector2]:
	pos_x, vel_x = smooth_damp(target.x, current.x, velocity.x, deltaTime)
	pos_y, vel_y = smooth_damp(target.y, current.y, velocity.y, deltaTime)
	return (Vector2(pos_x, pos_y), Vector2(vel_x, vel_y))

class OrbitingCircle:
	def __init__(self, orbit_center: Vector2, orbit_distance: float, position: float, speed: float, radius: float, color: pygame.Color, reactivity: float):
		self.orbit_center = orbit_center
		self.orbit_distance = orbit_distance
		self.position = position
		self.speed = speed
		self.radius = radius
		self.color = color
		self.reactivity = reactivity
		
	def draw(self, screen: pygame.Surface, deltaTime: float):
		self.position += self.speed * deltaTime
		pos = self.orbit_center + Vector2(math.cos(self.position), math.sin(self.position)) * self.orbit_distance
		
		pos += smooth_push_offset * self.reactivity
		
		surf = pygame.Surface((self.radius * 2 + 2,) * 2, pygame.SRCALPHA)
		
		center = math.floor(self.radius)
		r = math.floor(self.radius)
		pygame.gfxdraw.aacircle(surf, center, center, r, self.color)
		pygame.gfxdraw.filled_circle(surf, center, center, r, self.color)
		
		screen.blit(surf, surf.get_rect(center=pos))

screen_size = (1280, 720)

center = (screen_size[0] / 2, screen_size[1] / 2)

max_distance = math.sqrt(center[0]**2 + center[1]**2)

circles = []

push_distance = Vector2()
push_velocity = Vector2()
smooth_push_offset = Vector2()

def push_circles(distance: Vector2):
	global push_distance
	push_distance = distance

def generate_circles():
	circles.clear()

	for i in range(100):
		
		distance = math.sqrt(random.uniform(5, max_distance ** 2)) # try and get more even distribution farther away w/ sqrt curve
		position = random.uniform(0, 2 * math.pi)
		speed = random.uniform(0.5, 2) / (2 * math.pi) # revs per sec
		radius = random.uniform(20, 80)
		
		color = pygame.Color(0)
		
		color.hsva = (
			random.uniform(0, 360),
			random.uniform(60, 100),
			random.uniform(70, 100),
			100
		)
		
		circles.append(OrbitingCircle(center, distance, position, speed, radius, color, random.uniform(0, 1)))

def draw(screen: pygame.Surface, deltaTime: float):
	global smooth_push_offset, push_velocity
	
	smooth_push_offset, push_velocity = smooth_damp_v2(push_distance, smooth_push_offset, push_velocity, deltaTime)
	
	for c in circles:
		c.draw(screen, deltaTime)
