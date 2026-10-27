import pygame
import math
from pygame.math import Vector2
import pygame.gfxdraw
import pygame.transform
import random

class OrbitingCircle:
	def __init__(self, orbit_center: Vector2, orbit_distance: float, position: float, speed: float, radius: float, color: pygame.Color, reactivity: float):
		self.orbit_center = orbit_center
		self.orbit_distance = orbit_distance
		self.position = position
		self.speed = speed
		self.radius = radius
		self.color = color
		self.reactivity = reactivity
		self.smooth_offset = Vector2()
		
	def draw(self, screen: pygame.Surface, deltaTime: float):
		self.position += self.speed * deltaTime
		pos = self.orbit_center + Vector2(math.cos(self.position), math.sin(self.position)) * self.orbit_distance
		
		direction = push_distance - self.smooth_offset
		
		if direction.length() > self.reactivity:
			direction.normalize_ip()
			self.smooth_offset += direction * self.reactivity * deltaTime
		else:
			self.smooth_offset = push_distance
		
		pos += self.smooth_offset
		
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
		
		circles.append(OrbitingCircle(center, distance, position, speed, radius, color, random.uniform(0, 2)))

def draw(screen: pygame.Surface, deltaTime: float):
	for c in circles:
		c.draw(screen, deltaTime)
