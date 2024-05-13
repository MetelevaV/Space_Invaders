import pygame, sys
from settings import WIDTH, HEIGHT, NAV_THICKNESS
from world import World
from menu import Menu

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT + NAV_THICKNESS))
pygame.display.set_caption("Space Invader")

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()
        self.paused = False  # Переменная для отслеживания состояния паузы
        self.menu = Menu(screen)  # Создаем экземпляр меню
        self.world = None  # Инициализируем переменную world

    def main(self):
        while True:
            self.screen.fill("black")  # Заливаем экран чёрным цветом
            menu_result = self.menu.update()  # Обновляем меню и получаем результат
            if menu_result is not None:
                action, selected_speed = menu_result
                if action == "start":
                    # Создаем экземпляр мира с выбранной скоростью
                    self.world = World(self.screen, selected_speed)
                    break  # Выходим из цикла меню и начинаем игру

            pygame.display.update()
            self.FPS.tick(30)

        while True:
            self.screen.fill("black")  # Заливаем экран чёрным цветом
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #обработка нажатия кнопки выхода
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #обработка нажатия клавиши пробел
                        self.world.player_move(attack=True)
                    elif event.key == pygame.K_p: # Обрабатываем нажатие клавиши "P"
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:  # Обрабатываем нажатие клавиши "R"
                        self.world._restart_game()

            if not self.paused:  # Если игра не на паузе и мир создан
                self.world.player_move()
                self.world.update()

            pygame.display.update()

            if self.paused or not self.world:  # Если игра на паузе или мир не создан, пропустить обновление FPS и перейти к следующей итерации
                continue

            self.FPS.tick(30)

if __name__ == "__main__":
    play = Main(screen)
    play.main()
