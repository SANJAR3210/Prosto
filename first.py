import pygame


class Create_Ball():
    def __init__(self):
        running = True
        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.circle(screen, (255, 255, 255), player_pos, 10)
                    peremennaya = True
                if event.type == pygame.MOUSEBUTTONUP and peremennaya:
                    pygame.display.flip()
                    while True:
                        while player_pos[0] != 0 or player_pos[1] != 0:
                            player_pos[0] += 1
                            player_pos[1] += 1
                        while player_pos[0] != 800 or player_pos[1] != 800:
                            player_pos[0] -= 1
                            player_pos[1] -= 1
                pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    peremennaya = False
    pygame.display.set_caption('Жёлтый круг')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    fps = 100  # количество кадров в секунду
    clock = pygame.time.Clock()
    Create_Ball()
    pygame.display.flip()
