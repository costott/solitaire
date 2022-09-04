import pygame, sys

import settings

class StartMenu:
    def __init__(self, caps: bool = False) -> None:
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.NOFRAME)
        self.clock = pygame.time.Clock()

        self.running = True

        self.title = settings.TITLE_FONT.render("solitaire" if not caps else "SOLITAIRE", True, 'white')
        self.title_rect = self.title.get_rect(center = (settings.WIDTH//2, 200))

        self.symbols = settings.TITLE_FONT.render("♡♣♠♢", True, 'white')
        self.symbols_rect = self.symbols.get_rect(center = (settings.WIDTH//2, self.title_rect.centery-(self.title_rect.height/2)-15))

        self.credits = settings.CREDIT_FONT.render("by costott", True, 'white')
        self.credits_rect = self.credits.get_rect(midtop = (settings.WIDTH/2, self.title_rect.bottom - 10))

        play_button = Button("PLAY", (250, 125), 40, (settings.WIDTH//2, settings.HEIGHT//2+50), self.exit_menu)
        exit_button = Button("EXIT", (100, 50), 20, (settings.WIDTH//2, play_button.rect.centery+play_button.rect.height/2 + 50), self.close_game)
        self.buttons = [play_button, exit_button]

        self.bars = [pygame.Rect(0, 0, settings.WIDTH, 50), pygame.Rect(0, settings.HEIGHT-50, settings.WIDTH, 50)]

    def run(self) -> None:
        """runs the start menu"""
        while self.running:
            self.clock.tick(settings.FPS)
            self.update()
    
    def update(self) -> None:
        """called once per frame"""
        pygame.event.get()

        self.screen.fill(settings.BACKGROUND_COLOUR)
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.symbols, self.symbols_rect)
        self.screen.blit(self.credits, self.credits_rect)

        for button in self.buttons:
            button.draw(self.screen)
            button.update()

        for bar in self.bars: pygame.draw.rect(self.screen, (49, 49, 49), bar)

        pygame.display.update()
    
    def exit_menu(self) -> None:
        self.running = False
    
    def close_game(self) -> None:
        pygame.quit()
        sys.exit()

class Button:
    unhover_colour = settings.BACKGROUND_COLOUR
    hover_colour = "#4dab5e"
    hover_speed = 2

    def __init__(self, text: str, size: tuple[float,float], text_size: int, center_pos: tuple[float,float], action):
        """size: (width, height)"""
        self.rect = pygame.Rect(0,0,size[0],size[1])
        self.rect.center = center_pos

        self.size = pygame.math.Vector2(size[0], size[1])
        self.unhover_size = self.size.copy()
        self.hover_size = pygame.math.Vector2(size[0]+20, size[1]+20)

        self.text = pygame.font.Font("arial-unicode-ms.ttf", text_size).render(text, True, 'white')
        self.text_rect = self.text.get_rect()
        self.text_rect.center = center_pos

        self.colour = self.unhover_colour

        self.action = action
    
    def draw(self, surface: pygame.Surface) -> None:
        """draws the button onto the given surface"""
        pygame.draw.rect(surface, self.colour, self.rect)
        pygame.draw.rect(surface, 'white', self.rect, 5, 5)
        surface.blit(self.text, self.text_rect)
    
    def update(self) -> None:
        """called once per frame"""
        self.click()
    
    def click(self) -> None:
        """checks if button is clicked"""
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colour = self.unhover_colour
            if self.size.x > self.unhover_size.x:
                self.size.x -= self.hover_speed
                self.size.y -= self.hover_speed
                self.rect = pygame.Rect(0,0, self.size.x, self.size.y)
                self.rect.center = self.text_rect.center
            return
       
        self.colour = self.hover_colour
        if self.size.x < self.hover_size.x:
            self.size.x += self.hover_speed
            self.size.y += self.hover_speed
            self.rect = pygame.Rect(0,0, self.size.x, self.size.y)
            self.rect.center = self.text_rect.center
        if pygame.mouse.get_pressed()[0]:
           self.action()