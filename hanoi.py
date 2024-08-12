import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Torres de Hanoi')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (239, 229, 51)
GREY = (170, 170, 170)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)


class Disk:
    def __init__(self, color, width, height, tower_index, x, y):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.tower_index = tower_index

    def move_to(self, x, y):
        self.rect.centerx = x
        self.rect.y = y

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, screen, font_name='sans_serif', font_size=20, text_color=BLACK, button_color=GREY):
        pygame.draw.rect(screen, button_color, self.rect)
        font = pygame.font.SysFont(font_name, font_size)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Configuración de los discos
num_disks = 3
move_count = 0
tower_width = 15
tower_height = 250
disk_height = 20
towers = [[], [], []]
disk_colors = [RED, GREEN, BLUE, GOLD, GREY, CYAN, MAGENTA, ORANGE]
game_over = False
game_mode = 'PLAY'

# Posiciones de las torres
tower_positions = [
    (200, 450),
    (400, 450),
    (600, 450)
]

floating_disk_position = (screen_width // 2, 150)

menu_button_width = 100
menu_button = Button('Menu', screen_width - menu_button_width - 10, 10, menu_button_width, 40)

def build_disks():
    global towers

    # Clean towers
    towers = [[], [], []]

    # Create disks and apply them on the first tower
    for i in range(num_disks):
        width = (num_disks - i) * 30
        x = tower_positions[0][0] - width // 2
        y = tower_positions[0][1] - (i + 1) * disk_height
        disk = Disk(disk_colors[i % len(disk_colors)], width, disk_height, 0, x, y)
        towers[0].append(disk)

def blit_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:                                    
        font = pygame.font.SysFont(font_name, size)     
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def menu_screen():
    global screen, num_disks, game_over, game_mode
    menu_over = False

    while not menu_over:
        screen.fill(WHITE)
        blit_text(screen, 'Towers of Hanoi' if not game_over else 'VICTORY!', (screen_width // 2, 50), font_name='sans serif', size=90, color=GREEN)
        blit_text(screen, 'Towers of Hanoi' if not game_over else 'VICTORY!', (screen_width // 2, 45), font_name='sans serif', size=90, color=BLACK)
        blit_text(screen, 'Use arrow keys to select difficulty and game mode:', (screen_width // 2, 120), font_name='sans serif', size=30, color=BLACK)

        blit_text(screen, f'LEVEL: {num_disks}', (screen_width // 2, 225), font_name='sans serif', size=40, color=BLACK)

        blit_text(screen, '( DEMO )' if game_mode == 'DEMO' else 'DEMO', (screen_width // 2, 290), font_name='sans serif', size=50, color=BLACK)
        blit_text(screen, '( PLAY )' if game_mode == 'PLAY' else 'PLAY', (screen_width // 2, 350), font_name='sans serif', size=50, color=BLACK)

        blit_text(screen, 'Press ENTER to continue', (screen_width // 2, 500), font_name='sans_serif', size=30, color=BLACK)
        blit_text(screen, 'Or Q to exit', (screen_width // 2, 525), font_name='sans_serif', size=30, color=BLACK)

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_over = True
                    game_over = True
                elif event.key == pygame.K_RETURN:
                    menu_over = True
                    game_over = False
                    build_disks()
                elif event.key == pygame.K_RIGHT:
                    num_disks += 1
                    if num_disks > 10:
                        num_disks = 10
                elif event.key == pygame.K_LEFT:
                    num_disks -= 1
                    if num_disks < 3:
                        num_disks = 3
                elif event.key in [pygame.K_DOWN, pygame.K_UP]:
                    if game_mode == 'PLAY':
                        game_mode = 'DEMO'
                    else:
                        game_mode = 'PLAY'
                        
                
            if event.type == pygame.QUIT:
                menu_over = True
                game_over = True
        pygame.display.flip()

# Función para dibujar torres y discos
def draw(selected_disk=None):
    screen.fill(WHITE)
    draw_towers()
    draw_disks()

    if selected_disk:
        pygame.draw.rect(screen, selected_disk.color, selected_disk.rect)

    menu_button.draw(screen)

    blit_text(screen, f"Current Moves: {move_count}", (screen_width - 70, 60), font_name='sans_serif', size=20, color=BLACK)
    blit_text(screen, f"Level: {num_disks}", (screen_width - 70, 80), font_name='sans_serif', size=20, color=BLACK)

    pygame.display.flip()

def draw_towers():
    # Dibujar torres
    for x, y in tower_positions:
        pygame.draw.rect(screen, BLACK, (x - tower_width // 2, y - tower_height, tower_width, tower_height))

def draw_disks():
    for tower in towers:
        for disk in tower:
            pygame.draw.rect(screen, disk.color, disk.rect)

def check_win_condition():
    # Win condition: All disks on the right tower
    return len(towers[2]) == num_disks

# Función principal del juego
def hanoi_game():
    global game_over, move_count
    selected_disk = None
    selected_tower = None
    original_position = None
    dragging_disk = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_button.is_clicked(pos):
                    menu_screen()
                    build_disks() # Rebuilds disks after returning from the menu
                for i, tower in enumerate(towers):
                    if tower and tower[-1].rect.collidepoint(pos):
                        selected_disk = tower[-1]
                        selected_tower = i
                        original_position = (selected_disk.rect.centerx, selected_disk.rect.y)
                        selected_disk.move_to(*floating_disk_position)
                        dragging_disk = True
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_disk:
                    pos = pygame.mouse.get_pos()
                    placed = False
                    for i, (tower_x, tower_y) in enumerate(tower_positions):
                        if abs(pos[0] - tower_x) < 50:
                            if not towers[i] or towers[i][-1].rect.width > selected_disk.rect.width:
                                towers[selected_tower].remove(selected_disk)
                                selected_disk.move_to(tower_x,450 - (len(towers[i]) + 1) * disk_height ) 
                                towers[i].append(selected_disk)
                                move_count += 1
                                placed = True
                        if not placed:
                            # Move the disk back to its original position
                            selected_disk.move_to(*original_position)
                    selected_disk = None
                    dragging_disk = False

            draw(selected_disk)

            if check_win_condition():
                game_over = True
                menu_screen()

    pygame.quit()
    sys.exit()

# Llamar a la función principal
if __name__ == '__main__':
    menu_screen()
    hanoi_game()
