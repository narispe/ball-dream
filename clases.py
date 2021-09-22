import numpy as np
import pygame as pg
from func import vect_vel, impulse
import param as p


class Circle:  # rgb, center, radio, width, vect_dir, rap

    def __init__(self, rgb, center, radio, width, vect_dir, rap):
        self.rgb = rgb
        self.center = np.array(center)
        self.radio = radio
        self.width = width
        self.rap = rap
        self.vel = vect_vel(vect_dir, self.rap)

    def draw(self, screen):
        pg.draw.circle(screen, self.rgb, self.center, self.radio, self.width)

    def move(self):
        self.center = np.round(self.center + self.vel)
        self.check_wall()

    def check_wall(self):  # PAREDES -> CORREC CENTER + IMPULSO
        if self.center[0] + self.radio > p.XMAX:
            self.center[0] = p.XMAX-self.radio
            self.vel[0] *= -p.COEF
        elif self.center[0] - self.radio < 0:
            self.center[0] = self.radio
            self.vel[0] *= -p.COEF
        elif self.center[1] + self.radio > p.YMAX:
            self.center[1] = p.YMAX-self.radio
            self.vel[1] *= -p.COEF
        elif self.center[1] - self.radio < 0:
            self.center[1] = self.radio
            self.vel[1] *= -p.COEF

    def is_col(self, c2):  # COLISION -> CORREC CENTER
        ratio = self.radio + c2.radio + 1
        vect = c2.center - self.center
        dist = np.linalg.norm(vect)
        if dist <= ratio:
            v_correc = np.round((ratio/dist)*vect) + 1
            self.center = np.round(c2.center - v_correc)
            return True
        else:
            return False

    def collide(self, c2):  # COLISION -> IMPULSO
        n = c2.center-self.center
        if p.PHYSICS:
            self.vel, self.rap, c2.vel, c2.rap = impulse(n, self, c2, e=p.COEF)
        else:
            self.vel = vect_vel(-n, self.rap)
            c2.vel = vect_vel(n, self.rap)

    def __repr__(self):
        # return f"{self.rgb} | {self.center}"
        # return f"{self.rgb} | {np.round(self.vel,3)}"
        return str(self.rgb)


class Box:

    def __init__(self, screen, clock, font):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.info = ""
        self.circles = []

    def add(self, circle):
        self.circles.append(circle)

    def remove(self):
        self.circles.pop()

    def update(self):
        for c in self.circles:
            c.move()
            for c2 in self.circles:
                if c2 != c and c.is_col(c2):
                    c.collide(c2)
            c.draw(self.screen)

        teo = 0
        momentum = 0
        for c in self.circles:
            momentum += c.rap*(c.radio**2)
            teo += p.VEL*(c.radio**2)
        dif = (momentum-teo)
        self.info = (f"FPS: {round(self.clock.get_fps())}"
                     f"    N: {len(self.circles)}"
                     f"    VEL: {round(p.VEL*p.FPS)}"
                     f"    DIF: {round(dif)}"
                     f"    {round(100*dif/teo)}%")
        self.update_draw()

    def update_draw(self):
        self.screen.blit(self.font.render(self.info, True, (255, 255, 255)),
                         (0, 0))
        pg.display.flip()
        self.clock.tick(p.FPS)
        self.screen.fill((0, 0, 0))

    def change_vel(self, change):
        if change != 0:
            accel = (10/p.FPS)*change
            p.VEL += accel
            for c in self.circles:
                c.rap += accel
                c.vel = vect_vel(c.vel, c.rap)
        else:
            for c in self.circles:
                c.rap = p.VEL
                c.vel = vect_vel(c.vel, c.rap)
