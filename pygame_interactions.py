import pygame
import base
import objects


class GameEngineGateway(base.GameEngineGateway):

    def __init__(self):
        self._background_color = (0,0,0)

    def make_world(self,shape:tuple):
        pygame.init()
        self._screen = pygame.display.set_mode(shape)
        self._clock = pygame.time.Clock()

        self._screen.fill(self._background_color)


    def update_circles(self,circles:list[base.Circle]):
        self._check_quit()


        self._screen.fill(self._background_color)

        for circle in circles:
            faint_color = pygame.Color((*circle.colour, circle.alpha)).premul_alpha()
            pygame.draw.circle(self._screen, faint_color, circle.centre, circle.radius)

        pygame.display.flip()


    def get_keyboard_displacement(self,step) -> tuple[float,float]:

        self._check_quit()

        dt = self._get_timestep()
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        if keys[pygame.K_w]:
            dy -= step * dt
        if keys[pygame.K_s]:
            dy += step * dt
        if keys[pygame.K_a]:
            dx -= step * dt
        if keys[pygame.K_d]:
            dx += step * dt
        return dx,dy



    def _check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise base.UserHasQuitException()

    def _get_timestep(self) -> float:
        dt = self._clock.tick(60) / 1000
        return dt

