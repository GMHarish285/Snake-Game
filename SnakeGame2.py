import pygame, sys, random
from pygame.math import Vector2
# vectors are (x,y) coordinates(kinda like a list). we can access the 1st and 2nd elements in a vector by using .x and .y
# to move to right, we need to add +1 to .x, in a vector we can do this by (x,y) += (1,0) --> x+1, y+0
# we can actually use list for this entire program. but vectors are simple and easily readable

# GRID SYSTEM - here we aren't really creating a grid. we are just making each object move by increments of cell_size

pygame.mixer.pre_init(44100, -16, 2, 512)  # to reduce delay in playing sound
pygame.init()


class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):  # usually have a separate method to draw things on the screen
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)  # creating a rect for fruit
        screen.blit(apple_surf, fruit_rect)  # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number-1)  # creating x&y pos of fruit
        self.y = random.randint(0, cell_number-1)  # -1 cuz we don't want it to be exactly in the corners
        self.pos = Vector2(self.x, self.y)  # placing the x&y inside a vector


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # this stores all the vectors that constitutes the body of the snake
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load("img_head_up.png")
        self.head_down = pygame.image.load("img_head_down.png")
        self.head_left = pygame.image.load("img_head_left.png")
        self.head_right = pygame.image.load("img_head_right.png")

        self.tail_up = pygame.image.load("img_tail_up.png")
        self.tail_down = pygame.image.load("img_tail_down.png")
        self.tail_left = pygame.image.load("img_tail_left.png")
        self.tail_right = pygame.image.load("img_tail_right.png")

        self.body_vertical = pygame.image.load("img_body_vertical.png")
        self.body_horizontal = pygame.image.load("img_body_horizontal.png")

        self.body_tr = pygame.image.load("img_body_tr.png")
        self.body_tl = pygame.image.load("img_body_tl.png")
        self.body_br = pygame.image.load("img_body_br.png")
        self.body_bl = pygame.image.load("img_body_bl.png")

        self.sound_eat = pygame.mixer.Sound("Sound_crunch.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):  # enumerate returns both index and the element
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

        # rectangle snake:
        """for block in self.body:  # loop through the list of vectors of the snake body
            x_pos = block.x*cell_size
            y_pos = block.y*cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)  # create rect and draw it
            pygame.draw.rect(screen, (183, 111, 122), block_rect)"""

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]  # subtracting the head and first body cell vectors
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]  # subtracting last before block - last block
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):  self.tail = self.tail_down

    # moving the snake - each block is moved to the pos of the block that used to be there. the last block is deleted
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]  # copying the entire list
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]  # copying the entire list of vectors except last element
            body_copy.insert(0, body_copy[0]+self.direction)  # inserting a vector(which is the first element in the copy and added by 1(which is the next no.) at the start of the new list
            self.body = body_copy  # now the new list we created is becoming the real body

    def add_block(self):
        self.new_block = True

    def play_sound_eat(self):
        self.sound_eat.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # we are resetting the snake back to its starting position and direction(we don't wanna update the score cuz it depends of len of snake)
        self.direction = Vector2(0, 0)


class Main:  # *organising the game*; this is also convenient cuz we have fruit and snake in the same class
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:  # checking if the fruit and head of snake collide
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound_eat()
        for block in self.snake.body[1:]:  # we are checking if the fruit gets positioned on the body of the snake, if so it will get repositioned
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):  # check if snake is outside the screen or if the snake hits itself
        if (not 0 <= self.snake.body[0].x < cell_number) or (not 0 <= self.snake.body[0].y < cell_number):
            self.game_over()
        for block in self.snake.body[1:]:  # looping through all the elements in the body except head
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, green_dark, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, green_dark, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surf = game_font.render(score_text, True, black)
        score_rect = score_surf.get_rect(center=(cell_size*cell_number-20, 20))
        screen.blit(score_surf, score_rect)


cell_size = 40  # side of each cell(square)
cell_number = 16  # no. of cells in a row&column
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
pygame.display.set_caption("Snake Game")
icon = pygame.image.load("snake_icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

apple_surf = pygame.image.load("img_apple.png").convert_alpha()
game_font = pygame.font.Font("freesansbold.ttf", 25)

# colours
green_light = (175, 215, 70)
green_dark = (167, 209, 61)
black = (0, 0, 0)

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)  # we are setting the screen_update to be triggered every 150ms

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:  # every 150ms, the snake moves
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)

    screen.fill(green_light)
    main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)
