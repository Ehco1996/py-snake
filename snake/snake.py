import random
import sys
import time
import pygame
from pygame.locals import *

FPS = 2  # 屏幕刷新率（在这里相当于贪吃蛇的速度）
WINDOWWIDTH = 640  # 屏幕宽度
WINDOWHEIGHT = 480  # 屏幕高度
CELLSIZE = 20  # 小方格的大小

# 断言，屏幕的宽和高必须能被方块大小整除
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0

# 横向和纵向的方格数
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# 定义几个常用的颜色
# R G B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

# 定义贪吃蛇的动作
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# 贪吃蛇的头（）
HEAD = 0


def main():

    # 定义全局变量
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()  # 初始化pygame

    FPSCLOCK = pygame.time.Clock()  # 获得pygame时钟
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,
                                           WINDOWHEIGHT))  # 设置屏幕宽高
    BASICFONT = pygame.font.Font('resources/font/neuropol.ttf',
                                 18)  # BASICFONT
    pygame.display.set_caption('Wormy')  # 设置窗口的标题

    showStartScreen()  # 显示开始画面

    while True:

        # 这里一直循环于开始游戏和显示游戏结束画面之间，
        # 运行游戏里有一个循环，显示游戏结束画面也有一个循环
        # 两个循环都有相应的return，这样就可以达到切换这两个模块的效果

        runGame()  # 运行游戏

        showGameOverScreen()  # 显示游戏结束画面


def runGame():
    # 随机初始化设置一个点作为贪吃蛇的起点
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)

    # 以这个点为起点，建立一个长度为3格的贪吃蛇（数组）
    wormCoords = [{
        'x': startx,
        'y': starty
    }, {
        'x': startx - 1,
        'y': starty
    }, {
        'x': startx - 2,
        'y': starty
    }]

    direction = RIGHT  # 初始化一个运动的方向

    # 随机一个apple的位置
    apple = getRandomLocation()

    while True:  # 游戏主循环
        for event in pygame.event.get():  # 事件处理
            if event.type == QUIT:  # 退出事件
                terminate()
            elif event.type == KEYDOWN:  # 按键事件
                # 如果按下的是左键或a键，且当前的方向不是向右，就改变方向，以此类推
                if (event.key == K_LEFT
                        or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT
                      or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP
                      or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN
                      or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # 检查贪吃蛇是否撞到撞到边界
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return

        # 检查贪吃蛇是否撞到自己
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over

        # 检查贪吃蛇是否吃到apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # 不移除蛇的最后一个尾巴格
            apple = getRandomLocation()  # 重新随机生成一个apple
        else:
            del wormCoords[-1]  # 移除蛇的最后一个尾巴格

        # 根据方向，添加一个新的蛇头，以这种方式来移动贪吃蛇
        if direction == UP:
            newHead = {
                'x': wormCoords[HEAD]['x'],
                'y': wormCoords[HEAD]['y'] - 1
            }
        elif direction == DOWN:
            newHead = {
                'x': wormCoords[HEAD]['x'],
                'y': wormCoords[HEAD]['y'] + 1
            }
        elif direction == LEFT:
            newHead = {
                'x': wormCoords[HEAD]['x'] - 1,
                'y': wormCoords[HEAD]['y']
            }
        elif direction == RIGHT:
            newHead = {
                'x': wormCoords[HEAD]['x'] + 1,
                'y': wormCoords[HEAD]['y']
            }

        # 插入新的蛇头在数组的最前面
        wormCoords.insert(0, newHead)

        # 绘制背景
        DISPLAYSURF.fill(BGCOLOR)

        # 绘制所有的方格
        drawGrid()

        # 绘制贪吃蛇
        drawWorm(wormCoords)

        # 绘制apple
        drawApple(apple)

        # 绘制分数（分数为贪吃蛇数组当前的长度-3）
        drawScore(len(wormCoords) - 3)

        # 更新屏幕
        pygame.display.update()

        # 设置帧率
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    '''绘制提示消息'''
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    '''检查按键是否有按键事件'''
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    '''显示开始画面'''

    DISPLAYSURF.fill(BGCOLOR)

    titleFont = pygame.font.Font('resources/font/neuropol.ttf', 100)

    titleSurf = titleFont.render('Wormy!', True, GREEN)

    titleRect = titleSurf.get_rect()
    titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(titleSurf, titleRect)

    drawPressKeyMsg()

    pygame.display.update()

    while True:

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def terminate():
    '''退出'''
    pygame.quit()
    sys.exit()


def getRandomLocation():
    '''随机生成一个坐标位置'''
    return {
        'x': random.randint(0, CELLWIDTH - 1),
        'y': random.randint(0, CELLHEIGHT - 1)
    }


def showGameOverScreen():
    '''显示游戏结束画面'''
    gameOverFont = pygame.font.Font('resources/font/neuropol.ttf', 50)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2,
                       WINDOWHEIGHT / 2 - gameRect.height - 10)
    overRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    '''绘制分数'''
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    '''根据 wormCoords 数组绘制贪吃蛇'''
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8,
                                           CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    '''根据 coord 绘制 apple'''
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    '''绘制所有的方格'''
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
