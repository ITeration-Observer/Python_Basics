import pygame as pg


class ENGINE:
    def __init__(self):
        self.settings = self.SETTINGS
        self.logic = self.LOGIC
        self.window = self.WINDOW

    class SETTINGS:
        def __init__(self, **config):
            self.TITLE = config['TITLE']
            self.FPS = config['FPS']
            self.HEIGHT = config['HEIGHT']
            self.WIDTH = config['WIDTH']
            self.TILE = config['TILE']
            self.SCREEN_SIZE = self.WIDTH * self.TILE, self.HEIGHT * self.TILE
            ######
            self.colors = {
                            'black': (0, 0, 0),
                            'white': (255, 255, 255),
                            'sky': (87, 174, 209),
                            'sand': (255, 234, 0),
                            'water': (15, 94, 156),
                            'wall': (105, 105, 105)
                          }
            ######
            self.brick = [pg.Rect(self.TILE * y, self.TILE * x, self.TILE, self.TILE)
                          for x in range(self.WIDTH) for y in range(self.HEIGHT)]
            self.brick_colors = [self.colors['sky']
                                 for _ in range(self.WIDTH * self.HEIGHT)]
            self.default_key = 1
            self.pause = False

    class LOGIC:
        def __init__(self,  **_c_copy):
            self.c_copy = _c_copy
            ###########
            self.Tmap = []
            self.waterLevel = ''
            self.FountPoint_y, self.FountPoint_x = 0, 0

        def IfIn(self, y: int, x: int):
            return (x < 0 or y < 0 or x >= self.c_copy['WIDTH'] or y >= self.c_copy['HEIGHT'])

        def MoveSand(self, y: int, x: int):
            for n in [0, -1, 1]:
                if not self.IfIn(y + 1, x+n):
                    if (self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + (x+n)] == self.c_copy['colors']['sky']
                            or self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + (x+n)] == self.c_copy['colors']['water'] and self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + (x+n)] != self.c_copy['colors']['wall']):
                        self.c_copy['brick_colors'][y * self.c_copy['WIDTH']
                                                    + x] = self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + (x+n)]
                        self.c_copy['brick_colors'][(
                                y+1) * self.c_copy['WIDTH'] + (x+n)] = self.c_copy['colors']['sand']
                        return

        def MoveWater(self, y: int, x: int):
            if not self.IfIn(y + 1, x):
                if self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + x] == self.c_copy['colors']['sky']:
                    self.c_copy['brick_colors'][y * self.c_copy['WIDTH'] + x] = self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + x]
                    self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + x] = self.c_copy['colors']['water']
                    return
            for up in [1, 0]:
                for down in [1, -1]:
                    if not self.IfIn(y + up, x+down):
                        if self.c_copy['brick_colors'][(y+up) * self.c_copy['WIDTH'] + (x+down)] == self.c_copy['colors']['sky']:
                            self.c_copy['brick_colors'][y * self.c_copy['WIDTH'] + x] = self.c_copy['brick_colors'][(
                                y+up) * self.c_copy['WIDTH'] + (x+down)]
                            self.c_copy['brick_colors'][(
                                y+up) * self.c_copy['WIDTH'] + (x+down)] = self.c_copy['colors']['water']
                            return
        ###################################################################################################################
        def FindWaterPath(self, y, x):
            if self.IfIn(y, x): return
            if y >= self.waterLevel and y > self.FountPoint_y:
                if self.Tmap[y * self.c_copy['WIDTH'] + x] == self.c_copy['colors']['sky']:
                    self.FountPoint_x = x
                    self.FountPoint_y = y
            if self.Tmap[y * self.c_copy['WIDTH'] + x] == self.c_copy['colors']['water']:
                self.Tmap[y * self.c_copy['WIDTH'] + x] = self.c_copy['colors']['wall']
                self.FindWaterPath(y-1, x)
                self.FindWaterPath(y+1, x)
                self.FindWaterPath(y, x-1)
                self.FindWaterPath(y, x+1)

        def NewMoveWater(self, y, x):
            if self.IfIn(y + 1, x): return
            if self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + x] == self.c_copy['colors']['sky']:
                self.c_copy['brick_colors'][y * self.c_copy['WIDTH'] + x] = self.c_copy['colors']['sky']
                self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + x] = self.c_copy['colors']['water']
            
            elif self.c_copy['brick_colors'][(y+1) * self.c_copy['WIDTH'] + x] == self.c_copy['colors']['water']:
                self.waterLevel = y + 1
                self.FountPoint_y = -1
                self.Tmap = self.c_copy['brick_colors'][:]
                self.FindWaterPath(y+1, x)
                if self.FountPoint_y >= 0:
                    self.c_copy['brick_colors'][self.FountPoint_y * self.c_copy['WIDTH'] + self.FountPoint_x] = self.c_copy['colors']['water']
                    self.c_copy['brick_colors'][y * self.c_copy['WIDTH'] + x] = self.c_copy['colors']['sky']
        ###################################################################################################################
        def MoveSubstance(self):
            for y in range(self.c_copy['HEIGHT']-1, 0-1, -1):
                for x in range(0, self.c_copy['WIDTH'], 1):
                    if self.c_copy['brick_colors'][y * self.c_copy['WIDTH'] + x] == self.c_copy['colors']['sand']:
                        self.MoveSand(y, x)
                    if self.c_copy['brick_colors'][y * self.c_copy['WIDTH'] + x] == self.c_copy['colors']['water']:
                        # self.MoveWater(y, x)
                        self.NewMoveWater(y ,x)

    class WINDOW(LOGIC):
        def __init__(self, **_c_copy):
            self.c_copy = _c_copy
            pg.display.set_caption(self.c_copy['TITLE'])
            self.clock = pg.time.Clock()
            self.window = pg.display.set_mode(
                self.c_copy['SCREEN_SIZE'])
            pg.init()

        def Events(self):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.c_copy['default_key'] = 1
                    elif event.key == pg.K_2:
                        self.c_copy['default_key'] = 2
                    elif event.key == pg.K_3:
                        self.c_copy['default_key'] = 3
                    elif event.key == pg.K_e:
                        if self.c_copy['pause'] == False:
                            self.c_copy['pause'] = True
                        else:
                            self.c_copy['pause'] = False
                    elif event.key == pg.K_q:
                        self.c_copy['brick_colors'] = [self.c_copy['colors']['sky'] for _ in range(
                            self.c_copy['WIDTH'] * self.c_copy['HEIGHT'])]
            if not(self.c_copy['pause']):
                self.MoveSubstance()
            for y in range(self.c_copy['HEIGHT']):
                for x in range(self.c_copy['WIDTH']):
                    if pg.mouse.get_pressed()[0] and self.c_copy['brick'][y * self.c_copy['WIDTH'] + x].collidepoint(pg.mouse.get_pos()) and self.c_copy['brick_colors'][y * self.c_copy['WIDTH'] + x] == self.c_copy['colors']['sky']:
                        if self.c_copy['default_key'] == 1:
                            self.c_copy['brick_colors'][y * self.c_copy['WIDTH']
                                                        + x] = self.c_copy['colors']['sand']
                        elif self.c_copy['default_key'] == 2:
                            self.c_copy['brick_colors'][y * self.c_copy['WIDTH']
                                                        + x] = self.c_copy['colors']['water']
                        elif self.c_copy['default_key'] == 3:
                            self.c_copy['brick_colors'][y * self.c_copy['WIDTH']
                                                        + x] = self.c_copy['colors']['wall']
                    elif pg.mouse.get_pressed()[2] and self.c_copy['brick'][y * self.c_copy['WIDTH'] + x].collidepoint(pg.mouse.get_pos()):
                        self.c_copy['brick_colors'][y * self.c_copy['WIDTH']
                                                    + x] = self.c_copy['colors']['sky']
                    pg.draw.rect(
                        self.window, self.c_copy['brick_colors'][y * self.c_copy['WIDTH'] + x], self.c_copy['brick'][y * self.c_copy['WIDTH'] + x])

        def Inner(self):
            self.window.fill(self.c_copy['colors']['black'])
            self.Events()
            pg.display.update()
            self.clock.tick(self.c_copy['FPS'])

        def Loop(self):
            while True:
                self.Inner()


if __name__ == '__main__':
    engine = ENGINE()
    settings_engine = engine.SETTINGS(
        HEIGHT=60, WIDTH=60, TILE=10, FPS=60, TITLE='...')
    logic_engine = engine.LOGIC(**settings_engine.__dict__)
    window_engine = engine.WINDOW(**settings_engine.__dict__)
    # print(logic_engine.__dict__)
    window_engine.Loop()