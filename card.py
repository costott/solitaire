import pygame

import settings

class Card(pygame.sprite.Sprite):
    def __init__(self, groups: list, suit: str, type: str):
        super().__init__(groups)
        self.suit = suit
        self.type = type

        self.rect =  pygame.Rect((0,0), (settings.CARD_WIDTH, settings.CARD_HEIGHT))

        self.colour = "red" if self.suit in ["hearts", "diamonds"] else "white"
        self.type_text = settings.DISP_TYPE[self.type] if not self.type.isnumeric() else self.type
        self.disp_type = settings.CARD_FONT.render(self.type_text, True, self.colour)

        self.disp_suit = settings.CARD_FONT.render(settings.DISP_SUIT[self.suit], True, self.colour)

        self.draggable = False
        self.drag_offset = pygame.math.Vector2()
        self.is_being_dragged = False

        self.tether = None # card attached to it
    
    def draw(self, display_surface: pygame.Surface, center_pos: tuple[float, float]) -> None:
        """draws card onto surface"""
        if not self.is_being_dragged: 
            self.rect.center = center_pos
        pygame.draw.rect(display_surface, self.colour, self.rect.inflate(5,6), border_radius=settings.CARD_RAD)
        pygame.draw.rect(display_surface, 'black', self.rect, border_radius=settings.CARD_RAD)

        disp_type_rect = self.disp_type.get_rect(topleft = (self.rect.topleft[0]+5, self.rect.topleft[1]+5))
        display_surface.blit(self.disp_type, disp_type_rect)

        disp_suit_rect = self.disp_suit.get_rect(topright = (self.rect.topright[0]-5, self.rect.topright[1]+5))
        display_surface.blit(self.disp_suit, disp_suit_rect)
    
    def draw_tether(self, display_surface: pygame.Surface) -> None:
        pygame.draw.rect(display_surface, self.colour, self.rect.inflate(5,6), border_radius=settings.CARD_RAD)
        pygame.draw.rect(display_surface, 'black', self.rect, border_radius=settings.CARD_RAD)

        disp_type_rect = self.disp_type.get_rect(topleft = (self.rect.topleft[0]+5, self.rect.topleft[1]+5))
        display_surface.blit(self.disp_type, disp_type_rect)

        disp_suit_rect = self.disp_suit.get_rect(topright = (self.rect.topright[0]-5, self.rect.topright[1]+5))
        display_surface.blit(self.disp_suit, disp_suit_rect)

        if self.tether != None:
            self.tether.draw_tether(display_surface)
    
    def update(self, game, current_row) -> None:
        """called once per frame"""
        self.drag(game, current_row)
    
    def tether_cards(self) -> None:
        """tethers all cards down row to drag them"""
        if self.tether != None:
            self.tether.is_being_dragged = True
            self.tether.rect.x = self.rect.x
            self.tether.rect.y = self.rect.y + 36
            self.tether.tether_cards()
    
    def untether_cards(self) -> None:
        """stop making tethered cards being dragged"""
        if self.tether != None:
            self.tether.is_being_dragged = False
            self.tether.untether_cards()

    def drag(self, game, current_row) -> None:
        """drags card"""
        if not self.draggable or (game.card_being_dragged != None and game.card_being_dragged != self): return

        left_mouse = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if not self.is_being_dragged and left_mouse and self.rect.collidepoint(mouse_pos): # start dragging card
            self.drag_offset = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(mouse_pos)
            self.is_being_dragged = True
            game.card_being_dragged = self
        
        if self.is_being_dragged and left_mouse: # dragging
            self.rect.center = mouse_pos + self.drag_offset
            self.tether_cards()
        elif self.is_being_dragged and not left_mouse: # let go
            swapped_row = self.let_go_card(game, mouse_pos, current_row)
            if swapped_row: game.moves += 1

    def let_go_card(self, game, mouse_pos: tuple, current_row) -> bool:
        """lets go of card. will swap rows if it's let down onto an available row\n
        returns if it swapped rows"""
        self.is_being_dragged = False
        game.card_being_dragged = None

        for row in game.card_rows:
            if not row.rect.collidepoint(mouse_pos): continue

            if len(row.cards) == 0 and self.type == game.type_order[-1]:
                self.switch_row(current_row, row)
                return True
            elif len(row.cards) == 0:
                return False
                
            wants_index = game.type_order.index(row.cards[len(row.cards)-1].type) - 1
            wants_suit = ["hearts", "diamonds"] if row.cards[len(row.cards)-1].suit in ["clubs", "spades"] else ["clubs", "spades"]
            if game.type_order[wants_index] == self.type and wants_index >= 0 and self.suit in wants_suit:
                self.switch_row(current_row, row)
                row.cards[len(row.cards)-2].tether = self
                if self.tether != None:
                    self.tether.let_go_card(game, mouse_pos, current_row)
                return True
        
        for row in game.ace_rows:
            if not row.rect.collidepoint(mouse_pos): continue

            if self in row.cards or self.tether != None: return False

            if self.type == "ace" and len(row.cards) == 0 and row.suit == self.suit:
                self.switch_row(current_row, row)
                return True
            elif len(row.cards) == 0: continue

            wants_index = game.type_order.index(row.cards[len(row.cards)-1].type) + 1
            
            if game.type_order[wants_index] == self.type and wants_index >= 0 and self.suit == row.suit:
                self.switch_row(current_row, row)
                if self.tether != None:
                    self.tether.let_go_card(game, mouse_pos, current_row)
                return True
                
        return False

    def switch_row(self, current_row, row) -> None:
        """switches the card from the current row into the new one"""
        try:
            if len(current_row.cards) > 1: current_row.cards[current_row.cards.index(self)-1].tether = None
            current_row.cards.remove(self)
            current_row.visible_cards.remove(self)
            current_row.reveal_top()
        except ValueError: # remove from stock pile
            current_row.drawn_cards.remove(self)
            current_row.active_card = current_row.drawn_cards[len(current_row.drawn_cards)-1] if len(current_row.drawn_cards) > 0 else None
            if current_row.active_card != None: current_row.active_card.draggable = True

        row.cards.append(self)
        row.visible_cards.append(self)