import pygame as pg
from pygame.locals import *
import random
import math

snake_color = (0, 255, 0)


class Maze(pg.sprite.Sprite):
    bgcolor = (255, 255, 255)

    def __init__(self):
        super().__init__()
        pg.init()
        self.SW, self.SH = 600, 600

        fps = 15
        input_time = 60
        self.clock = pg.time.Clock()
        self.bs = 16
        self.surface = pg.display.set_mode((self.SW, self.SH))

        self.snake_list = []

        self.points = 0
        self.food_loc = [random.randint(5, 20), random.randint(5, 20)]
        self.movement = [1, 0]
        self.head = self.create_head()
        self.body = self.create_body(12, 12)
        self.food = self.create_food()

        is_Started = {"ON": False, "GO": False}

        title = pg.font.Font('src\\font\\MeriendaOne-Regular.ttf', 72).render("Snake", True, (0, 0, 128))
        info = pg.font.Font('src\\font\\RobotoSlab-Bold.ttf', 14).render("Press [SPACE] to start.", True, (int(math.fabs(self.bgcolor[0] - 255)), int(math.fabs(self.bgcolor[1] - 255)), int(math.fabs(self.bgcolor[2] - 255))))
        while True:
            for e in pg.event.get():
                if e.type is KEYDOWN and e.key == K_RETURN and (e.mod & (KMOD_LALT | KMOD_RALT)) != 0:
                    self.surface = self.toggle_fullscreen()
                    self.SW, self.SH = self.surface.get_width(), self.surface.get_height()

                if e.type == pg.QUIT:
                    pg.quit()
                    quit()

            pressed = pg.key.get_pressed()
            if pressed[pg.K_SPACE]:
                is_Started["ON"] = True
                is_Started["GO"] = False

            self.surface.fill(self.bgcolor)
            self.fill_object(self.food, (int(math.fabs(self.bgcolor[0] - 255)), int(math.fabs(self.bgcolor[1] - 255)), int(math.fabs(self.bgcolor[2] - 255))))
            if is_Started["ON"]:
                if (pressed[pg.K_UP] or pressed[pg.K_w]) and self.movement != [0, 1]:
                    self.movement = [0, -1]
                if (pressed[pg.K_DOWN] or pressed[pg.K_s]) and self.movement != [0, -1]:
                    self.movement = [0, 1]
                if (pressed[pg.K_RIGHT] or pressed[pg.K_d]) and self.movement != [-1, 0]:
                    self.movement = [1, 0]
                if (pressed[pg.K_LEFT] or pressed[pg.K_a]) and self.movement != [1, 0]:
                    self.movement = [-1, 0]

                self.blit_head()
                self.blit_body()
                self.blit_food()
                last_location = self.snake_list[-1]
                if self.SW // self.bs > self.snake_list[0][0] >= 0 // self.bs and self.SH // self.bs > self.snake_list[0][1] >= 0:
                    self.snake_list.insert(0, [self.snake_list[0][0] + self.movement[0], self.snake_list[0][1] + self.movement[1]])
                    del self.snake_list[len(self.snake_list) - 1]
                else:
                    self.new_game()
                    is_Started["GO"] = True
                    is_Started["ON"] = False
                if self.snake_list[0] in self.snake_list[1:]:
                    self.new_game()
                    is_Started["GO"] = True
                    is_Started["ON"] = False
                if self.snake_list[0] == self.food_loc:
                    self.food_loc = [random.randint(5, 20), random.randint(5, 20)]
                    self.points += 1
                    self.lvl_up(last_location)
            elif is_Started["GO"]:
                self.game_over()
            else:
                self.surface.blit(title, ((self.SW // 2) - (title.get_width()//2), (self.SH // 2) - (title.get_height() // 2)))
                self.surface.blit(info, ((self.SW // 2) - (info.get_width()//2), (self.SH // 2) + (title.get_height() // 2)))

            pg.time.delay(input_time * 15 // fps)
            self.clock.tick(input_time)
            pg.display.update()

    @staticmethod
    def fill_object(pixels, rong):
        w, h = pixels.get_size()
        r, g, b = rong
        for x in range(w):
            for y in range(h):
                a = pixels.get_at((x, y))[3]
                pixels.set_at((x, y), pg.Color(r, g, b, a))
        pass

    def create_body(self, x, y):
        body = []
        snake_body = []
        for i in range(1, 4):
            snake_body.append([x - i, y])

        for _ in snake_body:
            body.append(pg.image.load('src\\imgs\\Body.png'))
        self.snake_list = []
        self.snake_list.append([x, y])
        self.snake_list.extend(snake_body)
        return body

    @staticmethod
    def create_head():
        return pg.image.load('src\\imgs\\Head.png')

    @staticmethod
    def create_food():
        return pg.transform.rotozoom(pg.image.load('src\\imgs\\Food.png').convert_alpha(), 0, 1)

    def blit_head(self):
        self.surface.blit(self.head, (self.snake_list[0][0] * self.bs, self.snake_list[0][1] * self.bs))
        pass

    def blit_body(self):
        for i in range(len(self.body)):
            self.surface.blit(self.body[i], (self.snake_list[i+1][0] * self.bs, self.snake_list[i+1][1] * self.bs))
        pass

    def blit_food(self):
        self.surface.blit(self.food, (self.food_loc[0] * self.bs, self.food_loc[1] * self.bs))
        pass

    def lvl_up(self, loc):
        self.body.append(pg.image.load('src\\imgs\\Body.png'))
        self.snake_list.append(loc)
        pass

    def game_over(self):
        g_over = pg.font.Font('src\\font\\MeriendaOne-Regular.ttf', 72).render("Game Over", True, (255, 0, 0))
        sc_txt = pg.font.Font('src\\font\\RobotoSlab-Bold.ttf', 32).render("Your Score is "+str(self.points), True, (int(math.fabs(self.bgcolor[0] - 255)), int(math.fabs(self.bgcolor[1] - 255)), int(math.fabs(self.bgcolor[2] - 255))))
        self.surface.fill(self.bgcolor)
        self.surface.blit(g_over, ((self.SW // 2) - (g_over.get_width() // 2), (self.SH // 2) - (g_over.get_height() // 2)))
        self.surface.blit(sc_txt, ((self.SW // 2) - (sc_txt.get_width() // 2), (self.SH // 2) + (sc_txt.get_height() // 2)))
        pass

    def toggle_fullscreen(self):
        screen = pg.display.get_surface()
        tmp = screen.convert()
        caption = pg.display.get_caption()
        cursor = pg.mouse.get_cursor()

        w, h = screen.get_width(), screen.get_height()
        flags = screen.get_flags()
        bits = screen.get_bitsize()

        pg.display.quit()
        pg.display.init()

        screen = pg.display.set_mode((w, h), flags ^ FULLSCREEN, bits)
        screen.blit(tmp, (0, 0))
        pg.display.set_caption(*caption)
        self.SW, self.SH = w, h
        pg.mouse.set_cursor(*cursor)  # Duoas 16-04-2007

        return screen

    def new_game(self):
        self.movement = [1, 0]
        self.body = self.create_body(random.randint(5, 20), random.randint(5, 20))
        pass


