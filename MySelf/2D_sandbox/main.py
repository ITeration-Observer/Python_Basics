import pygame as pg
import random

class ParticleSim:
    def __init__(self, width=60, height=60, tile=10, fps=60):
        pg.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.TILE = tile
        self.FPS = fps
        
        self.colors = {
            'sky': (87, 174, 209),
            'sand': (255, 234, 0),
            'water': (15, 94, 156),
            'wall': (105, 105, 105),
            'black': (0, 0, 0)
        }
        
        self.screen = pg.display.set_mode((self.WIDTH*self.TILE, self.HEIGHT*self.TILE))
        pg.display.set_caption("Sandbox 2D")
        
        self.grid = [self.colors['sky'] for _ in range(self.WIDTH * self.HEIGHT)]
        self.rects = [pg.Rect(x*self.TILE, y*self.TILE, self.TILE, self.TILE) 
                     for y in range(self.HEIGHT) for x in range(self.WIDTH)]
        
        self.selected = 'sand'
        self.paused = False
        self.clock = pg.time.Clock()

    def get_index(self, x, y):
        return y * self.WIDTH + x

    def in_bounds(self, x, y):
        return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT

    def update_sand(self, x, y):
        index = self.get_index(x, y)
        for dx in [0, -1, 1]:
            if self.in_bounds(x+dx, y+1):
                below_idx = self.get_index(x+dx, y+1)
                if self.grid[below_idx] in (self.colors['sky'], self.colors['water']):
                    self.grid[index], self.grid[below_idx] = self.grid[below_idx], self.grid[index]
                    return

    def update_water(self, x, y):
        index = self.get_index(x, y)
        directions = random.sample([-1, 1], 2)  # Случайный порядок проверки
        
        # Падение вниз
        if self.in_bounds(x, y+1):
            below_idx = self.get_index(x, y+1)
            if self.grid[below_idx] == self.colors['sky']:
                self.grid[index], self.grid[below_idx] = self.grid[below_idx], self.grid[index]
                return
        
        # Растекание в стороны
        for dx in directions:
            if self.in_bounds(x+dx, y):
                side_idx = self.get_index(x+dx, y)
                if self.grid[side_idx] == self.colors['sky']:
                    self.grid[index], self.grid[side_idx] = self.grid[side_idx], self.grid[index]
                    return
        
        # Диагональное падение
        for dx in directions:
            if self.in_bounds(x+dx, y+1):
                diag_idx = self.get_index(x+dx, y+1)
                if self.grid[diag_idx] == self.colors['sky']:
                    self.grid[index], self.grid[diag_idx] = self.grid[diag_idx], self.grid[index]
                    return

    def handle_input(self):
        mouse_pos = pg.mouse.get_pos()
        grid_x = mouse_pos[0] // self.TILE
        grid_y = mouse_pos[1] // self.TILE
        
        if pg.mouse.get_pressed()[0] and self.in_bounds(grid_x, grid_y):
            idx = self.get_index(grid_x, grid_y)
            if self.grid[idx] == self.colors['sky']:
                self.grid[idx] = self.colors[self.selected]
        
        if pg.mouse.get_pressed()[2] and self.in_bounds(grid_x, grid_y):
            self.grid[self.get_index(grid_x, grid_y)] = self.colors['sky']

    def run(self):
        while True:
            self.screen.fill(self.colors['black'])
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1: self.selected = 'sand'
                    elif event.key == pg.K_2: self.selected = 'water'
                    elif event.key == pg.K_3: self.selected = 'wall'
                    elif event.key == pg.K_e: self.paused = not self.paused
                    elif event.key == pg.K_q: 
                        self.grid = [self.colors['sky'] for _ in range(self.WIDTH * self.HEIGHT)]

            if not self.paused:
                # Обработка снизу вверх для корректной симуляции
                for y in reversed(range(self.HEIGHT)):
                    for x in range(self.WIDTH) if random.choice([True, False]) else reversed(range(self.WIDTH)):
                        color = self.grid[self.get_index(x, y)]
                        if color == self.colors['sand']:
                            self.update_sand(x, y)
                        elif color == self.colors['water']:
                            self.update_water(x, y)

            # Отрисовка
            for i, rect in enumerate(self.rects):
                pg.draw.rect(self.screen, self.grid[i], rect)
            
            self.handle_input()
            pg.display.update()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = ParticleSim()
    game.run()
