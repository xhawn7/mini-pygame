import pygame
import random
import math
window = pygame.display.set_mode((800,600))
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
pygame.init()

class Element:
   def __init__(self,img,x=0,y=0,x_add=0,y_add=0):
     self.img = img
     self.x = x
     self.y = y
     self.x_add = x_add
     self.y_add = y_add

background = Element('background.png')
player = Element('player.png',370,480)
enemy_num = 3
enemy = [Element('enemy.png',random.randint(32,768),random.randint(32,80),1) for _ in range(enemy_num)]
bullet = Element('bullet.png',370,480)


class Game:
  def __init__(self):
    self.background = background
    self.player = player
    self.enemy = enemy
    self.bullet = bullet 
    self.bullet_state = 'ready'
    self.score = 0
    
  def play(self):
    self._load(self.background)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          self.player.x_add = -5
        if event.key == pygame.K_RIGHT:
          self.player.x_add = 5
        if event.key == pygame.K_SPACE:
          if self.bullet_state == 'ready':
            pygame.mixer.Sound('laser.wav').play()
            self.bullet.y_add = -5
            self.bullet.x = self.player.x
            self.bullet_state = 'shooting'
    self._move_player()
    self._move_enemy()
    self._move_bullet()
    self._show_score()
    if self.score == enemy_num:
      self._show_game_over()
    pygame.display.update() 

  def _load(self,item):
    itemUrl = pygame.image.load(item.img)
    window.blit(itemUrl,(item.x,item.y))
  def _render_font(self,content,font_size=32,rgb=(255,255,255),position=(10,10)):
    font = pygame.font.Font('freesansbold.ttf',font_size)
    render_font = font.render(content,True,rgb)
    window.blit(render_font,position)
  
  def _move_player(self):
    self.player.x = self.player.x + self.player.x_add
    if self.player.x <= 0:
      self.player.x = 0
    if self.player.x >= 736:
      self.player.x = 736
    self._load(player)
    
  def _move_enemy(self):
    for item in self.enemy:
      item.x += item.x_add
      hit_the_bullet = math.sqrt(math.pow(item.x - bullet.x, 2) + (math.pow(item.y - bullet.y, 2))) < 27
      if item.y > 440 :
        for j in self.enemy:
          j.y = 2000
          self._show_game_over()
        break
      if item.x<=0:
        item.x_add = 1
        item.y += 200
      elif item.x>=736:
        item.x_add = -1
        item.y += 200
      if hit_the_bullet:
        pygame.mixer.Sound('explosion.wav').play()
        self.score+=1
        self.enemy.remove(item)
      self._load(item)

  def _move_bullet(self):
    if self.bullet_state == 'shooting':
      self.bullet.y += self.bullet.y_add
      self._load(bullet)
    if self.bullet.y <= 0:
      self.bullet.y = 480
      self.bullet_state = 'ready'
  
    def _show_score(self):
      score_content = 'score:'+str(self.score)
      self._render_font(content = score_content)

    def _show_game_over(self):
      game_over_content = 'game over'
      self._render_font(content = game_over_content, font_size = 64,position=(200,100))

if __name__ == '__main__':
  shoot_game = Game()
  while True:
    shoot_game.play()
