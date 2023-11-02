## pygame
### 基本结构：
* 初始化
```python
pygame.init()
```
* 基本元素: 标题、窗口、icon、声音
```python
# 标题
pygame.display.set_caption('title')
# 窗口大小
window = pygame.display.set_mode((width,height))
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

### 基本操作：
```python
# 图片元素
def _load(img,x,y):
    itemUrl = pygame.image.load(img)
    window.blit(itemUrl,(x,y))
# 文字元素
def _render_font(self,content,font_size=32,rgb=(255,255,255),position=(10,10)):
  font = pygame.font.Font('freesansbold.ttf',font_size)
  render_font = font.render(content,True,rgb)
  window.blit(render_font,position)
```