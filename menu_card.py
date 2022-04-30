import pygame

from card import Card
import settings

class MenuCard(Card):
    def __init__(self, type: str):
        super().__init__([], "spades", type)
        self.draggable = True
        self.rect.width = 60
    
    def update(self, menu) -> None:
        """called once per frame"""
        self.drag(menu)
    
    def drag(self, menu) -> None:
        """logic for dragging card"""
        if menu.card_being_dragged != None and menu.card_being_dragged != self: return

        left_mouse = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if not self.is_being_dragged and left_mouse and self.rect.collidepoint(mouse_pos): # start dragging card
            self.drag_offset = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(mouse_pos)
            self.is_being_dragged = True
            menu.card_being_dragged = self
        
        if self.is_being_dragged and left_mouse: # dragging
            self.rect.center = mouse_pos + self.drag_offset
        elif self.is_being_dragged and not left_mouse: # let go
            self.is_being_dragged = False
            menu.card_being_dragged = None