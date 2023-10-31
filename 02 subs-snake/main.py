# init: 字体，标题
# 元素：画布，蛇，食物
# 方向，坐标，颜色，大小，速度
import pygame
import random
from collections import namedtuple
# 初始化
pygame.init()
font = pygame.font.Font('freesansbold.ttf',32)
pygame.display.set_caption('不死🐍')
# 大小速度
BLOCK_SIZE = 20
SPEED = 10
# 颜色
RED = (200,0,0)
BLACK = (0,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
WHITE = (255,255,255)
# 坐标
Point = namedtuple('point','x,y')
# 方向
# 用枚举的形式
# from enum import Enum
# class Direction(Enum):
#    RIGHT = 1
#    LEFT = 2
#    UP = 3
#    DOWN = 4
# 直接用元组的形式写
Direct = namedtuple('direction','LEFT,RIGHT,UP,DOWN')
Direction = Direct(1,2,3,4)
   

class Game:
  # 双下划线的变量为私有类型的变量，只允许类本身访问
  def __init__(self,w=640,h=480):
    self.w = w
    self.h = h
    self.display = pygame.display.set_mode((self.w,self.h))
    self.clock = pygame.time.Clock()
    # 蛇
    self.head = Point(w/2,h/2)
    self.snake = [self.head,
                  Point(self.head.x-BLOCK_SIZE,self.head.y),
                  Point(self.head.x-2*BLOCK_SIZE,self.head.y)
                  ]
    self.direction = None
    # 食物
    self.food = None
    self._show_food() # 为什么要加_
    # 分数
    self.score = 0

  # 单下划线开头的函数为保护类型的变量，只允许本身和子类访问，在from a import *时不会被引入 
  def _show_food(self):
    x = random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
    y = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
    self.food = Point(x,y)
    if self.food in self.snake:
        self._show_food()

  def play_snake(self):
   #   game_over = False
    #  if self.is_hit():
    #     # game_over = True
    #     return game_over, self.score
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           quit()
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_LEFT:
              self.direction = Direction.LEFT
           if event.key == pygame.K_RIGHT:
              self.direction = Direction.RIGHT
           if event.key == pygame.K_UP:
              self.direction = Direction.UP
           if event.key == pygame.K_DOWN:
              self.direction = Direction.DOWN
         #   # 按下数字8游戏结束  
         #   if event.key == pygame.K_8:
         #      game_over = True
         #      return game_over
     # 确定新蛇头方向&坐标  
     if self._is_hit():
        self._change_direction()
        # self.direction = Direction.LEFT
     self._locate_snake(self.direction)
     # 确定新蛇的长度
     self.snake.insert(0,self.head)
     # 吃到食物时 
     if self.head == self.food:
        self.score += 1
        self._show_food()
     else:
        self.snake.pop()
     # 画蛇
     self._draw_snake()
     self.clock.tick(SPEED)
     return self.score
  
  def _locate_snake(self,direction):
     x = self.head.x
     y = self.head.y
     if direction == Direction.LEFT :
       x-=BLOCK_SIZE
     elif direction == Direction.RIGHT :
       x+=BLOCK_SIZE
     elif direction == Direction.UP:
       y-=BLOCK_SIZE
     elif direction == Direction.DOWN:
       y+=BLOCK_SIZE
     self.head = Point(x,y)
  
  def _is_hit(self):
     x = self.head.x
     y = self.head.y
     if x<=0 or x>=self.w-BLOCK_SIZE or y<=0 or y>=self.h-BLOCK_SIZE:
        return True
    #  if self.head in self.snake[1:]:
    #     return True
     return False
  
  def _change_direction(self):
     x = self.head.x
     y = self.head.y
     if x == self.w - BLOCK_SIZE and self.direction == Direction.RIGHT:
        self.direction = Direction.UP
     if y == 0 and self.direction == Direction.UP:
        self.direction = Direction.LEFT
     if x == 0 and self.direction == Direction.LEFT:
        self.direction = Direction.DOWN
     elif y == self.h - BLOCK_SIZE and self.direction == Direction.DOWN:
        self.direction = Direction.RIGHT  
 
  def _draw_snake(self):
     self.display.fill(BLACK)
     for p in self.snake:
        pygame.draw.rect(self.display,BLUE1,pygame.Rect(p.x,p.y,BLOCK_SIZE,BLOCK_SIZE))
        pygame.draw.rect(self.display,BLUE2,pygame.Rect(p.x+4,p.y+4,12,12))
     pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
     text = font.render('score:'+str(self.score),True,WHITE)
     self.display.blit(text,[0,0])
     pygame.display.flip()         

if __name__ == '__main__':
  snake_game = Game()
  while True:
     snake_game.play_snake()
#     game_over = snake_game.play_snake()
#     if game_over:
#        break
#   pygame.quit()
   
