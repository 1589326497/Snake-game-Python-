
贪吃蛇游戏是一种经典的计算机游戏，玩家需要控制一条蛇吃到屏幕上出现的食物，每吃到一次食物，蛇的长度就会增加。在这篇文章中，我将分享如何使用Python和pygame库来实现这个游戏。

对于pygame还不熟悉的同学推荐看一下这篇文章
[Pygame - Display 显示模式 (w3schools.cn)](https://www.w3schools.cn/pygame/pygame_display_modes.html)

### 贪吃蛇游戏的主要逻辑如下：

1. 初始化游戏窗口和相关变量，如蛇头位置、食物位置、分数等。
2. 进入游戏循环，不断处理用户输入和游戏状态更新。
3. 在每次循环中，根据用户输入的方向（上、下、左、右）来更新蛇头的移动方向。
4. 判断蛇头是否到达边界或者碰到自己的身体，如果是，则游戏结束。
5. 判断蛇头是否吃到食物，如果是，则增加蛇的长度并重新生成食物。
6. 将新的蛇头添加到蛇的身体列表中，并删除尾巴（即原来的蛇头）。
7. 渲染游戏画面，包括背景、蛇头、食物和分数等。
8. 更新显示窗口，然后暂停一段时间以控制游戏帧率。
9. 重复步骤2-8，直到游戏结束。

##### 1.首先，我们需要导入所需的库：

```python
import pygame
import random
```

##### 2.加载游戏所需要的音频文件

```python
# 播放音效  
# 加载音效文件  
sound_effect = pygame.mixer.Sound("file/01.wav")  
sound_effect.play()
```

##### 3.然后，我们初始化pygame并设置窗口的大小：

```python
# 初始化
pygame.init()
W = 800
H = 600

ROW = 24  # 行
COL = 32  # 列
size = (W, H)

# 创建窗口
window = pygame.display.set_mode(size)
pygame.display.set_caption("贪吃蛇")
bg_color = (255, 255, 0)  # 背景颜色
```

##### 4.接下来，我们定义一个Point类来表示蛇的身体：

```python
class Point:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def copy(self):
        return Point(self.row, self.col)
```

##### 5.我们还定义了一个函数来绘制蛇的身体：

```python
def rect(Point, color):
    cell_width = W / COL
    cell_height = H / ROW
    left = Point.col * cell_width
    top = Point.row * cell_height

    pygame.draw.rect(window, color, (left, top, cell_width, cell_height))
```

##### 6.然后，我们定义一个函数来生成食物：

```python
def gen_food(snakes):
    while 1:
        pos = Point(random.randint(0, ROW - 1), random.randint(0, COL - 1))  # random.randint()方法生成随机的行和列的食物

        # 判断食物生成的位置是否在蛇身体上
        is_coll = False
        if head.row == pos.row and head.col == pos.col:
            is_coll = True
        for snake in snakes:
            if snake.row == pos.row and snake.col == pos.col:
                is_coll = True
        if not is_coll:
            break
    return pos
```

##### 7.接下来，我们定义蛇的身体、蛇头、食物和方向：

```python
# 定义蛇身体
snakes = []
snakes_color = (128, 128, 128)

# 蛇头
head = Point(int(ROW / 2), int(COL / 2))
head_color = (0, 128, 128)
food = gen_food(snakes)
food_color = (255, 255, 0)

# 方向
direct = 'left'
```

##### 8.最后，我们进入游戏循环：

```python
# 计分功能
score = 0
font = pygame.font.Font(None, 36)
# 游戏循环
no_quit = True
clock = pygame.time.Clock()

while no_quit:
    # 处理事件
    for event in pygame.event.get():  # 获取事件的对列
        if event.type == pygame.QUIT:  # 点下退出
            no_quit = False
        if event.type == pygame.KEYDOWN:  # 点下方向键
            if event.key == pygame.K_UP:
                if direct == 'left' or direct == 'right':
                    direct = 'up'
            elif event.key == pygame.K_DOWN:
                if direct == 'left' or direct == 'right':
                    direct = 'down'
            elif event.key == pygame.K_LEFT:
                if direct == 'up' or direct == 'down':
                    direct = 'left'
            elif event.key == pygame.K_RIGHT:
                if direct == 'up' or direct == 'down':
                    direct = 'right'
    # 吃东西
    eat = head.row == food.row and head.col == food.col
    # 从新产生食物
    if eat:
        food = Point(random.randint(0, ROW - 1), random.randint(0, COL - 1))
        score+=1    #分数加1
    # 身子
    # 1 先把头插到身子上
    snakes.insert(0, head.copy())
    # 2 把尾巴删掉
    if not eat:
        snakes.pop()

    # 移动
    if direct == 'left':
        head.col -= 1
    elif direct == 'right':
        head.col += 1
    elif direct == 'up':
        head.row -= 1
    elif direct == 'down':
        head.row += 1
    # 检查
    is_dead = False
    # 1，撞墙
    if head.col < 0 or head.row < 0 or head.col > COL or head.row > ROW:
        is_dead = True
    # 2，撞自己
    for snake in snakes:
        if snake.col == head.col and snake.row == head.row:
            is_dead = True
            break
    if is_dead:
        print("死亡了")
        no_quit = False
    # 渲染
    pygame.draw.rect(window, (255, 255, 255), (0, 0, W, H))  # 渲染背景
    rect(head, head_color)  # 蛇头渲染
    rect(food, food_color)  # 食物渲染
    for snake in snakes:  # 渲染身子
        rect(snake, snakes_color)
    # 渲染分数
    score_text = font.render("Score: {}".format(score), True, (106,90,205))
    window.blit(score_text, (10, 10))

    pygame.display.flip()  # 更新整个显示窗口

    # 设置帧频
    clock.tick(10)
```

这就是贪吃蛇游戏的Python实现

### 效果演示
![游戏运行](https://img-blog.csdnimg.cn/direct/cedced62619c4c9880829de53fe9e043.png#pic_center)
![吃到食物后蛇身变长](https://img-blog.csdnimg.cn/direct/62d6695fae7d4e84ac7a291955afff4c.png#pic_center)
### 完整代码

```python
"""贪吃蛇项目练习基于pygame 2023年11月27日"""
import pygame
import random

# 初始化
pygame.init()
W = 800
H = 600

ROW = 24  # 行
COL = 32  # 列
size = (W, H)

# 播放音效
# 加载音效文件
sound_effect = pygame.mixer.Sound("file/01.wav")
sound_effect.play()
# 点 类
class Point:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def copy(self):
        return Point(self.row, self.col)


# 绘制点函数
def rect(Point, color):
    cell_width = W / COL
    cell_height = H / ROW
    left = Point.col * cell_width
    top = Point.row * cell_height

    pygame.draw.rect(window, color, (left, top, cell_width, cell_height))


# 生成食物函数
def gen_food(snakes):
    while 1:
        pos = Point(random.randint(0, ROW - 1), random.randint(0, COL - 1))  # random.randint()方法生成随机的行和列的食物

        # 判断食物生成的位置是否在蛇身体上
        is_coll = False
        if head.row == pos.row and head.col == pos.col:
            is_coll = True
        for snake in snakes:
            if snake.row == pos.row and snake.col == pos.col:
                is_coll = True
        if not is_coll:
            break
    return pos



# 定义蛇身体
snakes = []
snakes_color = (128, 128, 128)

# 窗口
window = pygame.display.set_mode(size)
pygame.display.set_caption("贪吃蛇")
bg_color = (255, 255, 0)  # 背景颜色
# 定义坐标 和颜色
head = Point(int(ROW / 2), int(COL / 2))
head_color = (0, 128, 128)
food = gen_food(snakes)
food_color = (255, 255, 0)
# 定义方向
direct = 'left'

#计分功能
score = 0
font = pygame.font.Font(None, 36)
# 游戏循环
no_quit = True
clock = pygame.time.Clock()

while no_quit:
    # 处理事件
    for event in pygame.event.get():  # 获取事件的对列
        if event.type == pygame.QUIT:  # 点下退出
            no_quit = False
        if event.type == pygame.KEYDOWN:  # 点下方向键
            if event.key == pygame.K_UP:
                if direct == 'left' or direct == 'right':
                    direct = 'up'
            elif event.key == pygame.K_DOWN:
                if direct == 'left' or direct == 'right':
                    direct = 'down'
            elif event.key == pygame.K_LEFT:
                if direct == 'up' or direct == 'down':
                    direct = 'left'
            elif event.key == pygame.K_RIGHT:
                if direct == 'up' or direct == 'down':
                    direct = 'right'
    # 吃东西
    eat = head.row == food.row and head.col == food.col
    # 从新产生食物
    if eat:
        food = Point(random.randint(0, ROW - 1), random.randint(0, COL - 1))
        score+=1    #分数加1
    # 身子
    # 1 先把头插到身子上
    snakes.insert(0, head.copy())
    # 2 把尾巴删掉
    if not eat:
        snakes.pop()

    # 移动
    if direct == 'left':
        head.col -= 1
    elif direct == 'right':
        head.col += 1
    elif direct == 'up':
        head.row -= 1
    elif direct == 'down':
        head.row += 1
    # 检查
    is_dead = False
    # 1，撞墙
    if head.col < 0 or head.row < 0 or head.col > COL or head.row > ROW:
        is_dead = True
    # 2，撞自己
    for snake in snakes:
        if snake.col == head.col and snake.row == head.row:
            is_dead = True
            break
    if is_dead:
        print("死亡了")
        no_quit = False
    # 渲染
    pygame.draw.rect(window, (255, 255, 255), (0, 0, W, H))  # 渲染背景
    rect(head, head_color)  # 蛇头渲染
    rect(food, food_color)  # 食物渲染
    for snake in snakes:  # 渲染身子
        rect(snake, snakes_color)
    # 渲染分数
    score_text = font.render("Score: {}".format(score), True, (106,90,205))
    window.blit(score_text, (10, 10))

    pygame.display.flip()  # 更新整个显示窗口

    # 设置帧频
    clock.tick(10)

```

