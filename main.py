import pygame
pygame.init()

#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
golden_rod = (218, 165, 32)
#Constants
display_width = 1200
display_height = 800
display_surface = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("GO")
clock = pygame.time.Clock()
display_surface.fill(golden_rod)
board_width = 19
board_height = 19
game_board = [["" for height in range(board_width)] for width in range(board_height)]
x_first = 50
y_fisrt = 50
square_size = 30


def reverse_token(token):
    if token == "W":
        return "B"
    elif token == "B":
        return "W"

def next_to_enemy(x_cord, y_cord, token):
    enemies = []
    if (x_cord-1)>=0 and game_board[x_cord -1][y_cord] == reverse_token(token):
        enemies.append((x_cord - 1, y_cord))
    if (x_cord+1)<board_width and game_board[x_cord + 1][y_cord] == reverse_token(token):
        enemies.append((x_cord + 1,y_cord))
    if (y_cord-1)>=0 and game_board[x_cord][y_cord - 1] == reverse_token(token):
        enemies.append((x_cord, y_cord-1))
    if (y_cord+1)<board_height and game_board[x_cord][y_cord + 1] == reverse_token(token):
        enemies.append((x_cord, y_cord+1))
    return enemies

def count_liberty(x_cord, y_cord, previous, prev_count,token):
    previous.add((x_cord,y_cord))
    count = prev_count
    if (x_cord-1)>=0 and (x_cord-1, y_cord) not in previous:
        if game_board[x_cord -1][y_cord] == "":
            count+=1
        elif game_board[x_cord-1][y_cord] == token:
            count +=count_liberty(x_cord-1,y_cord,previous,count,token)[0]
    if (x_cord+1)<board_width and (x_cord+1, y_cord) not in previous:
        if game_board[x_cord +1][y_cord] == "":
            count+=1
        elif game_board[x_cord+1][y_cord] == token:
            count +=count_liberty(x_cord+1,y_cord,previous,count,token)[0]
    if (y_cord-1)>=0 and (x_cord,y_cord-1) not in previous:
        if game_board[x_cord][y_cord - 1] == "":
            count += 1
        elif game_board[x_cord][y_cord-1] == token:
            count += count_liberty(x_cord,y_cord-1,previous,count,token)[0]
    if (y_cord+1)<board_height and (x_cord,y_cord + 1) not in previous:
        if game_board[x_cord][y_cord + 1] == "":
            count += 1
        elif game_board[x_cord][y_cord + 1] == token:
            count += count_liberty(x_cord, y_cord+1 ,previous, count, token)[0]
    return count, previous

def is_atari(x_cord, y_cord, token):
    for element in next_to_enemy(x_cord,y_cord,token):
        liberties, points = count_liberty(element[0],element[1],set(),0,reverse_token(token))
        if liberties == 0:
            for point in points:
                game_board[point[0]][point[1]]=""
    
def place_token (left, top, token):
    if token == "W":
        color = white
    else:
        color = black
    pygame.draw.circle(display_surface, color, (left + int(square_size/2), top + int(square_size/2)), int(square_size/2))

def draw_board(color1,color2):
    for boardX in range(board_height):
        for boardY in range(board_width):
            if boardX % 2 == 0:
                if boardY % 2 == 0:
                    pygame.draw.rect(display_surface, color1, (x_first+square_size * boardX, y_fisrt + square_size * boardY, square_size, square_size))
                else:
                    pygame.draw.rect(display_surface, color2, (x_first+square_size * boardX, y_fisrt + square_size * boardY, square_size, square_size))
            else:
                if boardY%2 == 0:
                    pygame.draw.rect(display_surface, color2, (x_first+square_size*boardX, y_fisrt+square_size*boardY, square_size, square_size))
                else:
                    pygame.draw.rect(display_surface, color1, (x_first+square_size*boardX, y_fisrt+square_size*boardY, square_size, square_size))
            if game_board[boardX][boardY] != "":
                place_token(x_first+square_size*boardX, y_fisrt+square_size*boardY, game_board[boardX][boardY])

def get_pixels(box_x,box_y):
    top = y_fisrt+box_y*square_size
    left = x_first+box_x*square_size
    return left, top

def get_square(x_cord, y_cord):
    for box_x in range(board_width):
        for box_y in range(board_height):
            left, top = get_pixels(box_x, box_y)
            box_rect = pygame.Rect(left, top, square_size, square_size)
            if box_rect.collidepoint(x_cord,y_cord):
                return box_x, box_y
    return -1, -1

crashed = False

mouseX = 0
mouseY = 0
turn = 1
previous_move = []

while not crashed:
    if turn % 2 == 1:
        token = "B"
    else:
        token = "W"
    draw_board(green, red)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            x, y = get_square(mouseX, mouseY)
            if x >= 0 and y >= 0 and game_board[x][y] == "":
                game_board[x][y] = token
                is_atari(x,y,token)
                if count_liberty(x,y,set(),0,token)[0] != 0:
                    previous_move.append((x,y))
                    turn += 1
                else:
                    game_board[x][y] = ""
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                if len(previous_move)>0:
                    x, y = previous_move.pop()
                    game_board[x][y] = ""
                    turn -= 1
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
