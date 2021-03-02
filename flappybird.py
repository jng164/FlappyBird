import pygame, sys,random
import os#operating system, path to images

WIDTH,HEIGHT = 500,650
BIRD_WIDTH,BIRD_HEIGHT = 40,30
PIPE_WIDTH= 60
WHITE = (255,255,255)

#PARAMETERS OF THE GAME
GRAVITY = 0.15 #GRAVITY
bird_movement = 0
BIRD_VELOCITY = 4
FPS = 120

game_active = True
score = 0
high_score = 0
can_score = True

pygame.init()


game_font = pygame.font.Font('04B_19.ttf',30)
WIN = pygame.display.set_mode((WIDTH,HEIGHT))#window


pygame.display.set_caption("Flappy Bird!")#titol window


BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "background-day.png")), (WIDTH,HEIGHT))
FLOOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "base.png")), (WIDTH,HEIGHT//8))

bird_downflap = pygame.transform.scale(pygame.image.load('Assets/bluebird-downflap.png'),(BIRD_WIDTH,BIRD_HEIGHT))
bird_midflap = pygame.transform.scale(pygame.image.load('Assets/bluebird-midflap.png'),(BIRD_WIDTH,BIRD_HEIGHT))
bird_upflap = pygame.transform.scale(pygame.image.load('Assets/bluebird-upflap.png'),(BIRD_WIDTH,BIRD_HEIGHT))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center =(100,HEIGHT//2))#center of the rectangle is in the 100,HEIGHT/2

BIRDFLAP = pygame.USEREVENT +1
pygame.time.set_timer(BIRDFLAP, 200)#200 ms


game_over_surface = pygame.transform.scale(pygame.image.load('Assets/message.png'), (WIDTH//2, HEIGHT//2))
game_over_rect = game_over_surface.get_rect(center=(WIDTH//2,HEIGHT//2))





#PIPE_SURFACE = pygame.transform.scale((pygame.image.load('Assets/pipe-green.png')), (PIPE_WIDTH,PIPE_HEIGHT))
pipe_list=[]
SPAWNPIPE = pygame.USEREVENT 
pygame.time.set_timer(SPAWNPIPE,1200)#miliseconds, an event is gonna be triggered every 1.2sec
pipe_height = [HEIGHT//2,int(0.6*HEIGHT), int(0.4*HEIGHT), int(0.7*HEIGHT)]

def create_pipe():
	global PIPE_SURFACE
	PIPE_HEIGHT = random.choice(pipe_height)
	PIPE_SURFACE = pygame.transform.scale((pygame.image.load('Assets/pipe-green.png')), (PIPE_WIDTH,PIPE_HEIGHT))
	
	

	bottom_pipe = PIPE_SURFACE.get_rect(midtop =(WIDTH,HEIGHT - PIPE_HEIGHT))
	
	top_pipe = PIPE_SURFACE.get_rect(midbottom =(WIDTH,HEIGHT - PIPE_HEIGHT-BIRD_HEIGHT-100))
	return bottom_pipe,top_pipe #returns a tupple


def move_pipes(pipes):

	for pipe in pipes:
		pipe.centerx -= 3

	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]#copies de list but all the pipes that left the screen
	return visible_pipes

def check_collision(pipes):
	global can_score
	for pipe in pipes:
		if bird_rect.colliderect(pipe): #returns True
			can_score = True
			#print("Collision")
			return False

	if bird_rect.top <= -BIRD_HEIGHT//2 or bird_rect.bottom >= HEIGHT-FLOOR.get_height()-BIRD_HEIGHT//2:
		#print("Collision")
		can_score = True	
		return False

	return True

	
def draw_floor():
	WIN.blit(FLOOR, (floor_x_pos,HEIGHT-FLOOR.get_height()))#Space BackGround
	WIN.blit(FLOOR, (floor_x_pos + WIDTH,HEIGHT-FLOOR.get_height()))
	

def rotate_bird(bird_surface):
	new_bird = pygame.transform.rotozoom(bird_surface,-bird_movement*3, 1)#escale or rotate
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center=(100,bird_rect.centery))
	return new_bird, new_bird_rect
	
	

		
def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= HEIGHT:
			WIN.blit(PIPE_SURFACE, pipe)

		else:
			flip_pipe = pygame.transform.flip(PIPE_SURFACE, False, True)#Flipping in x direction(FALSE), flipping in Y direction(TRUE)
			WIN.blit(flip_pipe, pipe)

def score_display(game_state):
	if game_state == "main_game":
		score_surface = game_font.render(str(int(score)),True, WHITE)
		score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
		WIN.blit(score_surface,score_rect)

	if game_state == "game_over":
		score_surface = game_font.render(f'Score: {int(score)}',True, WHITE)
		score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
		WIN.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High Score: {int(high_score)}',True, WHITE)
		high_score_rect = score_surface.get_rect(center=(WIDTH//2-50, 550))
		WIN.blit(high_score_surface,high_score_rect)


def update_score(score,high_score):
	if score>high_score:
		high_score = score
	return high_score

def pipe_score_check():
	global can_score,score

	if pipe_list:
		for pipe in pipe_list:
			if 98 < pipe.centerx <102 and can_score:
				score +=1
				can_score = False
			if pipe.centerx < 0:
				can_score = True

def main():
	global floor_x_pos,bird_movement,pipe_height, game_active, bird_surface, bird_rect, bird_index,high_score,score
	
	clock = pygame.time.Clock()
	run = True
	
	floor_x_pos = 0
	while run:
		
		


		clock.tick(FPS)#controls the speed of the while loop,consistent at different computers

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				
				pygame.quit()#quit pygame close the window
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and game_active:

					bird_movement = 0				
					bird_movement -= BIRD_VELOCITY
					

				if event.key == pygame.K_SPACE and game_active == False:
					game_active = True
					pipe_list.clear()
					bird_rect.center = (100,HEIGHT//2)
					bird_movement=0
					score = 0
					

			if event.type == SPAWNPIPE:
				pipe_list.extend(create_pipe())#

			if event.type == BIRDFLAP:
				if bird_index<2:
					bird_index += 1
				else:
					bird_index = 0

				bird_surface, bird_rect = bird_animation()

		WIN.blit(BACKGROUND, (0,0))#Space BackGround

		if game_active:

			#bird into screen, yposition changes with BIRD_RECT.centery
		#BIRD_MOVEMENT
			bird_movement += GRAVITY
			rotated_bird = rotate_bird(bird_surface)
			
			bird_rect.centery += bird_movement
			WIN.blit(rotated_bird,bird_rect)
			
			
			
			#pipes
			pipes = move_pipes(pipe_list)
			draw_pipes(pipes)
			game_active =check_collision(pipe_list)


			#Score
			pipe_score_check()
			score_display("main_game")
		else:
			WIN.blit(game_over_surface, game_over_rect)
			high_score = update_score(score,high_score)
			score_display("game_over")
		
		floor_x_pos -= 1
		if floor_x_pos <= -WIDTH:
			floor_x_pos = 0

		draw_floor()
		pygame.display.update()


	



if __name__ == "__main__":#we only run the game when we run this file 
	main()