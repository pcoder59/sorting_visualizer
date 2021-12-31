import pygame
import random
import math
pygame.init()

class information:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    MED_GREY = 160, 160, 160
    DARK_GREY = 192, 192, 192
    BLUE = 0, 0, 255
    BACKGROUND_COLOR = WHITE

    BARS = [
        GREY,
        MED_GREY,
        DARK_GREY
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorthms Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_value = max(lst)
        self.min_value = min(lst)

        self.pixel_width = round((self.width - self.SIDE_PAD)/len(lst))
        self.pixel_height = math.floor((self.height - self.TOP_PAD)/(self.max_value - self.min_value))
        self.start_x = self.SIDE_PAD//2

def draw(draw_information, algo_name, ascending, FPS):
    draw_information.window.fill(draw_information.BACKGROUND_COLOR)

    title = draw_information.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_information.GREEN)
    draw_information.window.blit(title, ((draw_information.width/2) - (title.get_width()/2), 5))

    controls = draw_information.FONT.render("R - RESET | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_information.BLACK)
    draw_information.window.blit(controls, ((draw_information.width/2) - (controls.get_width()/2), 45))

    speed = draw_information.FONT.render("4 - Slow | 5 - Normal | 6 - Fast", 1, draw_information.BLACK)
    draw_information.window.blit(speed, ((draw_information.width/2) - (speed.get_width()/2), 65))

    sorting = draw_information.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_information.BLACK)
    draw_information.window.blit(sorting, ((draw_information.width/2) - (sorting.get_width()/2), 85))

    if FPS == 30:
        speeding = draw_information.FONT.render("Speed - Slow", 1, draw_information.GREEN)
    elif FPS == 60:
        speeding = draw_information.FONT.render("Speed - Normal", 1, draw_information.GREEN)
    else:
        speeding = draw_information. FONT.render("Speed - Fast", 1, draw_information.GREEN)
    draw_information.window.blit(speeding, ((draw_information.width/2) - (speeding.get_width()/2), 115))

    draw_list(draw_information)
    pygame.display.update()

def changeSpeedText(draw_information, FPS):
    if FPS == 30:
        speeding = draw_information.FONT.render("Speed - Slow", 1, draw_information.GREEN)
    elif FPS == 60:
        speeding = draw_information.FONT.render("Speed - Normal", 1, draw_information.GREEN)
    else:
        speeding = draw_information. FONT.render("Speed - Fast", 1, draw_information.GREEN)
    clear_rect = (draw_information.width/2) - (speeding.get_width()/2) - 20, 115, draw_information.width, speeding.get_height()
    pygame.draw.rect(draw_information.window, draw_information.BACKGROUND_COLOR, clear_rect)
    draw_information.window.blit(speeding, ((draw_information.width/2) - (speeding.get_width()/2), 115))
    pygame.display.update()

def draw_list(draw_information, color_positions = {}, clear = False):
    lst = draw_information.lst

    if clear:
        clear_rect = draw_information.SIDE_PAD//2, draw_information.TOP_PAD, draw_information.width - draw_information.SIDE_PAD, draw_information.height - draw_information.TOP_PAD
        pygame.draw.rect(draw_information.window, draw_information.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_information.start_x + (i * draw_information.pixel_width)
        y = draw_information.height - (val - draw_information.min_value) * draw_information.pixel_height

        color = draw_information.BARS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_information.window, color, (x, y, draw_information.pixel_width, draw_information.height))

    if clear:
        pygame.display.update()

def generator(n, min_val, max_val):
    lst = []

    for _ in range(n):
        value = random.randint(min_val, max_val)
        lst.append(value)

    return lst

def bubble_sort(draw_information, ascending):
    lst = draw_information.lst
    swap = -1

    while swap != 0:
        swap = 0
        for i in range(len(lst)-1):
            if ((ascending and (lst[i] > lst[i+1])) or (not ascending and (lst[i] < lst[i+1]))):
                swap = swap + 1
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                draw_list(draw_information, {i: draw_information.GREEN, i + 1: draw_information.RED}, True)
                yield True

    return lst

def Insertion_sort(draw_information, ascending):
    lst = draw_information.lst
    for i in range(len(lst)):
        swap = lst[i]
        j = i - 1
        while j >= 0 and ((ascending and lst[j] > swap) or (not ascending and lst[j] < swap)):
            lst[j+1] = lst[j]
            draw_list(draw_information, {j: draw_information.GREEN, j + 1: draw_information.RED}, True)
            yield True
            j = j - 1
        lst[j+1] = swap

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generator(n, min_val, max_val)
    draw_information = information(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_name = "Bubble Sort"
    sorting_generator = None

    FPS = 60

    while run:
        clock.tick(FPS)

        if sorting:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_information, sorting_name, ascending, FPS)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:
                lst = generator(n, min_val, max_val)
                draw_information.set_list(lst)
            elif (event.key == pygame.K_SPACE) and not sorting:
                sorting = True
                sorting_generator = sorting_algorithm(draw_information, ascending)
            elif (event.key == pygame.K_a) and not sorting:
                ascending = True
            elif (event.key == pygame.K_d) and not sorting:
                ascending = False
            elif (event.key == pygame.K_5):
                FPS = 60
                changeSpeedText(draw_information, FPS)
            elif (event.key == pygame.K_6):
                FPS = 120
                changeSpeedText(draw_information, FPS)
            elif (event.key == pygame.K_4):
                FPS = 30
                changeSpeedText(draw_information, FPS)
            elif (event.key == pygame.K_b) and not sorting:
                sorting_algorithm = bubble_sort
                sorting_name = "Bubble Sort"
            elif (event.key == pygame.K_i) and not sorting:
                sorting_algorithm = Insertion_sort
                sorting_name = "Insertion Sort"


    pygame.quit()

if __name__ == "__main__":
    main()