import pygame
from settings import WIDTH, HEIGHT, SPACE, FONT_SIZE, EVENT_FONT_SIZE

pygame.font.init()

class Display:
    def __init__(self, screen):
        self.screen = screen
        self.score_font = pygame.font.SysFont("monospace", FONT_SIZE)  # Шрифт для отображения счета
        self.level_font = pygame.font.SysFont("impact", FONT_SIZE)  # Шрифт для отображения уровня
        self.event_font = pygame.font.SysFont("impact", EVENT_FONT_SIZE)  # Шрифт для отображения сообщений
        self.text_color = pygame.Color("blue")  # Цвет текста для счета и уровня
        self.event_color = pygame.Color("red")  # Цвет текста для сообщений о событиях

    def show_life(self, life): # отображение количества жизней игрока
        life_size = 30  # Размер изображения жизни
        img_path = "assets/life/life.png"  # Путь к изображению жизни
        life_image = pygame.image.load(img_path)  # Загружаем изображение жизни
        life_image = pygame.transform.scale(life_image, (life_size, life_size))  # Изменяем размер изображения
        life_x = SPACE // 2  # Начальная позиция для отображения жизней
        if life != 0:
            for life in range(life):
                self.screen.blit(life_image, (life_x, HEIGHT + (SPACE // 2)))  # Отображаем жизни на экране
                life_x += life_size

    def show_score(self, score): # Отображение текущего счета
        score_x = WIDTH // 3  # Позиция для отображения счета по горизонтали
        score = self.score_font.render(f'score: {score}', True, self.text_color)  # Создаем изображение счета
        self.screen.blit(score, (score_x, (HEIGHT + (SPACE // 2))))  # Отображаем счет на экране

    def show_level(self, level):  # Отображение текущего уровня
        level_x = WIDTH // 3  # Позиция для отображения уровня по горизонтали
        level = self.level_font.render(f'Level {level}', True, self.text_color)  # Создаем изображение уровня
        self.screen.blit(level, (level_x * 2, (HEIGHT + (SPACE // 2))))  # Отображаем уровень на экране

    def game_over_message(self): # Отображение сообщения о заверщении игры
        message = self.event_font.render('GAME OVER!!!', True, self.event_color)  # Создаем изображение сообщения
        self.screen.blit(message, ((WIDTH // 3) - (EVENT_FONT_SIZE // 2), (HEIGHT // 2) - (EVENT_FONT_SIZE // 2)))  # Отображаем сообщение на экране