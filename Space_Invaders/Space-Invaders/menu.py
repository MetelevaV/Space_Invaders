import pygame
from settings import WIDTH, HEIGHT, SPACE, FONT_SIZE, EVENT_FONT_SIZE, ENEMY_SPEED_OPTIONS


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.score_font = pygame.font.SysFont("monospace", FONT_SIZE)  # Шрифт для отображения счета
        self.selected_speed = 0  # Выбранная скорость инопланетян по умолчанию

        # Создаем кнопку "Старт"
        self.start_button_text = self.score_font.render('MENU', True, pygame.Color("blue"))
        self.start_button_rect = self.start_button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Создаем прямоугольники для кнопок выбора скорости
        self.speed_selector_rects = []
        for i, option in enumerate(ENEMY_SPEED_OPTIONS):
            option_text = self.score_font.render(option, True, pygame.Color("blue"))
            option_rect = option_text.get_rect(midtop=(WIDTH // 2, HEIGHT // 2 + SPACE * (i + 2)))
            self.speed_selector_rects.append(option_rect)

    def draw(self):
        # Отображаем кнопку "Старт" и кнопки выбора скорости на экране
        self.screen.fill((0, 0, 0))  # Очищаем экран перед отрисовкой меню
        self.screen.blit(self.start_button_text, self.start_button_rect)
        for option_rect in self.speed_selector_rects:
            option_text = self.score_font.render(ENEMY_SPEED_OPTIONS[self.speed_selector_rects.index(option_rect)], True, pygame.Color("blue"))
            if option_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, pygame.Color("blue"), option_rect, 2)
            if self.selected_speed == ENEMY_SPEED_OPTIONS[self.speed_selector_rects.index(option_rect)]:
                pygame.draw.rect(self.screen, pygame.Color("blue"), option_rect, 2)
            self.screen.blit(option_text, option_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for option_rect in self.speed_selector_rects:
                    if option_rect.collidepoint(event.pos):
                        self.selected_speed = ENEMY_SPEED_OPTIONS[self.speed_selector_rects.index(option_rect)]
                        return "start", self.selected_speed  # Возвращаем "start" и выбранную скорость
                if self.start_button_rect.collidepoint(event.pos):  # Если нажата кнопка "Старт"
                    return "start", self.selected_speed  # Возвращаем "start" и выбранную скорость
        return None  # Возвращаем None, если не было нажатий на кнопки меню

    def update(self):
        self.draw()
        return self.handle_events()  # Обновляем и обрабатываем события меню

