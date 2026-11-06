from pygame import *
'''Required classes'''




#parent class for sprites
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed, width, height):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (width, height)) #e.g. 55,55 - parameters
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y


   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
   def update_r(self):
       keys = key.get_pressed()
       if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < win_height - 80:
           self.rect.y += self.speed
   def update_l(self):
       keys = key.get_pressed()
       if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_s] and self.rect.y < win_height - 80:
           self.rect.y += self.speed




#game scene:
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Free-Arcade')


background = transform.scale(image.load('tennisbg.jpg'), (win_width, win_height))




#flags responsible for game state
game = True
finish = False
clock = time.Clock()
FPS = 60




#creating ball and paddles
racket1 = Player('tp2.png', 30, 200, 4, 50, 150)
racket2 = Player('tp1.png', 520, 200, 4, 50, 150)
ball = GameSprite('tennis.png', 200, 200, 4, 50, 50)




font.init()
game_font = font.Font(None, 35)
info_font = font.Font(None, 28)
lose1 = game_font.render('Player 1 Is Lose!', True, (180, 0, 0))
lose2 = game_font.render('Player 2 Is Lose!', True, (180, 0, 0))
restart_info = info_font.render('Press R to restart', True, (0, 0, 0))


loser_text = None #which "lose" text to show


speed_x = 11
speed_y = 11




def restart_game():
   '''put everything back to the starting state'''
   global speed_x, speed_y, finish, loser_text
   racket1.rect.x, racket1.rect.y = 30, 200
   racket2.rect.x, racket2.rect.y = 520, 200
   ball.rect.x, ball.rect.y = 200, 200
   speed_x = 7
   speed_y = 7
   loser_text = None
   finish = False




while game:
   for e in event.get():
       if e.type == QUIT:
           game = False
       elif e.type == KEYDOWN:
           if e.key == K_r and finish:
               restart_game()


   window.blit(background, (0, 0))


   if finish != True:
       racket1.update_l()
       racket2.update_r()
       ball.rect.x += speed_x
       ball.rect.y += speed_y




       if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
           speed_x *= -1
           speed_y *= 1


       #if the ball reaches screen edges, change its movement direction
       if ball.rect.y > win_height-50 or ball.rect.y < 0:
           speed_y *= -1




       #if ball flies behind this paddle, player 1 loses
       if ball.rect.x < 0:
           finish = True
           loser_text = lose1




       #if the ball flies behind this paddle, player 2 loses
       if ball.rect.x > win_width:
           finish = True
           loser_text = lose2




   racket1.reset()
   racket2.reset()
   ball.reset()


   #game over screen: loser message + restart info
   if finish and loser_text:
       window.blit(loser_text, (200, 200))
       window.blit(restart_info, (205, 245))


   display.update()
   clock.tick(FPS)

