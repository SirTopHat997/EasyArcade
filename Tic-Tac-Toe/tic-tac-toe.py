import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
OVERLAY_COLOR = (0, 0, 0, 180)  # Semi-transparent black
HIGHLIGHT_COLOR = (255, 255, 0)  # Yellow for highlighting winning line

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Board
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    return all(all(row) for row in board)

def check_win(player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True, [(row, 0), (row, 2)]
    # Check vertical
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True, [(0, col), (2, col)]
    # Check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True, [(0, 0), (2, 2)]
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True, [(0, 2), (2, 0)]
    return False, None

def draw_win_line(start, end):
    pygame.draw.line(screen, HIGHLIGHT_COLOR, 
                     (start[1] * SQUARE_SIZE + SQUARE_SIZE // 2, start[0] * SQUARE_SIZE + SQUARE_SIZE // 2),
                     (end[1] * SQUARE_SIZE + SQUARE_SIZE // 2, end[0] * SQUARE_SIZE + SQUARE_SIZE // 2), 
                     LINE_WIDTH)

def draw_end_screen(message, color):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(overlay, OVERLAY_COLOR, (50, HEIGHT // 4, WIDTH - 100, HEIGHT // 2), border_radius=20)
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 80)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_button(text, position, size):
    font = pygame.font.Font(None, 40)
    text_render = font.render(text, True, LINE_COLOR)
    text_rect = text_render.get_rect(center=position)
    button_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
    pygame.draw.rect(screen, CIRCLE_COLOR, button_rect)
    screen.blit(text_render, text_rect)
    return button_rect

def restart_game():
    global board
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    return 'X'

def bot_move():
    # First, check if the player has a winning move that needs to be blocked
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'X'  # Simulate player's move
                if check_win('X')[0]:
                    board[row][col] = None
                    return row, col  # Block the player's winning move
                board[row][col] = None

    # Now check for bot's winning move
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'O'
                if check_win('O')[0]:
                    board[row][col] = None
                    return row, col  # Make the winning move
                board[row][col] = None

    # If no immediate threat or win, proceed with the existing strategy
    # Try to take the center
    if board[1][1] is None:
        return 1, 1

    # Try to take the corners
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    available_corners = [corner for corner in corners if board[corner[0]][corner[1]] is None]
    if available_corners:
        return random.choice(available_corners)

    # Take any available edge
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    available_edges = [edge for edge in edges if board[edge[0]][edge[1]] is None]
    if available_edges:
        return random.choice(available_edges)

    # If all else fails, choose a random empty square
    empty_squares = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] is None]
    if empty_squares:
        return random.choice(empty_squares)

    return None

def draw_start_screen():
    screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 80)
    title = font.render("Tic Tac Toe", True, LINE_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    pvp_button = draw_button("Player vs Player", (WIDTH // 2, HEIGHT // 2), (200, 50))
    pvb_button = draw_button("Player vs Bot", (WIDTH // 2, HEIGHT * 3 // 4), (200, 50))

    return pvp_button, pvb_button

def main():
    start_screen = True
    game_mode = None
    player = 'X'
    game_over = False
    winning_line = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_screen:
                pvp_button, pvb_button = draw_start_screen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pvp_button.collidepoint(event.pos):
                        start_screen = False
                        game_mode = "PVP"
                        player = restart_game()
                    elif pvb_button.collidepoint(event.pos):
                        start_screen = False
                        game_mode = "PVB"
                        player = restart_game()
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    
                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        win, winning_line = check_win(player)
                        if win:
                            game_over = True
                        elif is_board_full():
                            game_over = True
                            winning_line = None
                        else:
                            player = 'O' if player == 'X' else 'X'
                            if game_mode == "PVB" and player == 'O':
                                bot_row, bot_col = bot_move()
                                if bot_row is not None and bot_col is not None:
                                    mark_square(bot_row, bot_col, player)
                                    win, winning_line = check_win(player)
                                    if win:
                                        game_over = True
                                    elif is_board_full():
                                        game_over = True
                                        winning_line = None
                                    else:
                                        player = 'X'
            else:
                restart_rect = draw_button("Restart", (WIDTH // 2, HEIGHT - 50), (200, 50))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        start_screen = True
                        game_over = False
                        winning_line = None

        if not start_screen:
            screen.fill(BG_COLOR)
            draw_lines()
            draw_figures()

            if game_over:
                if winning_line:
                    draw_win_line(winning_line[0], winning_line[1])
                if is_board_full() and not winning_line:
                    draw_end_screen("It's a tie!", LINE_COLOR)
                else:
                    draw_end_screen(f"Player {player} wins!", CROSS_COLOR if player == 'X' else CIRCLE_COLOR)
                draw_button("Restart", (WIDTH // 2, HEIGHT - 50), (200, 50))

        pygame.display.update()

if __name__ == "__main__":
    main()