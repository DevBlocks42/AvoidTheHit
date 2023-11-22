import pygame
import time 
import random

pygame.init()
display_width = 852
display_height = 480
gameTitle = 'Avoid The Hit v1.0.0'
musicFilePath = "../Ressources/Sounds/Music/Music.wav"
scoreFilePath = '../Data/scores.txt'
spaceShipImagePath = '../Ressources/Images/SpaceShip.png'
meteorImagePath = '../Ressources/Images/Meteor.png'
backgroundImagePath = '../Ressources/Images/Background.jpg'
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption(gameTitle)
scoreFile = open(scoreFilePath,"w")
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
clock = pygame.time.Clock()
musicFile = pygame.mixer.Sound(musicFilePath)
backgroundImage = pygame.image.load(backgroundImagePath)
meteorImage = pygame.image.load(meteorImagePath).convert_alpha()
spaceShipImage = pygame.image.load(spaceShipImagePath)
spaceShipImage = pygame.transform.scale(spaceShipImage, (146, 128)) #394x347
spaceShip_speed = 60
spaceShip_width = 146
spaceShip_height = 128

def meteor(x, y, width, height, color):
   #DEBUG-COLLISION:# pygame.draw.rect(display, color, [x, y, width, height])
   display.blit(meteorImage, (x,y))

def drawspaceShip(x,y):
   display.blit(spaceShipImage, (x,y))

def game_over(score):
   musicFile.stop()
   send_message('Vous avez perdu ! Score ' + str(score))

def meteor_passed(count):
   font = pygame.font.SysFont(None, 25)
   text = font.render("Score : " + str(count), True, red)
   display.blit(text, (0,0))

def send_message(text):
   largeText = pygame.font.Font('freesansbold.ttf',45)
   TextSurf, TextRect = text_objects(text, largeText)
   TextRect.center = ((display_width/2),(display_height/2))
   display.blit(TextSurf, TextRect)
   pygame.display.update()
   time.sleep(2)
   game_loop()

def text_objects(text, font):
   textSurface = font.render(text, True, green)
   return textSurface, textSurface.get_rect()

def game_loop():
   X = (display_width * 0.045)
   Y = (display_width * 0.4)
   x_change = 0
   meteor_startX = random.randrange(0,display_width)
   meteor_startY = -600
   meteor_speed = 1
   meteor_width = 45
   meteor_height = 45
   meteor_count = 1
   s_passed = 0
   crashed = False
   musicFile.play()
   while not crashed:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               x_change -= spaceShip_speed
            elif event.key == pygame.K_RIGHT:
               x_change +=  spaceShip_speed
         if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               x_change = 0
         X += x_change 
      display.blit(backgroundImage, (0,0))
      meteor(meteor_startX,meteor_startY,meteor_width,meteor_height,white)
      meteor_startY += meteor_speed
      drawspaceShip(X,Y)
      meteor_passed(s_passed)
      if X > display_width - spaceShip_width or X < 0: # Le vaisseaux sort de l ecran
         game_over(s_passed)
      if meteor_startY > display_height: # L objet sort de l ecran
         meteor_startY = 0 - meteor_height
         meteor_startX = random.randrange(0,display_width - meteor_width)
         s_passed += 1
      if meteor_speed < 5:
         meteor_speed += 0.5
      else :
         meteor_speed = 5
      meteorRect = pygame.Rect(meteor_startX, meteor_startY, meteor_width, meteor_height)
      spaceShipRect = pygame.Rect(X, Y, spaceShip_width, spaceShip_height)
      if spaceShipRect.colliderect(meteorRect):
         game_over(s_passed)
      pygame.display.update()
      clock.tick(120)

game_loop()
pygame.quit()
quit()