import pygame

import settings

class GameButton:
    unhover_colour = 'white'
    hover_colour = (200,200,200)

    def __init__(self, text: str, center_pos: tuple[float,float], action):
        self.text_rect = pygame.Rect(0,0,0,0)
        self.text = text
        self.center_pos = center_pos

        self.colour = self.unhover_colour

        self.action = action
    
    def draw(self, surface: pygame.Surface) -> None:
        """draws GameButton to surface"""
        text = settings.GAME_BUTTON_FONT.render(self.text, True, self.colour)
        self.text_rect = text.get_rect(center = self.center_pos)

        surface.blit(text, self.text_rect)

    def update(self) -> None:
        """called once per frame"""
        self.click()
    
    def click(self) -> None:
        if not self.text_rect.collidepoint(pygame.mouse.get_pos()):
            self.colour = self.unhover_colour
            return
       
        self.colour = self.hover_colour
        if pygame.mouse.get_pressed()[0]:
           self.action()