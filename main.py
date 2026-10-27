import pygame
import pygame.joystick
import orbiting_circles
import sys

pygame.init()

pygame.display.set_caption("Arcade Sample")

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
deltaTime = 0

fps_limit = 60

BG_COLOR = (250,) * 3
FG_COLOR = (25,) * 3

font = pygame.font.SysFont("FreeSans", 18)
minifont = pygame.font.SysFont("FreeSans", 10)

show_debug_info = False

def quit():
	pygame.quit()
	sys.exit()
	
def setup():
	orbiting_circles.generate_circles()

def frameloop():
	global show_debug_info
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit()
				
			if event.key == pygame.K_F3:
				show_debug_info = not show_debug_info
				
			if event.key == pygame.K_SPACE:
				orbiting_circles.generate_circles()
	
	screen.fill(BG_COLOR)
	
	keys = pygame.key.get_pressed()
	
	push = pygame.math.Vector2()
	
	if keys[pygame.K_UP]: push.y -= 1
	if keys[pygame.K_DOWN]: push.y += 1
	if keys[pygame.K_RIGHT]: push.x += 1
	if keys[pygame.K_LEFT]: push.x -= 1
	
	if push.length() > 0: push.normalize_ip()
	
	push *= 50
	
	orbiting_circles.push_circles(push)
	
	orbiting_circles.draw(screen, deltaTime)
	
	debug_hint_text = minifont.render(f"Press F3 to {'hide' if show_debug_info else 'show'} debug info", True, FG_COLOR)
	debug_hint_rect = debug_hint_text.get_rect(topleft=(5, 5))
	screen.blit(debug_hint_text, debug_hint_rect)
	
	if show_debug_info:
		debug_info_content = f"""Debug info:
Joysticks detected: {pygame.joystick.get_count()}
Delta time: {deltaTime:.3f}
FPS: {1 / deltaTime:.1f}
"""

		y = debug_hint_rect.bottom + 5
		for line in debug_info_content.split('\n'):
			text_surface = font.render(line, True, FG_COLOR)
			text_rect = text_surface.get_rect(topleft=(5, y))
			screen.blit(text_surface, text_rect)
			y += text_rect.height + 5

def main():	
	print("By Alfred Roy Manongsong @ CSUEB 2026")
	
	global deltaTime
	
	setup()
	
	while True:
		frameloop()
		pygame.display.flip()
		deltaTime = clock.tick(fps_limit) / 1000

if __name__ == "__main__":
	main()
