# 初始页面：背景、元素（user/enemy/bullet/score）
# 操作：左移、右移、攻击
import pygame
import random 
import math
pygame.init()
window = pygame.display.set_mode((800,600))
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# 声音
pygame.mixer.Sound('background.wav').play(-1)

# 元素
class Element:
  def __init__(self,playImg,x=0,y=0,x_add=0,y_add=0):
    self.playImg = playImg
    self.x = x
    self.y = y
    self.x_add = x_add
    self.y_add = y_add
  def set_element(self):
    window.blit(self.playImg,(self.x,self.y))
    
bg = pygame.image.load('background.png')
background = Element(bg)

playerImg = pygame.image.load('player.png')
player = Element(playerImg,370,480)

enemyImg = pygame.image.load('enemy.png')
enemy_num = 3
element_list = [Element(enemyImg,random.randint(32,768),random.randint(32,80),1) for _ in range(enemy_num)]

bulletImg = pygame.image.load('bullet.png')
bullet = Element(bulletImg,370,480,0,0)
bullet_state = 'ready'

score = 0
font = pygame.font.Font('freesansbold.ttf',32)

over_font = pygame.font.Font('freesansbold.ttf',64)
over_text = over_font.render("GAME OVER", True, (255, 255, 255))
game_over_show = Element(over_text,200,100)

running = True
while running:
  # 背景记得放最前面，元素放它前面会被挡住
  background.set_element()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        # 不要把player.x放在这里面设置，不然执行效率会很慢
        # player.x = 0 if player.x <=64 else player.x - player.x_add
        player.x_add = -5
      if event.key == pygame.K_RIGHT:
        player.x_add = 5
      if event.key == pygame.K_SPACE:
        if bullet_state == 'ready':
          pygame.mixer.Sound('laser.wav').play()
          bullet.y_add = -5
          bullet.x = player.x
          bullet_state = 'shooting'
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        player.x_add = 0
  
  # 这一步会不停执行，所以要加上KEYUP事件，不然点击一下，它就会不停移动
  player.x += player.x_add 
  if player.x <= 0:
    player.x =0 
  if player.x >= 736:
    player.x =736 
  
  for item in element_list:
    item.x += item.x_add
    hit_the_bullet = math.sqrt(math.pow(item.x - bullet.x, 2) + (math.pow(item.y - bullet.y, 2))) < 27
    if item.y > 440 :
      for j in element_list:
        j.y = 2000
      game_over_show.set_element()
      break
    if item.x<=0:
      item.x_add = 1
      item.y += 200
    elif item.x>=736:
      item.x_add = -1
      item.y += 200
    if hit_the_bullet:
      pygame.mixer.Sound('explosion.wav').play()
      score+=1
      element_list.remove(item)
    item.set_element()

  if bullet_state == 'shooting':
    bullet.y += bullet.y_add
    bullet.set_element()
  if bullet.y <= 0:
    bullet.y = 480
    bullet_state = 'ready'
  player.set_element()
  render_font = font.render('score:'+str(score),True,(255,255,255))
  score_show = Element(render_font,10,10)
  score_show.set_element()
  if score == enemy_num:
    game_over_show.set_element()
  pygame.display.update()
