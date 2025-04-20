import pygame as pg
import random

class ParticleSim:
    def __init__(self, initial_width=80, initial_height=60, tile=8, fps=60):
        pg.init()
        self.TILE = tile
        self.FPS = fps
        
        self.colors = {
            'sky': (87, 174, 209),
            'sand': (255, 234, 0),
            'water': (15, 94, 156),
            'wall': (105, 105, 105),
            'black': (0, 0, 0)
        }
        
        initial_screen_width = initial_width * self.TILE
        initial_screen_height = initial_height * self.TILE
        self.screen = pg.display.set_mode((initial_screen_width, initial_screen_height), pg.RESIZABLE)
        pg.display.set_caption("Sandbox")
        
        self.WIDTH = initial_screen_width // self.TILE
        self.HEIGHT = initial_screen_height // self.TILE
        self.grid = [self.colors['sky'] for _ in range(self.WIDTH * self.HEIGHT)]
        self.grid_surface = pg.Surface((self.WIDTH*self.TILE, self.HEIGHT*self.TILE))
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
        directions = [0, -1, 1]
        random.shuffle(directions)
        
        for dx in directions:
            if self.in_bounds(x+dx, y+1):
                below_idx = self.get_index(x+dx, y+1)
                if self.grid[below_idx] in (self.colors['sky'], self.colors['water']):
                    self.grid[index], self.grid[below_idx] = self.grid[below_idx], self.grid[index]
                    return

    def update_water(self, x, y):
        index = self.get_index(x, y)
        directions = [-1, 1]
        random.shuffle(directions)
        
        if self.in_bounds(x, y+1):
            below_idx = self.get_index(x, y+1)
            if self.grid[below_idx] == self.colors['sky']:
                self.grid[index], self.grid[below_idx] = self.grid[below_idx], self.grid[index]
                return
        
        for dx in directions:
            if self.in_bounds(x+dx, y+1):
                diag_idx = self.get_index(x+dx, y+1)
                if self.grid[diag_idx] == self.colors['sky']:
                    self.grid[index], self.grid[diag_idx] = self.grid[diag_idx], self.grid[index]
                    return
        
        for dx in directions:
            if self.in_bounds(x+dx, y):
                side_idx = self.get_index(x+dx, y)
                if self.grid[side_idx] == self.colors['sky']:
                    self.grid[index], self.grid[side_idx] = self.grid[side_idx], self.grid[index]
                    return

    def handle_input(self):
        mouse_pos = pg.mouse.get_pos()
        grid_x = mouse_pos[0] // self.TILE
        grid_y = mouse_pos[1] // self.TILE
        
        if pg.mouse.get_pressed()[0] and self.in_bounds(grid_x, grid_y):
            radius = 3
            for dy in range(-radius, radius+1):
                for dx in range(-radius, radius+1):
                    if dx*dx + dy*dy <= radius*radius:
                        nx = grid_x + dx
                        ny = grid_y + dy
                        if self.in_bounds(nx, ny):
                            idx = self.get_index(nx, ny)
                            self.grid[idx] = self.colors[self.selected]
        
        if pg.mouse.get_pressed()[2] and self.in_bounds(grid_x, grid_y):
            radius = 5
            for dy in range(-radius, radius+1):
                for dx in range(-radius, radius+1):
                    if dx*dx + dy*dy <= radius*radius:
                        nx = grid_x + dx
                        ny = grid_y + dy
                        if self.in_bounds(nx, ny):
                            self.grid[self.get_index(nx, ny)] = self.colors['sky']

    def run(self):
        while True:
            self.grid_surface.fill(self.colors['black'])
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.VIDEORESIZE:
                    new_width = max((event.w // self.TILE) * self.TILE, self.TILE)
                    new_height = max((event.h // self.TILE) * self.TILE, self.TILE)
                    self.screen = pg.display.set_mode((new_width, new_height), pg.RESIZABLE)
                    
                    old_width = self.WIDTH
                    old_height = self.HEIGHT
                    
                    self.WIDTH = new_width // self.TILE
                    self.HEIGHT = new_height // self.TILE
                    
                    new_grid = [self.colors['sky'] for _ in range(self.WIDTH * self.HEIGHT)]
                    for y in range(min(old_height, self.HEIGHT)):
                        for x in range(min(old_width, self.WIDTH)):
                            old_idx = y * old_width + x
                            new_idx = y * self.WIDTH + x
                            if new_idx < len(new_grid) and old_idx < len(self.grid):
                                new_grid[new_idx] = self.grid[old_idx]
                    self.grid = new_grid
                    
                    self.grid_surface = pg.Surface((self.WIDTH*self.TILE, self.HEIGHT*self.TILE))
                    self.rects = [pg.Rect(x*self.TILE, y*self.TILE, self.TILE, self.TILE) 
                                 for y in range(self.HEIGHT) for x in range(self.WIDTH)]
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1: self.selected = 'sand'
                    elif event.key == pg.K_2: self.selected = 'water'
                    elif event.key == pg.K_3: self.selected = 'wall'
                    elif event.key == pg.K_e: self.paused = not self.paused
                    elif event.key == pg.K_q: 
                        self.grid = [self.colors['sky'] for _ in self.grid]
                    elif event.key == pg.K_ESCAPE: 
                        pg.quit()
                        return

            if not self.paused:
                for y in reversed(range(self.HEIGHT)):
                    for x in random.sample(range(self.WIDTH), self.WIDTH):
                        current_color = self.grid[self.get_index(x, y)]
                        if current_color == self.colors['sand']:
                            self.update_sand(x, y)
                        elif current_color == self.colors['water']:
                            self.update_water(x, y)

            for i, rect in enumerate(self.rects):
                pg.draw.rect(self.grid_surface, self.grid[i], rect)
            
            self.screen.blit(self.grid_surface, (0, 0))
            
            self.handle_input()
            pg.display.update()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = ParticleSim(initial_width=80, initial_height=60, tile=8, fps=60)
    game.run()
