import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Torres de Hanoi')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (239, 229, 51)
GREY = (170, 170, 170)


# Configuración de los discos
num_disks = 3
tower_width = 20
tower_height = 150
disc_height = 20
towers = [[], [], []]
game_over = False

# Crear discos y apilarlos en la primera torre
for i in range(num_disks):
    width = (num_disks - i) * 60
    disc = pygame.Rect(200 - width // 2, 450 - (i + 1) * disc_height, width, disc_height)
    towers[0].append(disc)

# Posiciones de las torres
tower_positions = [
    (200, 450),
    (400, 450),
    (600, 450)
]

def blit_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:                                    
        font = pygame.font.SysFont(font_name, size)     
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def menu_screen():
    global screen, num_disks, game_over
    menu_over = False
    while not menu_over:
        screen.fill(WHITE)
        blit_text(screen, 'Towers of Hanoi', (323,122), font_name='sans serif', size=90, color=GREY)
        blit_text(screen, 'Towers of Hanoi', (320,120), font_name='sans serif', size=90, color=GOLD)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30, color=BLACK)
        blit_text(screen, str(num_disks), (320, 260), font_name='sans serif', size=40, color=BLUE)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=BLACK)

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_over = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_over = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    num_disks += 1
                    if num_disks > 10:
                        num_disks = 10
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    num_disks -= 1
                    if num_disks < 3:
                        num_disks = 3
            if event.type == pygame.QUIT:
                menu_over = True
                game_over = True
        pygame.display.flip()

# Función para dibujar torres y discos
def draw():
    screen.fill(WHITE)
    # Dibujar torres
    for x, y in tower_positions:
        pygame.draw.rect(screen, BLACK, (x - tower_width // 2, y - tower_height, tower_width, tower_height))
    # Dibujar discos
    colors = [RED, GREEN, BLUE]
    for tower in towers:
        for disc in tower:
            pygame.draw.rect(screen, colors[tower.index(disc) % len(colors)], disc)
    pygame.display.flip()

# Función principal del juego
def hanoi_game():
    global game_over
    selected_disc = None
    selected_tower = None
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, tower in enumerate(towers):
                    if tower and tower[-1].collidepoint(pos):
                        selected_disc = tower[-1]
                        selected_tower = i
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_disc:
                    pos = pygame.mouse.get_pos()
                    for i, (tower_x, tower_y) in enumerate(tower_positions):
                        if abs(pos[0] - tower_x) < 50:
                            if not towers[i] or towers[i][-1].width > selected_disc.width:
                                towers[selected_tower].remove(selected_disc)
                                selected_disc.centerx = tower_x
                                selected_disc.y = 450 - (len(towers[i]) + 1) * disc_height
                                towers[i].append(selected_disc)
                            break
                    selected_disc = None

        draw()

    pygame.quit()
    sys.exit()

# Llamar a la función principal
if __name__ == '__main__':
    menu_screen()
    hanoi_game()
