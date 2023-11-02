# 确认页面有哪些角色元素（大小，位置，颜色）
# 确认页面的每个元素会有哪些操作：触发条件、触发结果
import pygame
import random 
import math
# *初始化
pygame.init()
# *基本元素
window = pygame.display.set_mode((800,600))
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
pygame.mixer.Sound('background.wav').play(-1)
pygame.display.set_caption('Space Shooting')
class Element:
  def __init__(self,img,x=0,y=0,x_add=0,y_add=0):
    self.img = img
    self.x = x
    self.y = y
    self.x_add = x_add
    self.y_add = y_add
# 角色元素
background = Element('background.png')
player = Element('player.png',370,480)
enemy_num = 13
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
  # 游戏入口 
  def play(self):
    # 背景记得放最前面，元素放它前面会被挡住
    self._load(self.background)
    # 基本事件
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          # 不要把player.x放在这里面设置，不然执行效率会很慢
          # player.x = 0 if player.x <=64 else player.x - player.x_add
          self.player.x_add = -5
        if event.key == pygame.K_RIGHT:
          self.player.x_add = 5
        if event.key == pygame.K_SPACE:
          if self.bullet_state == 'ready':
            pygame.mixer.Sound('laser.wav').play()
            self.bullet.y_add = -5
            self.bullet.x = player.x
            self.bullet_state = 'shooting'
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
          self.player.x_add = 0
  
    # 这一步会不停执行，所以要加上KEYUP事件，不然点击一下，它就会不停移动
    self._move_player()
    self._move_enemy()
    self._move_bullet()
    self._show_score()
    if self.score == enemy_num:
      self._show_game_over()
    pygame.display.update() 

  # 加载及改变图片元素
  def _load(self,item):
    itemUrl = pygame.image.load(item.img)
    window.blit(itemUrl,(item.x,item.y))
  # 加载及改变文字元素
  def _render_font(self,content,font_size=32,rgb=(255,255,255),position=(10,10)):
    font = pygame.font.Font('freesansbold.ttf',font_size)
    render_font = font.render(content,True,rgb)
    window.blit(render_font,position)
  # player的事件
  def _move_player(self):
    self.player.x += self.player.x_add 
    if self.player.x <= 0:
      self.player.x =0 
    if self.player.x >= 736:
      self.player.x =736 
    self._load(player)
  # enemy的事件
  def _move_enemy(self):
    for item in self.enemy:
      item.x += item.x_add
      hit_the_bullet = math.sqrt(math.pow(item.x - self.bullet.x, 2) + (math.pow(item.y - self.bullet.y, 2))) < 27
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
  # bullet的事件
  def _move_bullet(self):
    if self.bullet_state == 'shooting':
      self.bullet.y += self.bullet.y_add
      self._load(bullet)
    if self.bullet.y <= 0:
      self.bullet.y = 480
      self.bullet_state = 'ready'
  # 展示分数
  def _show_score(self):
    score_content = 'score:'+str(self.score)
    self._render_font(content = score_content)
  # 展示游戏结束
  def _show_game_over(self):
    game_over_content = 'game over'
    self._render_font(content = game_over_content, font_size = 64,position=(200,100))

if __name__ == '__main__':
  shoot_game = Game()
  while True:
    shoot_game.play()
