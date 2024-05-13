import pygame
from settings import BULLET_SPEED, HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, size, side):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        # информация о пуле
        img_path = f'assets/bullet/{side}-bullet.png'  # Путь к изображению пули в зависимости от стороны
        self.image = pygame.image.load(img_path)  # Загрузка изображения пули
        self.image = pygame.transform.scale(self.image, (size, size))  # Изменение размера изображения
        self.rect = self.image.get_rect(topleft=pos)  # Получение прямоугольника, описывающего положение пули на экране
        self.mask = pygame.mask.from_surface(self.image)  # Создание маски для обработки столкновений
        # Установка скорости движения пули в зависимости от стороны
        if side == "enemy":
            self.move_speed = BULLET_SPEED  # Если пуля противника, движется вниз
        elif side == "player":
            self.move_speed = (-BULLET_SPEED)  # Если пуля игрока, движется вверх

    def _move_bullet(self):
        self.rect.y += self.move_speed  # Сдвигаем пулю вверх или вниз в зависимости от стороны

    def update(self):
        self._move_bullet() # Обновляем прямоугольник пули
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y)) # Обновляем прямоугольник пули
        # Удаляем пулю, если она выходит за границы экрана
        if self.rect.bottom <= 0 or self.rect.top >= HEIGHT:
            self.kill()