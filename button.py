import pygame
from settings import listStyle, listColorStyle as LCoS, listCheckerStyle as LChS

pygame.init()
font = pygame.font.SysFont('Arial', 40)

objects = []
listColorStyle = [f'Стиль поля {i}' for i in range(1, len(LCoS)+1)]
listCheckerStyle = [f'Стиль шашек {i}' for i in range(1, len(LChS)+1)]
class Button():
    def __init__(self, screen, x, y, width, height, buttonText='Button', onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False
        self.screen = screen
        self.buttonText = buttonText

        self.fillColors = {
            'normal': '#987654',
            'hover': '#654321',
            'pressed': '#422d15',
            'border': '#000000'
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.buttonSurface, (255, 0, 0), self.buttonRect, 8)

        self.buttonSurf = font.render(self.buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self):
        flagColor = False
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        mousePos = (mousePos[0], mousePos[1]+50)
        # print(mousePos)
        # if self.buttonText == 'Играть снова':
        #     print(self.x, self.y)
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.alreadyPressed = True
                    if self.buttonText == 'Играть':
                        flagColor = 5
                    elif self.buttonText in listStyle:
                        indexStyle = listStyle.index(self.buttonText)
                        indexStyle += 1
                        if indexStyle == len(listStyle):
                            indexStyle = 0
                        self.buttonText = listStyle[indexStyle]
                        flagColor = 2
                    elif self.buttonText in listColorStyle:
                        indexStyle = listColorStyle.index(self.buttonText)
                        indexStyle += 1
                        if indexStyle == len(listColorStyle):
                            indexStyle = 0
                        self.buttonText = listColorStyle[indexStyle]
                        flagColor = 3
                    elif self.buttonText in listCheckerStyle:
                        indexStyle = listCheckerStyle.index(self.buttonText)
                        indexStyle += 1
                        if indexStyle == len(listCheckerStyle):
                            indexStyle = 0
                        self.buttonText = listCheckerStyle[indexStyle]
                        flagColor = 4
                    elif self.buttonText == 'Играть снова':
                        flagColor = 1
            else:
                self.alreadyPressed = False

        self.buttonSurf = font.render(self.buttonText, True, (20, 20, 20))
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        pygame.draw.rect(self.buttonSurface, self.fillColors['border'], (0, 0, self.width, self.height), 5)
        self.screen.blit(self.buttonSurface, self.buttonRect)
        if flagColor:
            return flagColor



def myFunction():
    print('Button Pressed')
