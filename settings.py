import pygame
pygame.init()

WIDTH = 900
HEIGHT = 630
FPS = 60

CARD_WIDTH = 75
CARD_HEIGHT = 125
CARD_RAD = 12
CARD_X_GAP = 25

BACK_CARD_BORDER_COLOUR = (18, 98, 24)
BACK_CARD_COLOUR = (7, 41, 17)
CARD_BACK_COLOUR = 'black'

INFO_HEIGHT = 75
EXIT_FONT = pygame.font.Font("arial-unicode-ms.ttf", CARD_WIDTH//3)
TIMER_FONT = pygame.font.Font("arial-unicode-ms.ttf", 20)
MOVES_FONT = pygame.font.Font("arial-unicode-ms.ttf", 25)

CARD_FONT = pygame.font.Font("arial-unicode-ms.ttf", CARD_WIDTH//3)
ACE_PILE_FONT = pygame.font.Font("arial-unicode-ms.ttf", CARD_WIDTH - 10)

DISP_TYPE = {
    "queen":"Q",
    "king":"K",
    "jack":"J",
    "ace":"A"
}

DISP_SUIT = {
    "hearts":"♡",
    "clubs":"♣",
    "spades":"♠",
    "diamonds":"♢"
}