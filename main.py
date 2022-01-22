# import pygame
# pygame.init()
#
# # screen
# screen=pygame.display.set_mode((800,600))
#
# # title and icon
# pygame.display.set_caption("Space Invaders")
# icon=pygame.image.load("hockey-puck.png")
# pygame.display.set_icon(icon)
#
# # players and balls
# player1=pygame.image.load("player1.png")
# player1_x=20
# player1_y=300
#
# player2=pygame.image.load("player2.png")
# player2_x=750
# player2_y=300
#
# ball=pygame.image.load("ball.png")
# ball_x=385
# ball_y=280
#
# def player():
#
#
# def ai():
#     screen.blit(player2,(player2_x,player2_y))
#
# def puck():
#     screen.blit(ball,(ball_x,ball_y))
#
#
# # game loop
# runnig=True
# while runnig:
#     for event in pygame.event.get():
#         # x button pressed
#         if event.type==pygame.QUIT:
#             runnig = False
#         up, down, right, left = 0, 0, 0, 0
#         down2, up2, right2, left2 = 0, 0, 0, 0
#         # print(event)
#         if event.type == pygame.QUIT:
#             gameExit = True
#         if event.type == pygame.KEYDOWN:
#             keys = pygame.key.get_pressed()
#
#             if keys[K_LEFT]:
#                 left = 5;
#             elif keys[K_RIGHT]:
#                 right = 5;
#             elif keys[K_UP]:
#                 up = 5;
#             elif keys[K_DOWN]:
#                 down = 5;
#
#
#
#     # player
#     screen.blit(player1, (player1_x, player1_y))
#
#     # field
#     # field color
#     screen.fill((0,128,0))
#     # pygame.display.update()
#
#     # field design
#     Color_line=(255,255,255)
#     pygame.draw.rect(screen, Color_line, (10,10,780,580), 2)
#
#     # mid-field
#     pygame.draw.line(screen,Color_line,(400,10),(400,590),2)
#     pygame.draw.circle(screen,Color_line,(400,290),70,2)
#
#     # D box
#     pygame.draw.rect(screen, Color_line, (10, 200, 100, 200), 2)
#     pygame.draw.rect(screen, Color_line, (690, 200, 100, 200), 2)
#
#     # player 1
#     # player()
#
#     # player 2
#     # ai()
#
#     # ball
#     # puck()
#
#     pygame.display.update()

import math
import sys

import pygame
import time
from pygame.locals import *

# Button class
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

pygame.init()

white = (255,255,255)
black = (0,0,0)
green = (0,150,0)
red = (255,0,0)
blue = (0,0,255)
light_blue = (147,251,253)

#Clock initialized
clock= pygame.time.Clock()
#Board Size
screen= pygame.display.set_mode((800,600))
#dividing line
divline1 = screen.get_width()/2, 0
divline2 = screen.get_width()/2 ,screen.get_height()
#Caption
pygame.display.set_caption('Air Hockey!')
#Font Sizes
smallfont = pygame.font.SysFont("comicsansms" , 25)
medfont = pygame.font.SysFont("comicsansms" , 45)
largefont = pygame.font.SysFont("comicsansms" , 65)

#Create Game Objects
goalheight = 50
goalwidth = 20
goal1 = pygame.Rect(0,screen.get_height()/2 - 50,10,100)
goal2 = pygame.Rect(screen.get_width()-10,screen.get_height()/2 - goalheight,10,100)

paddle1= pygame.draw.circle(screen,(0,0,0),(screen.get_width()/2-200,screen.get_height()/2),20)
paddle2= pygame.draw.circle(screen,(0,0,0),(screen.get_width()/2+200,screen.get_height()/2),20)

paddleVelocity= 4

disc= pygame.draw.circle(screen,(0,0,0),((screen.get_width()/2)-10,(screen.get_height()/2)-10),20)

score1,score2 = 0,0
serveDirection=1

img = pygame.image.load('disc.png')
bluepadimg = pygame.image.load('bluepad.png')
redpadimg = pygame.image.load('redpad.png')

def reset():
    score1, score2 = 0, 0
    serveDirection = 1
    paddleVelocity = 4

# paddle2 -> player
# paddle1 -> ai

def message_to_screen(msg,color,y_displace=0,x_displace=0,size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (screen.get_width()/2+x_displace) , ((screen.get_height()/2) + y_displace)
    screen.blit(textSurf,textRect)

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text , True , color)
    elif size == "medium":
        textSurface = medfont.render(text , True , color)
    elif size == "large":
        textSurface = largefont.render(text , True , color)
    return textSurface , textSurface.get_rect()

def playerUpdate(down,up,right,left):

    # Update Paddle2
    # print(down, " down up ", up, " ", paddleVelocity,'\n')
    # print(left, " left right  ", right, " ", paddleVelocity, '\n')
    paddle2.y += (down - up) * paddleVelocity
    paddle2.x += (right - left) * paddleVelocity

    # if(down-up!=0 or right-left!=0):
    #     print("Inside Paddle1 Moving Condition")
    # print("Y2", paddle2.y);
    # print("X2", paddle2.x);
    if paddle2.y < 0:
        paddle2.y = 0
    elif paddle2.y > screen.get_height() - paddle2.height:
        paddle2.y = screen.get_height() - paddle2.height
    if paddle2.x > screen.get_width() - paddle1.width:
        paddle2.x = screen.get_width() - paddle1.width
    elif paddle2.x < screen.get_width() / 2:
        paddle2.x = screen.get_width() / 2
    # screen.display.update()

player_hit=False
ai_hit=False

init_x=200
init_y=300

# discVelocity= [5,5]
discVelocity= [0,0]
BG = pygame.image.load("assets/Background.png")

def hit(circle1, circle2):
    radius = math.sqrt(pow(circle1.x-circle2.x,2)+pow(circle1.y-circle2.y,2))
    if(radius<=40):
        # print("Hit")
        return True
    else:
        return  False

def resetPuck():
    # discVelocity[0]=5*serveDirection
    # discVelocity[1]=5*serveDirection
    # print(score1,score2)
    # disc.x= screen.get_width()/2
    # disc.y= screen.get_height()/2

    disc.x=(screen.get_width()/2)-10
    disc.y=(screen.get_height()/2)-10
    discVelocity[0]=0
    discVelocity[1]=0

def ai():

    # if(pygame.Rect.colliderect(disc,paddle1)):
    #     print('yay!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #     discVelocity[0]*=-1
    #     discVelocity[1] *= -1
        # pygame.display.update()



    if (0 <= disc.x <= 400):
        # print("here")
        target_x=disc.x- paddle1.x
        target_y=disc.y- paddle1.y
        if(target_x!=0 or target_y!=0):
            valx= (target_x/(math.sqrt(pow(target_x,2)+pow(target_y,2))))*5
            valy =(target_y/(math.sqrt(pow(target_x,2)+pow(target_y,2))))*5
            print("XChange: ",valx)
            print("YChange: ",valy)

            paddle1.x += valx
            paddle1.y += valy
    else:
        # print("Coming back")
        target_x = init_x - paddle1.x
        target_y = init_y - paddle1.y

        if(paddle1.x!=init_x and paddle2.x!=init_y):
            paddle1.x += (target_x / (math.sqrt(pow(target_x, 2) + pow(target_y, 2)))) * 5
            paddle1.y += (target_y / (math.sqrt(pow(target_x, 2) + pow(target_y, 2)))) * 5


    # print("x : ",paddle1.x," y: ",paddle1.y)
    if (hit(paddle2, disc)):
        player_hit = True
        discVelocity[0] = disc.x - paddle2.x
        discVelocity[1] = disc.y - paddle2.y

    elif (hit(paddle1, disc)):
        ai_hit = True
        discVelocity[0] = disc.x - paddle1.x
        discVelocity[1] = disc.y - paddle1.y

def updatePuck():
    global score1
    global score2
    global  player_hit
    global  ai_hit
    if(hit(paddle2,disc)):
        player_hit = True
        discVelocity[0]=disc.x-paddle2.x
        discVelocity[1]=disc.y-paddle2.y

    elif (hit(paddle2, disc)):
        ai_hit = True
        discVelocity[0]=disc.x-paddle1.x
        discVelocity[1]=disc.y-paddle1.y





    # paddle1_hit = pygame.Rect.colliderect(disc,paddle1)
    # paddle2_hit = pygame.Rect.colliderect(disc,paddle2)

    # ai()
    # if(paddle1_hit):
    #     ai()
    #     paddle1_hit=False
    #     paddle2_hit=False

    # if(player_hit):
    #     ball_target_x=disc.x-paddle2.x
    #     ball_target_y=disc.y-paddle2.y
    #     disc.x+=(ball_target_x/math.sqrt(pow(ball_target_x,2)+pow(ball_target_y,2)))*5
    #     disc.y+=(ball_target_y/math.sqrt(pow(ball_target_x,2)+pow(ball_target_y,2)))*5
    #     # disc.x += ball_target_x * 0.1
    #     # disc.y += ball_target_y * 0.1
    #     # paddle2_hit=False
    #     # player_hit=False


    disc.x+=discVelocity[0]
    disc.y+=discVelocity[1]
    # if (disc.x <= disc.width and (disc.y <= screen.get_height()/2 + goalheight) and (disc.y >= screen.get_height() - goalheight)):
    if(disc.x<=goalwidth/2 and 250<=disc.y<=350):
        # print("skfjskfs")
        score2+=1

        # serveDirection=-1
        resetPuck()
    elif (disc.x >= screen.get_width()-goalwidth-disc.width) and (disc.y <= screen.get_height()/2 + goalheight) and (disc.y >= screen.get_height()/2 - goalheight):
        score1+=1
        # serveDirection=1
        resetPuck()
    elif disc.x - 10 < 0 or disc.x + 25 > screen.get_width() :
        discVelocity[0]*=-1;
        paddle1_hit=False

    if disc.y - 10 < 0  or disc.y + 10 > screen.get_height() - disc.height:
        discVelocity[1]*=-1
        paddle1_hit = False
    if disc.colliderect(paddle1) or disc.colliderect(paddle2):
        discVelocity[0]*=-1
        paddle1_hit = False

    # if (player_hit):
    #     ball_target_x = disc.x - paddle2.x
    #     ball_target_y = disc.y - paddle2.y
    #     disc.x += (ball_target_x / math.sqrt(pow(ball_target_x, 2) + pow(ball_target_y, 2))) * 5
    #     disc.y += (ball_target_y / math.sqrt(pow(ball_target_x, 2) + pow(ball_target_y, 2))) * 5
    #     # disc.x += ball_target_x * 0.1
    #     # disc.y += ball_target_y * 0.1
    #     # paddle2_hit=False
    #     player_hit=False

def play():
    # global down, up, right, left
    temp_down, temp_up, temp_right, temp_left=0,0,0,0
    global score1,score2
    last_key=''
    while True:

        # up, down, right, left = 0, 0, 0, 0
        for event in pygame.event.get():
            up, down, right, left = 0, 0, 0, 0
            update = False;
            if event.type == pygame.QUIT:
                score1=0
                score2=0
                gameExit = True
                resetPuck()
                return 0;
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    left = 5;
                    update=True;
                    last_key='left'
                elif keys[K_RIGHT]:
                    right = 5;
                    update=True
                    last_key='right'
                    # print("Pressed right")
                elif keys[K_UP]:
                    up = 5;
                    update=True
                    last_key='up'
                    # print("Pressed up")
                elif keys[K_DOWN]:
                    down = 5;
                    update=True;
                    last_key='down'

                    # print("Pressed down")
            if(update==False):
                last_key=''


        # print("LAST ",last_key,temp_up,temp_down,temp_left,temp_right)
        if (last_key == 'left'):
            temp_down, temp_up, temp_right, temp_left=0,0,0,0
            temp_left = 5;
        elif (last_key == 'right'):
            temp_down, temp_up, temp_right, temp_left=0,0,0,0
            temp_right = 5
        elif (last_key == 'up'):
            temp_down, temp_up, temp_right, temp_left=0,0,0,0
            temp_up = 5;
        elif (last_key == 'down'):
            temp_down, temp_up, temp_right, temp_left=0,0,0,0
            temp_down = 5;
        elif(last_key==''):
            temp_down, temp_up, temp_right, temp_left = 0, 0, 0, 0
        # player update
        playerUpdate(temp_down, temp_up, temp_right, temp_left)

        # ai
        ai()

        updatePuck()

        screen.fill(black)
        message_to_screen("Player 1", white, -250, -150, "small")
        message_to_screen(str(score1), white, -200, -150, "small")
        message_to_screen("Player 2", white, -250, 150, "small")
        message_to_screen(str(score2), white, -200, 150, "small")
        # pygame.draw.rect(screen, (255, 100, 100), paddle1)
        # pygame.draw.rect(screen, (20, 20, 100), paddle2)

        # screen.blit(img,(disc.x,disc.y))

        screen.blit(img, (disc.x, disc.y))
        screen.blit(bluepadimg, (paddle1.x - 5, paddle1.y - 5))
        screen.blit(redpadimg, (paddle2.x - 5, paddle2.y - 5))

        # boundaries and center line
        pygame.draw.rect(screen, light_blue, goal1)
        pygame.draw.rect(screen, light_blue, goal2)

        pygame.draw.circle(screen, white, (screen.get_width() / 2, screen.get_height() / 2), screen.get_width() / 10, 5)
        pygame.draw.line(screen, white, divline1, divline2, 5)
        pygame.draw.line(screen, blue, (0, 0), (screen.get_width() / 2 - 5, 0), 5)
        pygame.draw.line(screen, blue, (0, screen.get_height()), (screen.get_width() / 2 - 5, screen.get_height()), 5)
        pygame.draw.line(screen, red, (screen.get_width() / 2 + 5, 0), (screen.get_width(), 0), 5)
        pygame.draw.line(screen, red, (screen.get_width() / 2 + 5, screen.get_height()),
                         (screen.get_width(), screen.get_height()), 5)
        pygame.draw.line(screen, blue, (0, 0), (0, screen.get_height() / 2 - goalheight), 5)
        pygame.draw.line(screen, blue, (0, screen.get_height() / 2 + goalheight), (0, screen.get_height()), 5)
        pygame.draw.line(screen, red, (screen.get_width(), 0), (screen.get_width(), screen.get_height() / 2 - goalheight),
                         5)
        pygame.draw.line(screen, red, (screen.get_width(), screen.get_height() / 2 + goalheight),
                         (screen.get_width(), screen.get_height()), 5)
        pygame.display.update()
        clock.tick(50)

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        ONE_PLAYER_POS=pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("PLAY MODE", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        ONE_PLAYER= Button(image=None, pos=(400,250),
                          text_input="1 player",font=get_font(50),base_color="Black", hovering_color="Green")
        OPTIONS_BACK = Button(image=None, pos=(400, 350),
                              text_input="BACK", font=get_font(50), base_color="Black", hovering_color="Green")

        ONE_PLAYER.changeColor(ONE_PLAYER_POS)
        ONE_PLAYER.update(screen)
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    gameLoop()

        pygame.display.update()

ingame=False
def gameLoop():
    # Render Logic
    gameExit = False
    gameOver = False
    score2, score1 = 0, 0
    last_key = '';
    print('gameloop')
    while not gameExit:
        # play()
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250),
                             text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400),
                                text_input="MODE", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 550),
                             text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)


        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ingame=True
                    play()

                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                    # pass
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


        # for event in pygame.event.get():
        #     up, down, right, left = 0, 0, 0, 0
        #     if event.type == pygame.QUIT:
        #         gameExit = True
        #     if event.type == pygame.KEYDOWN:
        #         keys = pygame.key.get_pressed()
        #
        #         if keys[K_LEFT]:
        #             left = 5;
        #
        #         elif keys[K_RIGHT]:
        #             right = 5;
        #             # print("Pressed right")
        #         elif keys[K_UP]:
        #             up = 5;
        #             # print("Pressed up")
        #         elif keys[K_DOWN]:
        #             down = 5;
        #             # print("Pressed down")
        #
        #
        # # player update
        # playerUpdate(down, up, right, left)
        #
        # # ai
        # ai()
        #
        # updatePuck()
        #
        # screen.fill(black)
        # message_to_screen("Player 1", white, -250, -150, "small")
        # message_to_screen(str(score1), white, -200, -150, "small")
        # message_to_screen("Player 2", white, -250, 150, "small")
        # message_to_screen(str(score2), white, -200, 150, "small")
        # # pygame.draw.rect(screen, (255, 100, 100), paddle1)
        # # pygame.draw.rect(screen, (20, 20, 100), paddle2)
        #
        # # screen.blit(img,(disc.x,disc.y))
        #
        #
        # screen.blit(img, (disc.x, disc.y))
        # screen.blit(bluepadimg, (paddle1.x - 5, paddle1.y - 5))
        # screen.blit(redpadimg, (paddle2.x - 5, paddle2.y - 5))
        #
        # # boundaries and center line
        # pygame.draw.rect(screen, light_blue, goal1)
        # pygame.draw.rect(screen, light_blue, goal2)
        #
        # pygame.draw.circle(screen, white, (screen.get_width() / 2, screen.get_height() / 2), screen.get_width() / 10, 5)
        # pygame.draw.line(screen, white, divline1, divline2, 5)
        # pygame.draw.line(screen, blue, (0, 0), (screen.get_width() / 2 - 5, 0), 5)
        # pygame.draw.line(screen, blue, (0, screen.get_height()), (screen.get_width() / 2 - 5, screen.get_height()), 5)
        # pygame.draw.line(screen, red, (screen.get_width() / 2 + 5, 0), (screen.get_width(), 0), 5)
        # pygame.draw.line(screen, red, (screen.get_width() / 2 + 5, screen.get_height()),(screen.get_width(), screen.get_height()), 5)
        # pygame.draw.line(screen, blue, (0, 0), (0, screen.get_height() / 2 - goalheight), 5)
        # pygame.draw.line(screen, blue, (0, screen.get_height() / 2 + goalheight), (0, screen.get_height()), 5)
        # pygame.draw.line(screen, red, (screen.get_width(), 0), (screen.get_width(), screen.get_height() / 2 - goalheight),5)
        # pygame.draw.line(screen, red, (screen.get_width(), screen.get_height() / 2 + goalheight),(screen.get_width(), screen.get_height()), 5)
        # pygame.display.update()
        # clock.tick(50)


gameLoop()




