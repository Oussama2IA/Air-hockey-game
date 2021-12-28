import pygame
import pygame_menu
import random

pygame.init()
pygame.display.set_caption("Air Hockey Game")

wide = 500
tall = 600
size = (wide, tall)

screen = pygame.display.set_mode(size)

table_img = pygame.image.load(f'./assets/table.png')
table = pygame.transform.scale(table_img, (wide, tall))

#Player 1
p1wide = 50
p1high = 50
p1x = (wide - p1wide) / 2
p1y = 30
p1_score = 0

p1_img = pygame.image.load(f'./assets/player 1.png')
p1 = pygame.transform.scale(p1_img, (p1wide, p1high))

#Player 2
p2wide = 50
p2high = 50
p2x = (wide - p2wide) / 2
p2y = tall - p2high - 30
p2_score = 0

p2_img = pygame.image.load(f'./assets/player 2.png')
p2 = pygame.transform.scale(p2_img, (p2wide, p2high))

#Rounds
round = 0
max_rounds = 5

#Choose number of rounds
def set_rounds(_, value):
    global max_rounds
    max_rounds = value

#Start the game
def start_game():
    menu.disable()

menu = pygame_menu.Menu('Welcome', wide, tall, theme=pygame_menu.themes.THEME_SOLARIZED)
menu.add.selector('Amount of rounds', [('05', 5), ('10', 10)], onchange=set_rounds)
menu.add.button('Play', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)

#Goals dimentions
g_dim = (135, wide - 135)

#Ball
b_wide = 30
b_high = 30
b_x = (wide - b_wide) / 2
b_y = (tall - b_high) / 2
ball_speed = 1

ball_img = pygame.image.load(f'./assets/ball.png')
ball = pygame.transform.scale(ball_img, (b_wide, b_high))

#Start with random directions
x_dir = ball_speed * [-1, 1][random.randint(0, 1)]
y_dir = ball_speed * [-1, 1][random.randint(0, 1)]

#Draw score
def draw_score():
    font = pygame.font.Font('freesansbold.ttf', 100)
    p1_text = font.render(str(p1_score), False, (200, 200, 200))
    p2_text = font.render(str(p2_score), False, (200, 200, 200))
    screen.blit(p1_text, ((wide - p1_text.get_size()[0]) / 2, tall / 2 - p1_text.get_size()[1] - 70))
    screen.blit(p2_text, ((wide - p2_text.get_size()[0]) / 2, tall / 2 + 80))

#Draw winner
def draw_winner(winner_text):
    overlay = pygame.Surface((wide, tall), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    font = pygame.font.Font('freesansbold.ttf', 50)
    text = font.render(winner_text, False, (200, 200, 200))
    screen.blit(text, ((wide - text.get_size()[0]) / 2, (tall - text.get_size()[1]) / 2))

#Reset game
def reset():
    global b_x, b_y, p1x, p1y, p2x, p2y, x_dir, y_dir, ball_speed, round
    b_x = (wide - b_wide) / 2
    b_y = (tall - b_high) / 2
    p1x = (wide - p1wide) / 2
    p1y = 30
    p2x = (wide - p2wide) / 2
    p2y = tall - p2high - 30
    ball_speed = 1
    x_dir = ball_speed * [-1, 1][random.randint(0, 1)]
    y_dir = ball_speed * [-1, 1][random.randint(0, 1)]
    round += 1

#Restart game
def restart():
    global p1_score, p2_score, ball_speed, round
    p1_score = 0
    p2_score = 0
    reset()
    round = 0

#Game loop
run = True
clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and p1x >= 15:
        p1x += -5
    if keys[pygame.K_RIGHT] and p1x + p1wide <= wide - 15:
        p1x += 5
    if keys[pygame.K_UP] and p1y >= 10:
        p1y += -5
    if keys[pygame.K_DOWN] and p1y + p1high <= tall / 2:
        p1y += 5
    if keys[pygame.K_a] and p2x >= 15:
        p2x += -5
    if keys[pygame.K_d] and p2x + p1wide <= wide - 15:
        p2x += 5
    if keys[pygame.K_w] and p2y >= tall / 2:
        p2y += -5
    if keys[pygame.K_s] and p2y + p1high <= tall - 10:
        p2y += 5
    
    #Collision with left of the screen
    if b_x <= 15:
        x_dir = ball_speed

    ##Collision with right of the screen
    if b_x + b_wide >= wide - 15:
        x_dir = -ball_speed

    #Collision with top of the screen
    if b_y <= 10:
        y_dir = ball_speed

    ##Collision with bottom of the screen
    if b_y + b_high >= tall - 10:
        y_dir = -ball_speed

    #Collision with the bottom of player 1
    if b_y <= p1y + p1high <= b_y + b_high and p1x - b_wide <= b_x <= p1x + p1wide:
        y_dir = ball_speed
        ball_speed += 0.01

    #Collision with the top of player 1
    if b_y <= p1y <= b_y + b_high and p1x - b_wide <= b_x <= p1x + p1wide:
        y_dir = -ball_speed
        ball_speed += 0.01

    #Collision with the right of player 1
    if b_x <= p1x + p1wide <= b_x + b_wide and p1y - b_high <= b_y <= p1y + p1high:
        x_dir = ball_speed
        ball_speed += 0.01

    #Collision with the left of player 1
    if b_x <= p1x <= b_x + b_wide and p1y - b_high <= b_y <= p1y + p1high:
        x_dir = -ball_speed
        ball_speed += 0.01

    #Collision with the bottom of player 2
    if b_y <= p2y + p2high <= b_y + b_high and p2x - b_wide <= b_x <= p2x + p2wide:
        y_dir = ball_speed
        ball_speed += 0.01

    #Collision with the top of player 2
    if b_y <= p2y <= b_y + b_high and p2x - b_wide <= b_x <= p2x + p2wide:
        y_dir = -ball_speed
        ball_speed += 0.01

    #Collision with the right of player 2
    if b_x <= p2x + p2wide <= b_x + b_wide and p2y - b_high <= b_y <= p2y + p2high:
        x_dir = ball_speed
        ball_speed += 0.01

    #Collision with the left of player 2
    if b_x <= p2x <= b_x + b_wide and p2y - b_high <= b_y <= p2y + p2high:
        x_dir = -ball_speed
        ball_speed += 0.01

    #Goal hit player 1 goal
    if b_y <= 10 and g_dim[0] <= b_x <= g_dim[1]:
        p2_score += 1
        reset()

    #Goal hit player 2 goal
    if b_y + b_high >= tall - 10 and g_dim[0] <= b_x <= g_dim[1]:
        p1_score += 1
        reset()

    b_x += x_dir
    b_y += y_dir
    
    screen.fill((0, 0, 0))
    screen.blit(table, (0, 0))
    draw_score()
    screen.blit(p1, (p1x, p1y))
    screen.blit(p2, (p2x, p2y))
    screen.blit(ball, (b_x, b_y))

    #Produce winner
    if round == max_rounds:
        if p1_score > p2_score:
            draw_winner('Player 1 win')
        elif p2_score > p1_score:
            draw_winner('Player 2 win')
        else:
            draw_winner('Draw')
        pygame.display.flip()
        pygame.time.wait(3000)
        restart()
    
    #Updates the entire display surface to the screen        
    pygame.display.flip()
    
    #Updates the frame no more than once every 60 seconds    
    clock.tick(60)

pygame.quit()
