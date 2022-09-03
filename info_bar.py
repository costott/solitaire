import pygame
import sys

import settings

class InfoBar:
    def __init__(self, clock: pygame.time.Clock):
        self.bar = pygame.Rect((0,0), (settings.WIDTH, settings.INFO_HEIGHT))

        self.timer = 0
        self.clock = clock

        self.exit_button = ExitButton((settings.WIDTH - 25, settings.INFO_HEIGHT/2))
    
    def update(self, game_won: bool) -> None:
        """called once per frame"""
        self.exit_button.update()

        if game_won: return

        fps = self.clock.get_fps()
        self.timer += 1/(fps if fps != 0 else 9999)

    def draw(self, display_surface: pygame.Surface, moves: int) -> None:
        """draws info bar to screen"""
        pygame.draw.rect(display_surface, (49, 49, 49), self.bar)

        disp_timer = settings.TIMER_FONT.render(self.to_hms(self.timer), True, 'white')
        disp_timer_rect = disp_timer.get_rect(center = self.bar.center)
        display_surface.blit(disp_timer, disp_timer_rect)

        disp_moves = settings.MOVES_FONT.render("moves", True, (175, 175, 175))
        disp_moves_rect = disp_moves.get_rect(midleft = (self.bar.left + 20, self.bar.centery))
        display_surface.blit(disp_moves, disp_moves_rect)
        disp_moves_num = settings.MOVES_FONT.render(str(moves), True, 'white')
        disp_moves_num_rect = disp_moves_num.get_rect(midleft = (disp_moves_rect.right + 10, disp_moves_rect.centery))
        display_surface.blit(disp_moves_num, disp_moves_num_rect)

        self.exit_button.draw(display_surface)
    
    def to_hms(self, time: int) -> str:
        """return the time (in seconds) into hours:minutes:seconds"""
        if time > 3600:
            hours = time//3600
            time -= 3600*hours 
        else: hours = 0

        if time > 60:
            minutes = time //60
            time -= 60*minutes
        else: minutes = 0

        return f"{int(hours):2}:{int(minutes):2}:{int(time):2}".replace(" ", "0")

class ExitButton:
    def __init__(self, pos: tuple):
        self.pos = pos
        self.rect = pygame.Rect(0,0,0,0)

        self.base_colour = 'white'
        self.hover_colour = (200,200,200)
        self.colour = self.base_colour
    
    def draw(self, display_surface: pygame.Surface) -> None:
        """draws exit button to screen"""
        text = settings.EXIT_FONT.render("✕", True, self.colour)
        self.rect = text.get_rect(center = self.pos)

        display_surface.blit(text, self.rect)
    
    def update(self) -> None:
        """called once per frame"""
        self.click()
    
    def click(self) -> None:
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colour = self.base_colour
            return
       
        self.colour = self.hover_colour
        if pygame.mouse.get_pressed()[0]:
           pygame.quit()
           sys.exit()