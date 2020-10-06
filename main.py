import pygame
import random
from time import sleep

#게임에 사용되는 전역변수 정의

BLACK=(0,0,0)       #게임 바탕 화면의 색상으로 사용될 튜플값
RED=(255,0,0)
pad_width=480       #게임 화면의 가로값
pad_height=640      #게임 화면의 세로값
fighter_width=36    #게이머가 조종할 전투기 이미지의 가로,세로크기
fighter_height=38
enemy_width=26
enemy_height=20

def drawScore(count, WHITE=(0,0,255)):           #couont에 해당하는 숫자를 게임 화면의 왼쪽 상단에 폰트 크기 20의 흰색 글씨로 나타내는 함수입니다.
    global gamepad
    font = pygame.font.SysFont(None,20)
    text = font.render('Enemy Kills:'+str(count),True,WHITE)
    gamepad.blit(text,(0,0))
# 적이 화면 아래로 통과한 개수
def drawPassed(count):          # count에 해닫하는 숫자를 게임 화면의 오른쪽 상단에 폰트 크기 20의 빨간색 글씨로 나타내는 함수
    global gamepad
    font = pygame.font.SysFont(None,20)
    text = font.render('Enemy Passed:'+str(count),True,RED)
    gamepad.blit(text,(360,0))
# 화면에 글씨 보이게 하기

def dispMessage(text):          # text를 폰트 크기 80의 빨간색 글씨로 게임화면 정중앙에 표시하고 2초 이후 runGame 호출하여 게임 재시작
    global gamepad
    textfont = pygame.font.Font('freesansbold.ttf',80)
    text = textfont.render(text,True,RED)
    textpos = text.get_rect()
    textpos.center = (pad_width/2,pad_height/2)
    gamepad.blit(text,textpos)
    pygame.display.update()
    sleep(2)
    runGame()

def crash():
    global gamepad
    dispMessage('Crashed!')

#게임 오버 메시지 보이기
def gameover():
    global gamepad
    dispMessage('Game Over')



#게임에 등장하는 객체를 드로잉
def drawObject(obj,x,y):            #게임 화면의 x,y 좌표에 그려주는 함수
    global gamepad
    gamepad.blit(obj, (x,y))         #obj를 그리는 실제 함수

#게임 실행 메인 함수
def runGame():
    global gamepad,clock,fighter,enemy,bullet            #gamepad는 게임이 진행될 게임 화면,clock은 게임의 초당 프레밈 설정을 위한 clock 객체

    # 전투기 무기에 적이 맞았을 경우 True로 설정되는 플래그
    isShot = False
    shotcount = 0
    enemypassed = 0

    bullet_xy=[]                # 전투기에서 발사되는 무기는 여러 발이 될 수 있으므로 이에 대한 좌표를 저장하기 위해 리스트 이용. bullet_xy는 전투기에서 발사된 무기의 좌표를 저장하는 리스트 변수
    # 전투기 초기 위치 (x,y) 설정
    x=pad_width*0.45
    y=pad_height*0.9
    x_change=0                              # 전투기를 좌우로 이동시키기 위한 변수.

    # 적 초기 위치 설정
    enemy_x=random.randrange(0,pad_width-enemy_width)       #게임 화면에서 적 이미지가 위치할 x좌표 random.randrange(m,n)는 m과n 사이에서 무작위로 하나의 숫자 선택
    enemy_y=0
    enemy_speed=3       # 적이 화면 상단에서 하단으로 떨어지는 속도를 지정해주는 변수

    ongame = False
    while not ongame:
        for event in pygame.event.get():    #게임 화면에서 발생하는 다양한 이벤트 리턴
            if event.type == pygame.QUIT:     #event.type의 값이 마우스로 창을 닫는 이벤트인 pyhame.QUIT이면 값을 TRUE로 설정하여 빠져나감
                ongame = True

            if event.type == pygame.KEYDOWN:      # pygame.KEYDOWN 은 키보드가 눌러졌을 때 발생하는 이벤트 타입.
                if event.key == pygame.K_LEFT:    # 누른 키보드가 왼쪽 화살표키이면 x_change 값을 5감소시킵니다,
                    x_change -= 5

                elif event.key == pygame.K_RIGHT:
                    x_change += 5

                elif event.key == pygame.K_LCTRL:
                    if len(bullet_xy) < 2:
                        bullet_x=x+fighter_width/2
                        bullet_y=y-fighter_height
                        bullet_xy.append([bullet_x,bullet_y])
            if event.type==pygame.KEYUP:        # 게임 화면에서 발생한 이벤트 타입이 키보드를 눌렀다가 떼는 이벤트 타입인지 체크
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        gamepad.fill(BLACK)                 #게임 화면 전체를 BLACK으로 설정된 값에 해당하는 색상으로 채운다 흰색으로 채우고싶으면 (255,255,255)

        #전투기의 위치를 재조정
        x+=x_change                         # x_change 값을 5보다 크게하면 전투기가 좌우로 움직이는 속도가 5로 설정한 것에 비해 빨라지게 됨
        if x < 0:
           x = 0
        elif x > pad_width-fighter_width:     # x값이 게임화면의 오른쪽 끝에서 전투기 이미지의 가로 크기를 뺀 값보다 커지지 않도록 합니다.
            x = pad_width-fighter_width

        if y < enemy_y + enemy_height:
            if (enemy_x>x and enemy_x<x+fighter_width )or (enemy_x + enemy_width>x and enemy_x + enemy_width<x+fighter_width):
                crash()

        drawObject(fighter,x,y)             # fighter를 게임 화면의 x,y 좌표에 그려줍니다.

        #전투기 무기 발사 화면에 그리기
        if len(bullet_xy)!=0:
            for i,bxy in enumerate(bullet_xy):
                bxy[1]-=10
                bullet_xy[i][1]=bxy[1]

                if bxy[1] < enemy_y:
                    if bxy[0]>enemy_x and bxy[0]<enemy_x+enemy_width:
                        bullet_xy.remove(bxy)
                        isShot = True
                        shotcount += 1

                if bxy[1]<=0:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass
        if len(bullet_xy)!=0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)

        drawScore(shotcount)
        #적을 아래로 움직임
        enemy_y += enemy_speed
        if enemy_y>pad_height:              # 화면의 세로 크기를 벗어나면 0으로 초기화하고 enemy_x의 값을 무작위 값으로 설정
            enemy_y=0
            enemy_x = random.randrange(0,pad_width-enemy_width)
            enemypassed += 1
        if enemypassed == 3:
            gameover()

        drawPassed(enemypassed)

        #적이 무기에 맞았는지 체크하고 맞았으면 스피드업
        if isShot:
            enemy_speed += 1
            if enemy_speed >= 10:
                enemy_speed = 10

            enemy_x = random.randrange(0,pad_width-enemy_width)
            enemy_y = 0
            isShot = False

        drawObject(enemy,enemy_x,enemy_y)   #enemy를 게임화면의 (enemy_x,enemy_y) 좌표에 그려줍니다.

        pygame.display.update()             #게임 화면을 다시 그림
        clock.tick(60)                      # 게임 화면의 초당 프레임 수를 60으로 설정
    pygame.quit()

#게임 초기화 함수
def initGame():
    global gamepad,clock,fighter,enemy,bullet

    pygame.init()                           #pygame 라이브러리를 초기화.pygame을 활용하려면 게임 구현 초기에 항상 pygame.init()을 호출해야함
    gamepad=pygame.display.set_mode((pad_width,pad_height))     #게임 화면의 가로 세로 크기 설정
    pygame.display.set_caption('MyGalaga')      #게임 화면 타이틀 바에 이름 표시
    fighter=pygame.image.load('fighter.png')    # fighter.png 이미지 파일을 읽고 이 이미지 객체를 변수 fighter에 지정
    enemy=pygame.image.load('enemy.png')        # enemy.png 이미지 파일을 읽고 이 이미지 객체를 변수 enemy에 지정합니다.
    clock=pygame.time.Clock()       # 초당 프레임 수를 설정할 수 있는 Clock 객체 생성 생성된 클락 객체를 clock으로 둡니다.
    bullet=pygame.image.load('bullet.png')
initGame()
runGame()