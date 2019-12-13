from util import *
import pygame

TILE_SIZE = 8
N_TILES_X = 42
N_TILES_Y = 24


class Display:

    tile_colors = {
        0: (0, 0, 0), # Empty
        1: (255, 0, 0), # Wall
        2: (0, 255, 0), # Block
        3: (0, 0, 255), # Paddle
        4: (255, 255, 0) # Ball
    }

    def __init__(self, tile_size, width, height):
        self.tile_size = tile_size
        self.width = width
        self.height = height
        self.input_buffer = []
        self.screen = pygame.display.set_mode((width * tile_size, (height + 2) * tile_size))
        self.screen_buffer = [[None for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.font = pygame.font.Font(None, 20)
        self.ball_x = 0
        self.paddle_x = 0

    def add_to_input_buffer(self, val):
        self.input_buffer.append(val)
        if len(self.input_buffer) == 3:
            self.draw()

    def draw(self):
        x, y, tile = self.input_buffer

        self.input_buffer = []
        if x == -1 and y == 0:
            self.score = tile
            self.draw_score()
            return

        if tile == 4:
            self.ball_x = x
        elif tile == 3:
            self.paddle_x = x

        self.screen_buffer[y][x] = tile
        pygame.draw.rect(self.screen, Display.tile_colors[tile], (x * self.tile_size, (y + 2) * self.tile_size, self.tile_size, self.tile_size))
        pygame.display.update()

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}", True, (0, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width * self.tile_size, 2 * self.tile_size))
        self.screen.blit(text, (0, 0))

    def buffer_count(self, tile):
        return [t for col in self.screen_buffer for t in col].count(tile)

    def joystick_cheat(self):
        if self.paddle_x < self.ball_x:
            return 1
        elif self.paddle_x > self.ball_x:
            return -1
        return 0


pygame.init()


def read_joystick_blocking():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                return 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                return 0


def read_joystick():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            return -1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            return 1
    return 0


display = Display(TILE_SIZE, N_TILES_X, N_TILES_Y)

intcode = readline("inputs/13.txt", type=int)[0]
program = list(intcode)
program[0] = 2 # Enable free-play

run_intcode_program(program, inp_func=display.joystick_cheat, outp_func=display.add_to_input_buffer, log_instructions=False)
print(f"Part 1: {display.buffer_count(2)}")
