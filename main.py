import pygame
import random

from game_buttons import GameButton
from stock_pile import StockPile
from order_menu import OrderMenu
from startmenu import StartMenu
from info_bar import InfoBar
from row import Row, AceRow
from card import Card
import settings

class Game:
    def __init__(self, type_order: list[str] = ["ace"] + [str(i) for i in range(2,11)] + ["jack", "king", "queen"]):
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.NOFRAME)
        self.clock = pygame.time.Clock()

        self.running = True

        self.type_order = type_order

        self.stock_pile = self.make_cards()
        random.shuffle(self.stock_pile)
        self.card_rows = self.make_start_rows()
        self.ace_rows = self.make_ace_rows()

        self.stock_pile = StockPile(self.stock_pile)

        self.info_bar = InfoBar(self.clock)
        new_game = GameButton("★ new", (settings.WIDTH//2, settings.HEIGHT-50), self.new_game)
        self.game_buttons = [new_game]

        self.card_being_dragged = None

        self.moves = 0
    
        self.make_won_screen()
        self.won = False
    
    def make_cards(self) -> list[Card]:
        """returns all 52 cards"""
        cards = []
        for suit in ["hearts", "clubs", "spades", "diamonds"]:
            for type in self.type_order:
                cards.append(Card([], suit, type))
        
        return cards
    
    def make_start_rows(self) -> list[Row]:
        """returns the starting rows witht their cards"""
        rows = []
        for i in range(7):
            row_cards = []
            for _ in range(i+1):
                card = self.stock_pile.pop(random.randint(0, len(self.stock_pile)-1))
                row_cards.append(card)
            row = Row(row_cards, (settings.CARD_WIDTH//2 + settings.CARD_X_GAP/2 + (i+1)*(settings.CARD_WIDTH + settings.CARD_X_GAP), settings.INFO_HEIGHT + settings.CARD_HEIGHT//2 + 10))
            rows.append(row)
        
        return rows
    
    def make_ace_rows(self) -> list[AceRow]:
        """reuturns a list of empty ace rows"""
        ace_rows = []
        for i, suit in enumerate(["hearts", "clubs", "spades", "diamonds"]):
            x = self.card_rows[len(self.card_rows)-1].top_card_center_pos[0] + (settings.CARD_WIDTH + settings.CARD_X_GAP)
            y = settings.INFO_HEIGHT + settings.CARD_HEIGHT//2 + 10 + i*(settings.CARD_HEIGHT + 10)
            ace_rows.append(AceRow(suit, (x,y)))
        
        return ace_rows
    
    def new_game(self) -> None:
        """starts new game by stopping current one"""
        self.running = False
    
    def make_won_screen(self) -> None:
        """makes screen to be displayed when a game is won"""
        self.won_screen = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        self.won_screen.fill(settings.WON_SCREEN_COLOUR)
        self.won_screen.set_alpha(settings.WON_SCREEN_ALPHA)

        self.won_text_rect = settings.WON_TEXT.get_rect(center = (settings.WIDTH/2, settings.HEIGHT/2))
    
    def check_won(self) -> None:
        """checks if the game is won"""
        if len(self.stock_pile.cards) == 0 and len(self.stock_pile.drawn_cards) == 0:
            won = True
            for row in self.card_rows:
                if len(row.cards) > len(row.visible_cards): won = False
            self.won = won
    
    def run(self) -> None:
        """runs the game"""
        while self.running:
            self.clock.tick(settings.FPS)
            self.update()
    
    def update(self) -> None:
        """called once per frame"""
        pygame.event.get()

        self.screen.fill(settings.BACKGROUND_COLOUR)

        if self.won:
            self.screen.blit(self.won_screen, (0,0))
            self.screen.blit(settings.WON_TEXT, self.won_text_rect)
        else:
            pygame.draw.rect(self.screen, (35, 115, 51), (0,0,settings.CARD_WIDTH+settings.CARD_X_GAP,settings.HEIGHT))
            pygame.draw.rect(self.screen, (35, 115, 51), ((settings.CARD_WIDTH+settings.CARD_X_GAP)*8, 0, settings.CARD_WIDTH+settings.CARD_X_GAP, settings.HEIGHT))

        self.info_bar.draw(self.screen, self.moves)
        self.info_bar.update(self.won)

        for button in self.game_buttons:
            button.draw(self.screen)
            if self.card_being_dragged is None: button.update()
        
        if self.won:
            pygame.display.update()
            return

        for row in self.card_rows:
            row.draw(self.screen)
            row.update(self)
        
        for row in self.ace_rows:
            row.draw(self.screen)
            row.update(self)
        
        self.stock_pile.draw(self.screen)
        self.stock_pile.update(self)

        if self.card_being_dragged != None: self.card_being_dragged.draw_tether(self.screen)

        self.check_won()

        pygame.display.update()

def main():
    order_menu = OrderMenu()
    menu = StartMenu(caps=True)
    menu.run()

    type_order = order_menu.run()

    while True:
        game = Game(type_order)
        game.run()

if __name__ == "__main__":
    main()