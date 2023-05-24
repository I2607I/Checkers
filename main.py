import pygame
from button import Button, objects
from settings import listColorStyle, listCheckerStyle, listStyle

#для отладки
DEBUGGING = False

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
VIOLET = (139, 0, 255)
DARK_GREEN = (1, 100, 72)
DARK_YELLOW = (255, 179, 0)
LIGHT_BROWN = (152, 118, 84)
CREAMY = (242, 232, 201)
BLUISH_BLACK = (21, 23, 25)
ALMOND_CRAYOLA = (219, 222, 205)

SIMPLE_FIGHT_BACK = True      # простая шашка бьёт назад
KING_MOVE_ONE_STEP = False    # дамка делает один шаг
SIMPLE_STOP = False           # происходит остановка при становлении дамкой
SIZE_FIELD = 100
COUNT_FIELD = 8
countCheckers = dict()


WHITECHECKER = WHITE
BLACKCHECKER = BLACK


pygame.init()

W = 1200
H = 800
 
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Checkers")

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, colorCeil, color = -1, stylechecker = True):
        super().__init__() 
        self.colorCeil = colorCeil
        self.ceil = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.ceil.fill(colorCeil)
        self.radius = SIZE_FIELD//3
        self.radiusR = 4

        self.checkerBlack = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.checkerBlack.fill(colorCeil)
        pygame.draw.circle(self.checkerBlack, BLACKCHECKER, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius)

        self.checkerWhite = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.checkerWhite.fill(colorCeil)
        pygame.draw.circle(self.checkerWhite, WHITECHECKER, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius)

    
        self.checkerActiveBlack = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.checkerActiveBlack.fill(colorCeil)
        pygame.draw.circle(self.checkerActiveBlack, BLACKCHECKER, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius)
        pygame.draw.circle(self.checkerActiveBlack, DARK_YELLOW, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius+self.radiusR, self.radiusR)

        self.checkerActiveWhite = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.checkerActiveWhite.fill(colorCeil)
        pygame.draw.circle(self.checkerActiveWhite, WHITECHECKER, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius)
        pygame.draw.circle(self.checkerActiveWhite, DARK_YELLOW, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius+self.radiusR, self.radiusR)

        
        self.kingBlack = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.kingBlack.fill(colorCeil)
        pygame.draw.circle(self.kingBlack, BLACKCHECKER, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius)
        pygame.draw.circle(self.kingBlack, RED, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius//3)

        self.kingWhite = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.kingWhite.fill(colorCeil)
        pygame.draw.circle(self.kingWhite, WHITECHECKER, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius)
        pygame.draw.circle(self.kingWhite, RED, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius//3)  


        self.kingActiveBlack = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.kingActiveBlack.fill(colorCeil)
        pygame.draw.circle(self.kingActiveBlack, BLACKCHECKER, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius)
        pygame.draw.circle(self.kingActiveBlack, RED, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius//3)
        pygame.draw.circle(self.kingActiveBlack, DARK_YELLOW, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius+self.radiusR, self.radiusR)

        self.kingActiveWhite = pygame.Surface((SIZE_FIELD, SIZE_FIELD))
        self.kingActiveWhite.fill(colorCeil)
        pygame.draw.circle(self.kingActiveWhite, WHITECHECKER, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius)
        pygame.draw.circle(self.kingActiveWhite, RED, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius//3)
        pygame.draw.circle(self.kingActiveWhite, DARK_YELLOW, (SIZE_FIELD//2, SIZE_FIELD//2), self.radius+self.radiusR, self.radiusR)


        if stylechecker != True:
            imageCheckerBlack = pygame.image.load(f"images/{stylechecker}.png").convert()
            imageCheckerBlack.set_colorkey((255, 255, 255))
            rec = imageCheckerBlack.get_rect(center = (SIZE_FIELD//2, SIZE_FIELD//2))
            self.checkerBlack.blit(imageCheckerBlack, rec)
        
            imageCheckerActiveBlack = pygame.image.load(f"images/{stylechecker}active.png").convert()
            imageCheckerActiveBlack.set_colorkey((255, 255, 255))
            self.checkerActiveBlack.blit(imageCheckerActiveBlack, rec)

            imageKingBlack = pygame.image.load(f"images/{stylechecker}king.png").convert()
            imageKingBlack.set_colorkey((255, 255, 255))
            rec = imageKingBlack.get_rect(center = (SIZE_FIELD//2, SIZE_FIELD//2))
            self.kingBlack.blit(imageKingBlack, rec)

            imageKingActiveBlack = pygame.image.load(f"images/{stylechecker}kingactive.png").convert()
            imageKingActiveBlack.set_colorkey((255, 255, 255))
            rec = imageKingActiveBlack.get_rect(center = (SIZE_FIELD//2, SIZE_FIELD//2))
            self.kingActiveBlack.blit(imageKingActiveBlack, rec)


        self.checker = {BLACKCHECKER: self.checkerBlack, WHITECHECKER: self.checkerWhite}
        self.checkerActive = {BLACKCHECKER: self.checkerActiveBlack, WHITECHECKER: self.checkerActiveWhite}        
        self.king = {BLACKCHECKER: self.kingBlack, WHITECHECKER: self.kingWhite}
        self.kingActive = {BLACKCHECKER: self.kingActiveBlack, WHITECHECKER: self.kingActiveWhite} 


        self.image = self.ceil
        self.clicked = False
        self.isChecker = False
        self.isKing = False
        if color == WHITECHECKER:
            self.image = self.checkerWhite
            self.isChecker = True
        elif color == BLACKCHECKER:
            self.image = self.checkerBlack
            self.isChecker = True
        self.color = color
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, event_list):
        if not self.isChecker:
            self.isKing = False
        if self.isChecker and not self.isKing:
            if self.clicked:
                self.image = self.checkerActive[self.color]
            else:
                self.image = self.checker[self.color]
        elif self.isChecker and self.isKing:
            if self.clicked:
                self.image = self.kingActive[self.color]
            else:
                self.image = self.king[self.color]
        else:
            self.image = self.ceil
 
flagBackground = 0
FPS = 60        # число кадров в секунду
clock = pygame.time.Clock()

sound_step = pygame.mixer.Sound('sounds/step.ogg')
sound_win = pygame.mixer.Sound('sounds/win.ogg')
# field = []
def createField(COLORFIELD, STYLECHECKER):
    global field
    field = [[0 for j in range(COUNT_FIELD)] for i in range(COUNT_FIELD)]
    BLACKBIELD, WHITEFIELD = COLORFIELD[0], COLORFIELD[1]
    if STYLECHECKER[0] == True:
        global BLACKCHECKER
        global WHITECHECKER
        BLACKCHECKER = STYLECHECKER[1]
        WHITECHECKER = STYLECHECKER[2]
    for i in range(COUNT_FIELD):
        for j in range(COUNT_FIELD):
            if (i + j)%2 == 1:
                if DEBUGGING:
                    if i < 1:
                        field[i][j] = SpriteObject(SIZE_FIELD*j, SIZE_FIELD*i, BLACKBIELD, BLACKCHECKER, STYLECHECKER[0])
                    if i >= COUNT_FIELD-1:
                        field[i][j] = SpriteObject(SIZE_FIELD*j, SIZE_FIELD*i, BLACKBIELD, WHITECHECKER, STYLECHECKER[0])
                    if i >=1 and i <COUNT_FIELD-1:
                        field[i][j] = SpriteObject(SIZE_FIELD*j, SIZE_FIELD*i, BLACKBIELD, -1, STYLECHECKER[0])
                else:
                    if i < COUNT_FIELD//2-1:
                        field[i][j] = SpriteObject(SIZE_FIELD*j, SIZE_FIELD*i, BLACKBIELD, BLACKCHECKER, STYLECHECKER[0])
                    if i > COUNT_FIELD//2:
                        field[i][j] = SpriteObject(SIZE_FIELD*j, SIZE_FIELD*i, BLACKBIELD, WHITECHECKER, STYLECHECKER[0])
                    if i >=COUNT_FIELD//2-1 and i <=COUNT_FIELD//2:
                        field[i][j] = SpriteObject(SIZE_FIELD*j, SIZE_FIELD*i, BLACKBIELD, -1, STYLECHECKER[0])
            else:
                field[i][j] = SpriteObject(SIZE_FIELD*j, SIZE_FIELD*i, WHITEFIELD)
            sc.blit(field[i][j].image, field[i][j].rect)
    group = pygame.sprite.Group(field)
    return group

indexStyle = 0
indexColorStyle = 0
indexCheckerStyle = 0
indexSoundStyle = 0


b = pygame.image.load("images/back.png").convert()
b = pygame.transform.scale(b, (b.get_width()*1.2, b.get_height()*1.2))
Button(b, 50, 20+50, 300, 80, 'Играть')
Button(b, 50+400, 20+50, 300, 80, 'Русские')
Button(b, 50+800, 20+50, 300, 80, 'Стиль поля 1')
Button(b, 50+800, 20+50+650, 300, 80, 'Стиль шашек 1')

surf_alpha = pygame.Surface((W-SIZE_FIELD*COUNT_FIELD, H))
pygame.draw.rect(surf_alpha, ALMOND_CRAYOLA, (0, 0, W-SIZE_FIELD*COUNT_FIELD, H))

pygame.font.init()
my_font = pygame.font.SysFont('arial', 60)
my_font2 = pygame.font.SysFont('arial', 40)

text_surface = my_font.render('Счёт', False, (0, 0, 0))
text_rect = text_surface.get_rect(centerx=(W-SIZE_FIELD*COUNT_FIELD)//2)

text_white = my_font2.render('Белые', False, (0, 0, 0))
text_white_rect = text_white.get_rect(centerx=(W-SIZE_FIELD*COUNT_FIELD)*0.25, centery = (80))

text_black = my_font2.render('Чёрные', False, (0, 0, 0))
text_black_rect = text_white.get_rect(centerx=(W-SIZE_FIELD*COUNT_FIELD)*0.75, centery = (80))

surf_alpha.blit(text_surface, text_rect)
surf_alpha.blit(text_white, text_white_rect)
surf_alpha.blit(text_black, text_black_rect)

# surf_finish = pygame.Surface((300, 80))
surf_finish = pygame.Surface((1200, 1200))
surf_finish.fill(ALMOND_CRAYOLA)
surf_finish.set_colorkey(ALMOND_CRAYOLA)
surf_finish_rect = surf_finish.get_rect(centerx=(W-SIZE_FIELD*COUNT_FIELD)//2+SIZE_FIELD*COUNT_FIELD, centery = 80*4)
Button(surf_finish, (W+SIZE_FIELD*COUNT_FIELD)//2 - 150, 80*4, 300, 80, 'Играть снова')

pygame.display.update()

# возвращает список шашек, которые могут быть взяты
def check_checker_can_fight(i, j, color1, color2):
    res = []
    if field[i][j].color == color1 and field[i][j].isChecker == True and i-2>=0 and j-2>=0 and field[i - 2][j - 2].isChecker == False and field[i-1][j-1].isChecker == True and field[i-1][j-1].color == color2:
        res.append(field[i - 2][j - 2])
    if field[i][j].color == color1 and field[i][j].isChecker == True and i+2<COUNT_FIELD and j-2>=0 and field[i + 2][j - 2].isChecker == False and field[i+1][j-1].isChecker == True and field[i+1][j-1].color == color2:
        res.append(field[i + 2][j - 2])
    if field[i][j].color == color1 and field[i][j].isChecker == True and i-2>=0 and j+2<COUNT_FIELD and field[i - 2][j + 2].isChecker == False and field[i-1][j+1].isChecker == True and field[i-1][j+1].color == color2:
        res.append(field[i - 2][j + 2])
    if field[i][j].color == color1 and field[i][j].isChecker == True and i+2<COUNT_FIELD and j+2<COUNT_FIELD and field[i + 2][j + 2].isChecker == False and field[i+1][j+1].isChecker == True and field[i+1][j+1].color == color2:
        res.append(field[i + 2][j + 2])
    return res
    

# совершает ход белой шашкой, если это возможно
def check_whites_move(i, j, xPrev, yPrev):
    if field[yPrev][xPrev].color == WHITECHECKER and i == yPrev - 1 and (j == xPrev - 1 or j == xPrev + 1) and field[i][j].isChecker == False:
        return 1
    elif field[yPrev][xPrev].color == WHITECHECKER and i == yPrev - 2 and j == xPrev - 2 and field[i][j].isChecker == False and field[yPrev-1][xPrev-1].isChecker == True and field[yPrev-1][xPrev-1].color == BLACKCHECKER:
        field[yPrev-1][xPrev-1].isChecker = False
        field[yPrev-1][xPrev-1].color = -1
        return 2
    elif field[yPrev][xPrev].color == WHITECHECKER and i == yPrev - 2 and j == xPrev + 2 and field[i][j].isChecker == False and field[yPrev-1][xPrev+1].isChecker == True and field[yPrev-1][xPrev+1].color == BLACKCHECKER:
        field[yPrev-1][xPrev+1].isChecker = False
        field[yPrev-1][xPrev+1].color = -1
        return 2
    elif field[yPrev][xPrev].color == WHITECHECKER and i == yPrev + 2 and j == xPrev - 2 and field[i][j].isChecker == False and field[yPrev+1][xPrev-1].isChecker == True and field[yPrev+1][xPrev-1].color == BLACKCHECKER:
        field[yPrev+1][xPrev-1].isChecker = False
        field[yPrev+1][xPrev-1].color = -1
        return 2
    elif field[yPrev][xPrev].color == WHITECHECKER and i == yPrev + 2 and j == xPrev + 2 and field[i][j].isChecker == False and field[yPrev+1][xPrev+1].isChecker == True and field[yPrev+1][xPrev+1].color == BLACKCHECKER:
        field[yPrev+1][xPrev+1].isChecker = False
        field[yPrev+1][xPrev+1].color = -1
        return 2
    return 0

# совершает ход чёрной шашкой, если это возможно
def check_blacks_move(i, j, xPrev, yPrev):
    if field[yPrev][xPrev].color == BLACKCHECKER and i == yPrev + 1 and (j == xPrev - 1 or j == xPrev + 1) and field[i][j].isChecker == False:
        return 1
    elif field[yPrev][xPrev].color == BLACKCHECKER and i == yPrev - 2 and j == xPrev - 2 and field[i][j].isChecker == False and field[yPrev-1][xPrev-1].isChecker == True and field[yPrev-1][xPrev-1].color == WHITECHECKER:
        field[yPrev-1][xPrev-1].isChecker = False
        field[yPrev-1][xPrev-1].color = -1
        return 1
    elif field[yPrev][xPrev].color == BLACKCHECKER and i == yPrev - 2 and j == xPrev + 2 and field[i][j].isChecker == False and field[yPrev-1][xPrev+1].isChecker == True and field[yPrev-1][xPrev+1].color == WHITECHECKER:
        field[yPrev-1][xPrev+1].isChecker = False
        field[yPrev-1][xPrev+1].color = -1
        return 1
    elif field[yPrev][xPrev].color == BLACKCHECKER and i == yPrev + 2 and j == xPrev - 2 and field[i][j].isChecker == False and field[yPrev+1][xPrev-1].isChecker == True and field[yPrev+1][xPrev-1].color == WHITECHECKER:
        field[yPrev+1][xPrev-1].isChecker = False
        field[yPrev+1][xPrev-1].color = -1
        return 1
    elif field[yPrev][xPrev].color == BLACKCHECKER and i == yPrev + 2 and j == xPrev + 2 and field[i][j].isChecker == False and field[yPrev+1][xPrev+1].isChecker == True and field[yPrev+1][xPrev+1].color == WHITECHECKER:
        field[yPrev+1][xPrev+1].isChecker = False
        field[yPrev+1][xPrev+1].color = -1
        return 1
    return 0

def printCoordinates(res):
    for i in range(COUNT_FIELD):
        for j in range(COUNT_FIELD):
            if field[i][j] in res:
                print(i, j)

# возвращает список шашек, которые могут быть взяты
def check_king_can_fight(i, j, color1, color2):
    res = []
    listi = [1, 1, -1, -1]
    listj = [1, -1, 1, -1]
    for k in range(4):
        ii = listi[k]
        jj = listj[k]
        prev = -1
        tmpres = []
        colorOnRoad = False
        while i + ii < COUNT_FIELD and j + jj < COUNT_FIELD and i + ii >= 0 and j + jj >= 0:
            if field[i+ii][j+jj].isChecker == True and field[i+ii][j+jj].color == color1:
                break
            elif field[i+ii][j+jj].isChecker == False and (prev == color2 or prev == -1) and colorOnRoad:
                tmpres.append(field[i+ii][j+jj])
            elif field[i+ii][j+jj].isChecker == True and field[i+ii][j+jj].color == color2 and prev == color2:
                break
            if field[i+ii][j+jj].isChecker and field[i+ii][j+jj].color == color2:
                colorOnRoad = True
            if field[i+ii][j+jj].isChecker:
                prev = color2
            else:
                prev = -1
            ii +=listi[k]
            jj +=listj[k]
        if colorOnRoad:
            for item in tmpres:
                res.append(item)
    # printCoordinates(res)
    return res

# совершает ход дамкой, если это возможно
def check_king_move(i, j, xPrev, yPrev, color1, color2, needFight):
    isFightOnRoad = False
    if abs(i - yPrev) == abs(j - xPrev) and field[yPrev][xPrev].color == color1 and field[i][j].isChecker == False:
        if i-yPrev >= 1:
            listk = [_ for _ in range(1, i - yPrev)]
        else:
            listk = [_ for _ in range(-1, i - yPrev, -1)]
        if j - xPrev >=1:
            listl = [_ for _ in range(1, j - xPrev)]
        else:
            listl = [_ for _ in range(-1, j - xPrev, -1)]
        for k, l in zip(listk, listl):
            if field[yPrev + k][xPrev + l].isChecker and field[yPrev + k][xPrev + l].color == color1:
                return False
        prev = -1
        for k, l in zip(listk, listl):
            if field[yPrev + k][xPrev + l].isChecker and field[yPrev + k][xPrev + l].color == color2 and prev == color2:
                return False
            if field[yPrev + k][xPrev + l].isChecker:
                prev = field[yPrev + k][xPrev + l].color
            else:
                prev = -1
            if field[yPrev + k][xPrev + l].isChecker and field[yPrev + k][xPrev + l].color == color2:
                isFightOnRoad = True
        if needFight and not isFightOnRoad:
            return False
        field[i][j].isChecker = True
        field[i][j].color = color1
        field[i][j].isKing = True
        field[yPrev][xPrev].isChecker = False
        field[yPrev][xPrev].isKing = False
        for k, l in zip(listk, listl):
            if field[yPrev + k][xPrev + l].isChecker == True:
                countCheckers[color2] -= 1
                field[yPrev + k][xPrev + l].isChecker = False
                field[yPrev + k][xPrev + l].isKing = False
        return True
    return False

def checker_can_move(i, j, color):
    if color == WHITECHECKER:
        res = check_whites_can_move(i, j)
    else:
        res = check_blacks_can_move(i, j)
    return res

def check_whites_can_move(i, j):
    res = []
    if i-1 >= 0 and j-1>=0 and field[i-1][j-1].isChecker == False:
        res.append(field[i-1][j-1])
    elif i-1 >= 0 and j+1 < COUNT_FIELD and field[i-1][j+1].isChecker == False:
        res.append(field[i-1][j+1])
    return res

def check_blacks_can_move(i, j):
    res = []
    if i+1 < COUNT_FIELD and j-1>=0 and field[i+1][j-1].isChecker == False:
        res.append(field[i+1][j-1])
    elif i+1 < COUNT_FIELD and j+1 < COUNT_FIELD and field[i+1][j+1].isChecker == False:
        res.append(field[i+1][j+1])
    return res
    


while 1:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            exit()

    for event in event_list:
            if event.type == pygame.KEYDOWN:
                flagBackground = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flagBackground == 1:
                    ii, jj = event.pos[0]//SIZE_FIELD, event.pos[1]//SIZE_FIELD
                    for i in range(COUNT_FIELD):
                        for j in range(COUNT_FIELD):
                            if j == ii and i == jj:
                                field[i][j].clicked = True
                            else:
                                field[i][j].clicked = False
                    list_white_can_fight = []
                    list_black_can_fight = []
                    for i in range(COUNT_FIELD):
                        for j in range(COUNT_FIELD):
                            if field[i][j].isChecker == True and field[i][j].color == WHITECHECKER and (check_checker_can_fight(i, j, WHITECHECKER, BLACKCHECKER) and field[i][j].isKing == False or check_king_can_fight(i, j, WHITECHECKER, BLACKCHECKER) and field[i][j].isKing == True):
                                list_white_can_fight.append(field[i][j])
                            elif field[i][j].isChecker == True and field[i][j].color == BLACKCHECKER and (check_checker_can_fight(i, j, BLACKCHECKER, WHITECHECKER) and field[i][j].isKing == False or check_king_can_fight(i, j, BLACKCHECKER, WHITECHECKER) and field[i][j].isKing == True):
                                list_black_can_fight.append(field[i][j])

                    if isMOveWhite and len(list_white_can_fight) > 0:
                        for i in range(COUNT_FIELD):
                            for j in range(COUNT_FIELD):
                                if field[i][j] not in list_white_can_fight and field[i][j].isChecker:
                                    field[i][j].clicked = False
                    elif not isMOveWhite and len(list_black_can_fight) > 0:
                        for i in range(COUNT_FIELD):
                            for j in range(COUNT_FIELD):
                                if field[i][j] not in list_black_can_fight and field[i][j].isChecker:
                                    field[i][j].clicked = False
                    if prevfight in list_black_can_fight:
                        isMOveWhite = False
                        if prevfight.isKing:
                            res = check_king_can_fight(prevfighti, prevfightj, BLACKCHECKER, WHITECHECKER)
                        else:
                            res = check_checker_can_fight(prevfighti, prevfightj, BLACKCHECKER, WHITECHECKER)
                        res.append(prevfight)
                        if field[jj][ii] not in res:
                            prevfight.clicked = True
                            field[jj][ii].clicked = False
                        yPrev = prevfighti
                        xPrev = prevfightj

                    if prevfight in list_white_can_fight:
                        isMOveWhite = True
                        if prevfight.isKing:
                            res = check_king_can_fight(prevfighti, prevfightj, WHITECHECKER, BLACKCHECKER)
                        else:
                            res = check_checker_can_fight(prevfighti, prevfightj, WHITECHECKER, BLACKCHECKER)
                        res.append(prevfight)
                        if field[jj][ii] not in res:
                            prevfight.clicked = True
                            field[jj][ii].clicked = False
                        yPrev = prevfighti
                        xPrev = prevfightj

                    # for iii in range(COUNT_FIELD):
                    #     for jjj in range(COUNT_FIELD):
                    #         print(field[iii][jjj].clicked, end='    ')
                    #     print()

            if event.type == pygame.QUIT:
                exit()

    sc.fill(WHITE)
    flagDo = False
    if flagBackground == 1:
        for i in range(COUNT_FIELD):
            for j in range(COUNT_FIELD):
                if field[i][j].clicked:
                    if isMOveWhite:
                        if not field[yPrev][xPrev].isKing:
                            if check_checker_can_fight(yPrev, xPrev, WHITECHECKER, BLACKCHECKER):
                                if max(i, yPrev) - min(i, yPrev) != 1 and check_whites_move(i, j, xPrev, yPrev):
                                    countCheckers[BLACKCHECKER] -= 1 
                                    flagDo = True
                                    prevfighti = i
                                    prevfightj = j
                                    prevfightColor = WHITECHECKER
                                    prevfight = field[i][j]
                            else:
                                if check_whites_move(i, j, xPrev, yPrev):
                                    flagDo = True
                                    prevfight = -1
                            if flagDo:
                                field[i][j].isChecker = True
                                field[i][j].color = WHITECHECKER
                                field[yPrev][xPrev].isChecker = False
                        else:
                            if check_king_can_fight(yPrev, xPrev, WHITECHECKER, BLACKCHECKER):  # если может бить, то бить
                                flagDo = check_king_move(i, j, xPrev, yPrev, WHITECHECKER, BLACKCHECKER, True)
                                # print('YES FIGHT KING')
                                if flagDo:
                                    prevfighti = i
                                    prevfightj = j
                                    prevfightColor = WHITECHECKER
                                    prevfight = field[i][j]
                            else:
                                flagDo = check_king_move(i, j, xPrev, yPrev, WHITECHECKER, BLACKCHECKER, False)
                                if flagDo:
                                    prevfight = -1
                                # print('NO FIGHT')

                        # создание дамки
                        if i == 0 and field[i][j].isChecker and field[i][j].color == WHITECHECKER:
                            field[i][j].isKing = True

                        if field[i][j].color == BLACKCHECKER and field[i][j].isChecker is True:
                            field[i][j].clicked = False
                    else:
                        if not field[yPrev][xPrev].isKing:
                            if check_checker_can_fight(yPrev, xPrev, BLACKCHECKER, WHITECHECKER):
                                if max(i, yPrev) - min(i, yPrev) != 1 and check_blacks_move(i, j, xPrev, yPrev):
                                    countCheckers[WHITECHECKER] -= 1
                                    flagDo = True
                                    prevfighti = i
                                    prevfightj = j
                                    prevfightColor = BLACKCHECKER
                                    prevfight = field[i][j]
                            else:
                                if check_blacks_move(i, j, xPrev, yPrev):
                                    flagDo = True
                                    prevfight = -1
                            if flagDo:
                                field[i][j].isChecker = True
                                field[i][j].color = BLACKCHECKER
                                field[yPrev][xPrev].isChecker = False
                        else:
                            if check_king_can_fight(yPrev, xPrev, BLACKCHECKER, WHITECHECKER):   # если может бить, то бить
                                flagDo = check_king_move(i, j, xPrev, yPrev, BLACKCHECKER, WHITECHECKER, True)
                                # print('YES FIGHT')
                                if flagDo:
                                    prevfighti = i
                                    prevfightj = j
                                    prevfightColor = BLACKCHECKER
                                    prevfight = field[i][j]
                            else:
                                flagDo = check_king_move(i, j, xPrev, yPrev, BLACKCHECKER, WHITECHECKER, False)
                                # print('NO FIGHT')
                                if flagDo:
                                    prevfight = -1

                        # создание дамки
                        if i == COUNT_FIELD - 1 and field[i][j].isChecker and field[i][j].color == BLACKCHECKER:
                            field[i][j].isKing = True

                        if field[i][j].color == WHITECHECKER and field[i][j].isChecker is True:
                            field[i][j].clicked = False

                    xPrev = j
                    yPrev = i
                    if flagDo:
                        list_can_fight = []
                        if isMOveWhite:
                            find_color = BLACKCHECKER
                            not_find_color = WHITECHECKER
                        else:
                            find_color = WHITECHECKER
                            not_find_color = BLACKCHECKER
                        for ii in range(COUNT_FIELD):
                            for jj in range(COUNT_FIELD):
                                if field[ii][jj].isChecker and field[ii][jj].color == find_color and not field[ii][jj].isKing:
                                    list_can_fight += check_checker_can_fight(ii, jj, find_color, not_find_color)
                                    list_can_fight += checker_can_move(ii, jj, find_color)
                                elif field[ii][jj].isChecker and field[ii][jj].color == find_color and field[ii][jj].isKing:
                                    list_can_fight += check_king_can_fight(ii, jj, find_color, not_find_color)
                        if countCheckers[BLACKCHECKER] == 0 or countCheckers[WHITECHECKER] == 0 or not list_can_fight:
                            if isMOveWhite:
                                text_win = 'Белые победили'
                            else:
                                text_win = 'Чёрные победили'
                            sound_win.play()
                            flagBackground = 2
                        else:
                            sound_step.play()
                        isMOveWhite = not isMOveWhite

        if prevfight != -1:
            if prevfight.color == BLACKCHECKER and check_checker_can_fight(prevfighti, prevfightj, BLACKCHECKER, WHITECHECKER):
                prevfight.clicked = True
            elif prevfight.color == WHITECHECKER and check_checker_can_fight(prevfighti, prevfightj, WHITECHECKER, BLACKCHECKER):
                prevfight.clicked = True

    # print(xPrev, yPrev)
    if flagBackground == 0:
        sc.blit(b, (0, -50))
        for object in objects:
            z = object.process()
            # print(z)
            if z == 5:
                flagBackground = 1
                xPrev = 0
                yPrev = 0
                isMOveWhite = True
                flagDo = False
                prevfightColor = -1
                prevfighti = -1
                prevfightj = -1
                prevfight = -1
                if indexStyle == 3:
                    SIZE_FIELD = 80
                    COUNT_FIELD = 10
                else:
                    SIZE_FIELD = 100
                    COUNT_FIELD = 8
                group = createField(listColorStyle[indexColorStyle], listCheckerStyle[indexCheckerStyle])
                if indexStyle == 3:
                    countCheckers = {BLACKCHECKER: 20, WHITECHECKER: 20}
                else:
                    countCheckers = {BLACKCHECKER: 12, WHITECHECKER: 12}
            elif z == 2:
                indexStyle += 1
                if indexStyle == len(listStyle):
                    indexStyle == 0
            elif z == 3:
                indexColorStyle += 1
                if indexColorStyle == len(listColorStyle):
                    indexColorStyle = 0
                print(indexColorStyle)
            elif z == 4:
                indexCheckerStyle += 1
                if indexCheckerStyle == len(listCheckerStyle):
                    indexCheckerStyle = 0

    elif flagBackground == 1:
        group.update(event_list)
        group.draw(sc)
        text_count_black = my_font2.render(f'{countCheckers[BLACKCHECKER]}', False, (0, 0, 0))
        text_count_black_rect = text_black.get_rect(centerx=(W - SIZE_FIELD * COUNT_FIELD) * 0.75, centery=(80 * 2))
        text_count_white = my_font2.render(f'{countCheckers[WHITECHECKER]}', False, (0, 0, 0))
        text_count_white_rect = text_white.get_rect(centerx=(W - SIZE_FIELD * COUNT_FIELD) * 0.25, centery=(80 * 2))
        surf_alpha.fill(ALMOND_CRAYOLA)
        surf_alpha.blit(text_surface, text_rect)
        surf_alpha.blit(text_white, text_white_rect)
        surf_alpha.blit(text_black, text_black_rect)
        surf_alpha.blit(text_count_black, text_count_black_rect)
        surf_alpha.blit(text_count_white, text_count_white_rect)

        sc.blit(surf_alpha, (SIZE_FIELD*COUNT_FIELD, 0))
    elif flagBackground == 2:
        group.update(event_list)
        group.draw(sc)
        text_count_black = my_font2.render(f'{countCheckers[BLACKCHECKER]}', False, (0, 0, 0))
        text_count_black_rect = text_black.get_rect(centerx=(W - SIZE_FIELD * COUNT_FIELD) * 0.75, centery=(80 * 2))
        text_count_white = my_font2.render(f'{countCheckers[WHITECHECKER]}', False, (0, 0, 0))
        text_count_white_rect = text_white.get_rect(centerx=(W - SIZE_FIELD * COUNT_FIELD) * 0.25, centery=(80*2))
        surf_alpha.fill(ALMOND_CRAYOLA)
        surf_alpha.blit(text_surface, text_rect)
        surf_alpha.blit(text_white, text_white_rect)
        surf_alpha.blit(text_black, text_black_rect)
        surf_alpha.blit(text_count_black, text_count_black_rect)
        surf_alpha.blit(text_count_white, text_count_white_rect)
        text_win_surf = my_font2.render(text_win, False, (0, 0, 0))
        text_win_rect = text_win_surf.get_rect(centerx=(W - SIZE_FIELD * COUNT_FIELD) // 2, centery=80 * 3)

        surf_alpha.blit(text_win_surf, text_win_rect)
        sc.blit(surf_alpha, (SIZE_FIELD*COUNT_FIELD, 0))
        sc.blit(surf_finish, (0, -50))
        if objects[-1].process() == 1:
            flagBackground = 0
    pygame.display.update()
    clock.tick(FPS)
