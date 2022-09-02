import pygame

from card import Card
import settings

class StockPile:
    def __init__(self, cards: list[Card]):
        self.cards = cards
        self.drawn_cards = []
        self.center_pos = (settings.CARD_WIDTH//2 + settings.CARD_X_GAP/2, settings.INFO_HEIGHT + settings.CARD_HEIGHT//2 + 10)
        self.drawn_pos = (self.center_pos[0], self.center_pos[1]+settings.CARD_HEIGHT + 10)

        self.top_card = pygame.Rect((0,0), (settings.CARD_WIDTH, settings.CARD_HEIGHT))
        self.top_card.center = self.center_pos

        self.active_card = None

        self.clicked = False
    
    def draw(self, display_surface: pygame.Surface) -> None:
        """draws the stock pile and (active pile if there is one)"""
        if len(self.cards) == 0:
            placeholder = pygame.Rect(0,0, settings.CARD_WIDTH, settings.CARD_HEIGHT)
            placeholder.center = self.center_pos
            placeholder.inflate(6,6)
            pygame.draw.rect(display_surface, settings.CARD_BORDER_COLOUR, placeholder, border_radius=settings.CARD_RAD)
        if len(self.cards) > 0:
            pygame.draw.rect(display_surface, settings.CARD_BORDER_COLOUR, self.top_card.inflate(5,6), border_radius=settings.CARD_RAD)
            pygame.draw.rect(display_surface, settings.BACK_CARD_COLOUR, self.top_card, border_radius=settings.CARD_RAD)

        for card in self.drawn_cards[len(self.drawn_cards)-2:len(self.drawn_cards)]:
            card.draw(display_surface, self.drawn_pos)

    def update(self, game) -> None:
        """called once per frame"""
        self.click(game)
        
        if self.active_card != None: 
            self.active_card.update(game, self)
    
    def click(self, game) -> None:
        """logic for being clicked"""
        if (self.active_card != None and self.active_card.is_being_dragged) or game.card_being_dragged: # not dragging anything
            return

        mouses_pressed = pygame.mouse.get_pressed()
        if not mouses_pressed[0]:
            self.clicked = False
            return
    
        m_x, m_y = pygame.mouse.get_pos()
        if self.top_card.collidepoint(m_x, m_y) and not self.clicked:
            if len(self.cards) == 0 and len(self.drawn_cards) > 0: 
                self.drawn_to_main()
                return
            if len(self.cards) == 0 and len(self.drawn_cards) == 0:
                return

            if self.active_card != None: self.active_card.draggable = False
            self.active_card = self.cards.pop(len(self.cards)-1)
            self.active_card.draggable = True
            self.drawn_cards.append(self.active_card)
            self.clicked = True

            game.moves += 1
        
    def drawn_to_main(self):
        """puts the cards in the drawn cards pile into the main card pile"""
        self.drawn_cards.reverse()
        self.cards = self.drawn_cards.copy()
        self.drawn_cards.clear()
        self.clicked = True