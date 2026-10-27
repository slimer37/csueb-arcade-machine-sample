import pygame
import math
from pygame.math import Vector2
import pygame.gfxdraw
import random

class OrbitingCircle:
	def __init__(self, orbit_center: Vector2, orbit_distance: float, position: float, speed: float, radius: float, color: pygame.Color):
		self.orbit_center = orbit_center
		self.orbit_distance = orbit_distance
		self.position = position
		self.speed = speed
		self.radius = radius
		self.color = color
		
	def draw(self, screen: pygame.Surface, deltaTime: float):
		self.position += self.speed * deltaTime
		pos = self.orbit_center + Vector2(math.cos(self.position), math.sin(self.position)) * self.orbit_distance
		pygame.gfxdraw.aacircle(screen, int(pos.x), int(pos.y), int(self.radius), self.color)
		pygame.gfxdraw.filled_circle(screen, int(pos.x), int(pos.y), int(self.radius), self.color)
		#pygame.draw.circle(screen, self.color, pos, self.radius)


screen_size = (1280, 720)

center = (screen_size[0] / 2, screen_size[1] / 2)

max_distance = math.sqrt(center[0]**2 + center[1]**2)

circles = []

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
		
		circles.append(OrbitingCircle(center, distance, position, speed, radius, color))

def draw(screen: pygame.Surface, deltaTime: float):
	for c in circles:
		c.draw(screen, deltaTime)
