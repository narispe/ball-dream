import pygame as pg
from random import randint
import param as p
from func import randdir, randcolor
from clases import Circle, Box


pg.init()
pg.display.init()
pg.display.set_caption('BALL DREAM')
screen = pg.display.set_mode((p.XMAX, p.YMAX), pg.RESIZABLE)
screen.fill((0, 0, 0))
pg.font.init()
fuente = pg.font.SysFont('Lucida', 25)
clock = pg.time.Clock()


if __name__ == '__main__':

    running = True
    box = Box(screen, clock, fuente)
    box.add(Circle(randcolor(),
            (p.CX, p.CY),
            randint(p.RMIN, p.RMAX),
            randint(0, 1),
            randdir(),
            p.VEL))

    while running:
        box.update()

        for event in pg.event.get():

            if event.type == pg.QUIT \
                    or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                running = False

            if event.type == pg.VIDEORESIZE:
                p.XMAX, p.YMAX = screen.get_size()
                p.CX, p.CY = int(p.XMAX/2), int(p.YMAX/2)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_PLUS:
                    box.add(Circle(randcolor(),
                                   (p.CX, p.CY),
                                   randint(p.RMIN, p.RMAX),
                                   randint(0, 1),
                                   randdir(),
                                   p.VEL))

                if event.key == pg.K_MINUS:
                    box.remove()

                if event.key == pg.K_LEFT and p.FPS > 0:
                    p.VEL = (p.VEL*p.FPS)/(p.FPS-5)
                    p.FPS -= 5
                    box.change_vel(0)

                if event.key == pg.K_RIGHT and p.FPS > 0:
                    p.VEL = (p.VEL*p.FPS)/(p.FPS+5)
                    p.FPS += 5
                    box.change_vel(0)

                if event.key == pg.K_UP:
                    box.change_vel(1)

                if event.key == pg.K_DOWN:
                    box.change_vel(-1)

                if event.key == pg.K_SPACE:
                    box.change_vel(0)
