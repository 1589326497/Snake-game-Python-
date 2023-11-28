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
