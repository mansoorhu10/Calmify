import pygame as py
import random
import time
py.init()

#Colours
RED = (255, 0, 0)
GREY = (40, 40, 40)
WHITE = (255, 255, 255)
YELLOW = (255,255,102)
BLACK = (0, 0, 0)

#Setup
width = 1000
height = 700
py.display.set_caption("Calmify")
clock = py.time.Clock()
win = py.display.set_mode((width, height))
tile = 30
background = py.image.load("coin_background.png")
menu_background = py.image.load("menu_background.png")
control_pic = py.image.load("control_pic.png")

#Button
clicked = False
font1 = py.font.SysFont('Comic Sans', 30)
bg = (100, 100, 100)

allSpritesList = py.sprite.Group()
player_down = py.image.load("player_down.png")
player_up = py.image.load("player_up.png")
player_right = py.image.load("player_right.png")
player_left = py.image.load("player_left.png")


class Player(py.sprite.Sprite):
    def __init__(self, image, vel):
        super().__init__()
        self.image = py.image.load(image)
        self.rect = self.image.get_rect()
        self.vel = vel

    def moveUp(self):
        self.image = player_up
        self.rect.y -= self.vel
    def moveDown(self):
        self.image = player_down
        self.rect.y += self.vel
    def moveLeft(self):
        self.image = player_left
        self.rect.x -= self.vel
    def moveRight(self):
        self.image = player_right
        self.rect.x += self.vel  

class Coin(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load("Coin_img.png")
        self.rect = self.image.get_rect()

mainCharacter = Player("player_down.png", 8)
allSpritesList.add(mainCharacter)
coinsList = py.sprite.Group()
numCoins = 10
for i in range(numCoins):
    c = Coin()
    c.rect.x = random.randint(0, width -20)
    c.rect.y = random.randint(0, height - 20)
    coinsList.add(c)
    allSpritesList.add(c)

    
class Main():
     buttonColour = (50, 200, 10)
     Highlight = (75, 225, 255)
     clickColour = (50, 150, 255)
     textColour = BLACK
     w = 180
     h = 60

     def __init__(self, x, y, text):
          self.x = x
          self.y = y
          self.text = text

     def draw_button(self):
          global clicked
          action = False
          pos = py.mouse.get_pos()
          button_rect = py.Rect(self.x, self.y, self.w, self.h)
          if button_rect.collidepoint(pos):
               if py.mouse.get_pressed()[0] == 1:
                    clicked = True
                    py.draw.rect(win, self.clickColour, button_rect)
               elif py.mouse.get_pressed()[0] == 0 and clicked == True:
                    clicked = False
                    action = True
               else:
                    py.draw.rect(win, self.Highlight, button_rect)
          else:
               py.draw.rect(win, self.buttonColour, button_rect)
          py.draw.line(win, WHITE, (self.x, self.y), (self.x + self.w, self.y), 2)
          py.draw.line(win, WHITE, (self.x, self.y), (self.x, self.y + self.h), 2)
          py.draw.line(win, BLACK, (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), 2)
          py.draw.line(win, BLACK, (self.x + self.w, self.y), (self.x + self.w, self.y + self.h), 2)
          text_img = font1.render(self.text, True, self.textColour)
          text_len = text_img.get_width()
          win.blit(text_img, (self.x + int(self.w / 2) - int(text_len / 2), self.y + 25))
          font_colour = py.Color("blue")
          font = py.font.Font(None, 50)
          back = font.render("To go back to the main menu at any time, press ESC", True, font_colour)
          win.blit(back, (90, 600))
          return action
        
def Control():
    py.mixer.music.unpause()
    run = True
    while run:
        win.blit(menu_background, (0, 0))
        for event in py.event.get():
          if event.type == py.QUIT:
              run = False 
          elif event.type == py.KEYDOWN:
              if event.key == py.K_ESCAPE:
                  py.mixer.music.pause()
                  intro()
        win.blit(control_pic, (0,0))
        py.display.update()



def gameloop():
    music = py.mixer.music.load('game_music.mp3')
    py.mixer.music.play(-1)
    coin_sound = py.mixer.Sound("coin_sound.wav")
    score = 0
    counter = 0
    current_time = 0
    game_Exit = False
    time_passed = 0
    start_timer = False
    font = py.font.Font(None, 50)
    font_colour = py.Color("green")
    font_colour2 = py.Color("blue")
    while not game_Exit:
        for event in py.event.get():
          if event.type == py.QUIT:
              game_Exit = True #Program will end
          elif event.type == py.KEYDOWN:
              if event.key == py.K_SPACE:
                  start_timer = not start_timer
                  if start_timer:
                      current_time = py.time.get_ticks()
              if event.key == py.K_ESCAPE:
                  py.mixer.music.fadeout
                  py.time.delay(200)
                  music = py.mixer.music.load('menu_music.mp3')
                  py.mixer.music.play(-1) 
                  intro()
              if event.key == py.K_1:
                  py.mixer.music.set_volume(0)
                  coin_sound.set_volume(0)
              if event.key == py.K_2:
                  py.mixer.music.set_volume(.6)
                  coin_sound.set_volume(.6)
        if start_timer:
            time_passed = (60 -(py.time.get_ticks() - current_time)/1000.0)
        if time_passed < 0:
            music = py.mixer.music.load('menu_music.mp3')
            py.mixer.music.play(-1) 
            intro()

        
        keys = py.key.get_pressed()

        if keys[py.K_a] and mainCharacter.rect.x >= 10:
            mainCharacter.moveLeft()
        if keys[py.K_d] and mainCharacter.rect.x <= width - 50:
            mainCharacter.moveRight()
        if keys[py.K_w] and mainCharacter.rect.y >= 10:
            mainCharacter.moveUp()
        if keys[py.K_s] and mainCharacter.rect.y <= height - 70:
            mainCharacter.moveDown()
        
        allSpritesList.update()
        coinsCollected = py.sprite.spritecollide(mainCharacter, coinsList, True)

        for i in coinsCollected:
            score+= 1
            c = Coin()
            c.rect.x = random.randint(0, width -20)
            c.rect.y = random.randint(0, height - 20)
            coinsList.add(c)
            allSpritesList.add(c)
            coin_sound.play()
            
            
        win.blit(background, (0, 0))
        text = font.render("Timer: " + str(round(time_passed)), True, font_colour)
        win.blit(text, (760, 10))
        text2 = font.render("Score: " + str(score), True, font_colour2) 
        win.blit(text2, (30, 650))
        allSpritesList.draw(win)
        
        py.display.flip()
        clock.tick(60)

    py.quit()
    quit()


music = py.mixer.music.load('menu_music.mp3')
py.mixer.music.play(-1)
py.mixer.music.set_volume(.6)
Start = Main(220, 220, 'Start')
Controls = Main(600, 220, 'Controls')
Mute = Main(220, 410, "Mute")
UnMute = Main(600, 410, "Unmute")

def intro():
    py.mixer.music.unpause()
    font = py.font.SysFont(None, 30)
    timer = 10  
    dt = 0  
    run = True
    while run:
        win.blit(menu_background, (0, 0))
        font_colour = py.Color("blue")
        font = py.font.Font(None, 50)
        text = font.render("Calmify" , True, BLACK)
        win.blit(text, (430, 100))
        txt = font.render("Time Left: " + str(round(timer))+ " Seconds", True, WHITE)
        win.blit(txt, (20, 50))
        timer -= dt
        dt = clock.tick(30) / 1000 
        if timer <= 0:
            timer = dt
        if Start.draw_button():
            if timer <= 1:
                txt2 = font.render("You may start the game now!", True, WHITE)
                win.blit(txt2, (50, 100))
                py.mixer.music.stop()
                gameloop() 
        if Controls.draw_button():
            py.mixer.music.pause()
            Control()
        if Mute.draw_button():
            py.mixer.music.set_volume(0)
        if UnMute.draw_button():
            py.mixer.music.set_volume(.6)
        
            
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

        py.display.update()

intro()
