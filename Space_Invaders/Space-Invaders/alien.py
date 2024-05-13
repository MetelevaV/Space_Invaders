import pygame
from settings import BULLET_SIZE
from bullet import Bullet
from menu import Menu

class Alien(pygame.sprite.Sprite):
    def __init__(self, pos, size, row_num, enemy_speed):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.speed = enemy_speed  # Устанавливаем скорость движения пришельца

        # Установка скорости движения пришельца
        if self.speed == 'Slow':
            self.move_speed = 1
        elif self.speed == "Medium":
            self.move_speed = 5
        else:
            self.move_speed = 10

        # информация о пришельцах
        img_path = f'assets/aliens/{row_num}.png'  # Путь к изображению пришельца
        self.image = pygame.image.load(img_path)  # Загрузка изображения пришельца
        self.image = pygame.transform.scale(self.image, (size, size))  # Изменение размера изображения
        self.rect = self.image.get_rect(topleft=pos)  # Получение прямоугольника, описывающего положение пришельца на экране
        self.mask = pygame.mask.from_surface(self.image)  # Создание маски для обработки столкновений
        self.to_direction = "right"  # Начальное направление движения
        self.bullets = pygame.sprite.GroupSingle()  # Создание группы для хранения пуль пришельца

    def move_left(self):
        self.rect.x -= self.move_speed  # Сдвигаем пришельца влево на его скорость

    def move_right(self):
        self.rect.x += self.move_speed # Сдвигаем пришельца вправо на его скорость

    def move_bottom(self):
        self.rect.y += self.move_speed # Сдвигаем пришельца вниз на его скорость

    def _shoot(self):
        specific_pos = (self.rect.centerx - (BULLET_SIZE // 2), self.rect.centery) # Вычисляем позицию выстрела
        self.bullets.add(Bullet(specific_pos, BULLET_SIZE, "enemy")) # Создаем и добавляем пулю

    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y)) # Обновляем положение пришельца на экране