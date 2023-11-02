pygame的基本框架：
* 初始化
```python
pygame.init()
```
* 基本元素: 窗口、icon、声音
```python
# 窗口大小
window = pygame.display.set_mode((800,600))
# icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
# 声音，-1表示无限循环
pygame.mixer.Sound('background.wav').play(-1)
```
* 通过循环实现不停重绘来实现动画效果，基本事件
```python
while True:
  for event in pygame.event.get():
    # 确定结束出口
    if event.type == pygame.QUIT:
      pygame.quit()
  # 不停重绘来实现动画
  pygame.display.update() # 只更新部分
  # pygame.display.flip() # 整个重绘
```