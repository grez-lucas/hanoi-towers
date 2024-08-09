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

# Configuración de los discos
num_discs = 3
tower_width = 20
tower_height = 150
disc_height = 20
towers = [[], [], []]

# Crear discos y apilarlos en la primera torre
for i in range(num_discs):
    width = (num_discs - i) * 60
    disc = pygame.Rect(200 - width // 2, 450 - (i + 1) * disc_height, width, disc_height)
    towers[0].append(disc)

# Posiciones de las torres
tower_positions = [
    (200, 450),
    (400, 450),
    (600, 450)
]

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
    selected_disc = None
    selected_tower = None
    running = True
    while running:
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
    hanoi_game()
