import pygame
from settings import PLAYER_SPEED, BULLET_SIZE
from bullet import Bullet

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.x = pos[0] # начальная позиция корабля по x
        self.y = pos[1] # начальная позиция корабля по y
        # информация о корабле
        img_path = 'assets/ship/ship.png'  # Путь к изображению корабля
        self.image = pygame.image.load(img_path)  # Загрузка изображения корабля
        self.image = pygame.transform.scale(self.image, (size, size))  # Изменение размера изображения
        self.rect = self.image.get_rect(topleft=pos)  # Получение прямоугольника, описывающего положение корабля на экране
        self.mask = pygame.mask.from_surface(self.image)  # Создание маски для обработки столкновений
        self.ship_speed = PLAYER_SPEED  # Установка скорости корабля из настроек
        self.life = 3  # Установка начального количества жизней корабля
        self.player_bullets = pygame.sprite.Group()  # Создание группы для хранения пуль игрока

    def move_left(self):
        self.rect.x -= self.ship_speed # Сдвигаем корабль влево на его скорость

    def move_up(self):
        self.rect.y -= self.ship_speed # Сдвигаем корабль вверх на его скорость

    def move_right(self):
        self.rect.x += self.ship_speed # Сдвигаем корабль вправо на его скорость

    def move_bottom(self):
        self.rect.y += self.ship_speed  # Сдвигаем корабль вниз на его скорость

    def _shoot(self):
        specific_pos = (self.rect.centerx - (BULLET_SIZE // 2), self.rect.y)  # Вычисляем позицию выстрела
        self.player_bullets.add(Bullet(specific_pos, BULLET_SIZE, "player")) # Создаем и добавляем пулю

    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y)) # Обновляем положение корабля на экране