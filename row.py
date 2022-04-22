import pygame

from card import Card
import settings

class Row:
    def __init__(self, cards: list[Card], top_card_center_pos: tuple[float, float]):
        self.cards = cards
        self.top_card_center_pos = top_card_center_pos

        self.rect = pygame.Rect(0,0, settings.CARD_WIDTH+settings.CARD_X_GAP, settings.HEIGHT)
        self.rect.centerx = top_card_center_pos[0]

        self.visible_cards = []
        self.reveal_top()
    
    def reveal_top(self) -> None:
        """reveals the top card"""
        if len(self.cards) == 0 or len(self.visible_cards) > 0:
            return

        self.visible_cards = [self.cards[len(self.cards)-1]]
        self.cards[len(self.cards)-1].draggable = True
    
    def draw(self, display_surface: pygame.Surface,) -> None:
        """draws row to display surface"""
        for i, card in enumerate(self.cards):
            pos = (self.top_card_center_pos[0], self.top_card_center_pos[1]+i*(36))
            if card.draggable:
                card.draw(display_surface, pos)
            else:
                card_back = pygame.Rect((0,0), (settings.CARD_WIDTH, settings.CARD_HEIGHT))
                card_back.center = pos
                pygame.draw.rect(display_surface, settings.BACK_CARD_BORDER_COLOUR, card_back.inflate(5,6), border_radius=settings.CARD_RAD)
                pygame.draw.rect(display_surface, settings.BACK_CARD_COLOUR, card_back, border_radius=settings.CARD_RAD)
    
    def update(self, game) -> None:
        """called once per frame"""
        for card in reversed(self.cards):
            card.update(game, self)

class AceRow:
    def __init__(self, suit: str, center_pos: tuple[float, float]):
        self.cards = []
        self.rect = pygame.Rect(0,0, settings.CARD_WIDTH, settings.CARD_HEIGHT)
        self.rect.center = center_pos

        self.suit = suit

        self.visible_cards = []

        self.colour = "red" if self.suit in ["hearts", "diamonds"] else "white"
        self.disp_suit = settings.ACE_PILE_FONT.render(settings.DISP_SUIT[self.suit], True, self.colour)
        self.disp_suit_rect = self.disp_suit.get_rect(center = self.rect.center)

    def draw(self, display_surface: pygame.Surface) -> None:
        """draws top card in ace pile"""
        card_back = pygame.Rect((0,0), (settings.CARD_WIDTH, settings.CARD_HEIGHT))
        card_back.center = self.rect.center
        pygame.draw.rect(display_surface, settings.BACK_CARD_BORDER_COLOUR, card_back.inflate(6,6), border_radius=settings.CARD_RAD)
        pygame.draw.rect(display_surface, '#34A249', card_back, border_radius=settings.CARD_RAD)
        display_surface.blit(self.disp_suit, self.disp_suit_rect)

        if len(self.cards) >= 2:
            self.cards[len(self.cards)-2].draw(display_surface, self.rect.center)

        if len(self.cards) > 0:
            self.cards[len(self.cards)-1].draw(display_surface, self.rect.center)
    
    def update(self, game) -> None:
        """called once per frame"""
        if len(self.cards) > 0: 
            self.cards[len(self.cards)-1].update(game, self)

    def reveal_top(self) -> None:
        """makes the next top card draggable"""
        if len(self.cards) > 0: self.cards[len(self.cards)-1].draggable = True