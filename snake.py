import pygame
import time
import random
from gameState import GameState
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 400
dis_height = 400




dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game AI')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 100

 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("arial", 35)
 

 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
 
def gameLoop():
    game_over = False
    game_close = False
    steps_since_food_eaten = 0
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    curr_food_location = set([foodx,foody])
    while not game_over:
 
        while game_close == True:
            #time.sleep(10)
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
              
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        # Human player
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         game_over = True
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             x1_change = -snake_block
        #             y1_change = 0
        #         elif event.key == pygame.K_RIGHT:
        #             x1_change = snake_block
        #             y1_change = 0
        #         elif event.key == pygame.K_UP:
        #             y1_change = -snake_block
        #             x1_change = 0
        #         elif event.key == pygame.K_DOWN:
        #             y1_change = snake_block
        #             x1_change = 0
        # AI player

 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        if not game_close:
            gameState = GameState(snake_Head,snake_List,foodx,foody,dis_width,dis_width,steps_since_food_eaten)
            best_move = gameState.a_star()
            if best_move == 'left':
                x1_change = -snake_block
                y1_change = 0
            elif best_move == 'right':
                x1_change = snake_block
                y1_change = 0
            elif best_move == 'up':
                y1_change = -snake_block
                x1_change = 0
            elif best_move == 'down':
                y1_change = snake_block
                x1_change = 0
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            steps_since_food_eaten = 0
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        steps_since_food_eaten +=1
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()