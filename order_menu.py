import pygame

from menu_card import MenuCard
from startmenu import Button
import settings

class OrderMenu:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.NOFRAME)
        self.clock = pygame.time.Clock()

        self.running = True

        self.bars = [pygame.Rect(0, 0, settings.WIDTH, 50), pygame.Rect(0, settings.HEIGHT-50, settings.WIDTH, 50)]
        self.title_text = settings.ORDER_MENU_TITLE_FONT.render("CARD ORDER", True, 'white')
        self.title_text_rect = self.title_text.get_rect(center = (settings.WIDTH//2, self.bars[0].centery))

        self.type_order = ["ace"] + [str(i) for i in range(2,11)] + ["jack", "king", "queen"]
        self.cards = [MenuCard(type) for type in self.type_order]
        self.card_being_dragged = None

        self.confirm_button = Button("PLAY", (200, 100), 40, (settings.WIDTH//2, settings.HEIGHT//2+175), self.exit_menu)
    
    def run(self) -> None:
        """runs the order menu"""
        while self.running:
            self.clock.tick(settings.FPS)
            self.update()
        return self.type_order
    
    def update(self) -> None:
        """called once per frame"""
        pygame.event.get()

        self.screen.fill(settings.BACKGROUND_COLOUR)

        for bar in self.bars: pygame.draw.rect(self.screen, (49, 49, 49), bar)
        self.screen.blit(self.title_text, self.title_text_rect)

        self.confirm_button.draw(self.screen)
        if self.card_being_dragged == None: self.confirm_button.update()

        self.draw_cards()
        if self.card_being_dragged != None: self.card_being_dragged.draw(self.screen, (self.card_being_dragged.rect.centerx, self.card_being_dragged.rect.centery))
        for card in self.cards: 
            card.update(self)

        pygame.display.update()
    
    def draw_cards(self) -> None:
        """draws cards to screen"""
        for i, card in enumerate(self.cards):
            pos = (card.rect.width/2+7+i*(card.rect.width+8), settings.HEIGHT//2)
            card.draw(self.screen, pos)
    
    def exit_menu(self) -> None:
        self.running = False