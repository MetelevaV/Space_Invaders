import pygame
from ship import Ship
from alien import Alien
from settings import HEIGHT, WIDTH, ENEMY_SPEED, CHARACTER_SIZE, BULLET_SIZE, NAV_THICKNESS
from display import Display

class World:
    def __init__(self, screen, enemy_speed):
        self.screen = screen
        self.player = pygame.sprite.GroupSingle()
        self.aliens = pygame.sprite.Group()
        self.display = Display(self.screen)  # Создаем объект Display для отображения интерфейса
        self.game_over = False
        self.player_score = 0
        self.game_level = 1
        self.enemy_speed = enemy_speed  # Устанавливаем скорость врагов из аргумента
        self._generate_world()

    def _generate_aliens(self):
        alien_cols = (WIDTH // CHARACTER_SIZE) // 2  # Вычисляет количество столбцов пришельцев
        alien_rows = 2  # Задает количество строк пришельцев
        for y in range(alien_rows):
            for x in range(alien_cols):
                my_x = CHARACTER_SIZE * x  # Вычисляет координату x для текущего пришельца
                my_y = CHARACTER_SIZE * y  # Вычисляет координату y для текущего пришельца
                specific_pos = (my_x, my_y)  # Определяет позицию для текущего пришельца
                self.aliens.add(Alien(specific_pos, CHARACTER_SIZE, y, self.enemy_speed))  # Создает и добавляет пришельца в группу

    def _generate_world(self):
        player_x, player_y = WIDTH // 2, HEIGHT - CHARACTER_SIZE  # Вычисляет начальное положение игрока
        center_size = CHARACTER_SIZE // 2  # Определяет центральный размер игрока
        player_pos = (player_x - center_size, player_y)  # Определяет позицию игрока на экране
        self.player.add(Ship(player_pos, CHARACTER_SIZE))  # Создает игрока и добавляет его на экран
        self._generate_aliens()  # Генерирует пришельцев
    def add_additionals(self):
        nav = pygame.Rect(0, HEIGHT, WIDTH, NAV_THICKNESS)  # Создает прямоугольник для навигационной панели
        pygame.draw.rect(self.screen, pygame.Color("gray"), nav)  # Рисует навигационную панель на экране
        # Отображает текущее количество жизней, счет игрока и уровень игры
        self.display.show_life(self.player.sprite.life)
        self.display.show_score(self.player_score)
        self.display.show_level(self.game_level)

    def player_move(self, attack=False):
        keys = pygame.key.get_pressed()  # Получает состояние клавиш клавиатуры
        if keys[pygame.K_a] and not self.game_over or keys[pygame.K_LEFT] and not self.game_over:
            if self.player.sprite.rect.left > 0:
                self.player.sprite.move_left()  # Двигает игрока влево
        if keys[pygame.K_d] and not self.game_over or keys[pygame.K_RIGHT] and not self.game_over:
            if self.player.sprite.rect.right < WIDTH:
                self.player.sprite.move_right()  # Двигает игрока вправо
        if keys[pygame.K_w] and not self.game_over or keys[pygame.K_UP] and not self.game_over:
            if self.player.sprite.rect.top > 0:
                self.player.sprite.move_up()  # Двигает игрока вверх
        if keys[pygame.K_s] and not self.game_over or keys[pygame.K_DOWN] and not self.game_over:
            if self.player.sprite.rect.bottom < HEIGHT:
                self.player.sprite.move_bottom()  # Двигает игрока вниз
            # Кнопка перезапуска игры
        if keys[pygame.K_r]:
            self.game_over = False
            self.player_score = 0
            self.game_level = 1
            for alien in self.aliens.sprites():
                alien.kill()  # Удаляет всех пришельцев
            self._generate_world()  # Генерирует новое состояние игрового мира
        if attack and not self.game_over:
            self.player.sprite._shoot()  # Производит атаку игрока, если не завершена игра

    def _restart_game(self):
        self.game_over = False  # Сбрасывает флаг завершения игры
        self.player_score = 0  # Сбрасывает счет игрока
        self.game_level = 1  # Сбрасывает уровень игры
        for alien in self.aliens.sprites():
            alien.kill()  # Удаляет всех пришельцев
        self._generate_world()  # Генерирует новое начальное состояние игрового мира
    def _detect_collisions(self):
        # Проверяет столкновения пуль игрока с пришельцами
        player_attack_collision = pygame.sprite.groupcollide(self.aliens, self.player.sprite.player_bullets, True, True)
        if player_attack_collision:
            self.player_score += 10  # Увеличивает счет игрока при попадании пули в пришельца
        # Проверяет столкновения пуль пришельцев с игроком
        for alien in self.aliens.sprites():
            alien_attack_collision = pygame.sprite.groupcollide(alien.bullets, self.player, True, False)
            if alien_attack_collision:
                self.player.sprite.life -= 1  # Уменьшает количество жизней игрока при попадании пули пришельца
                break
        # Проверяет столкновения пришельцев с игроком
        alien_to_player_collision = pygame.sprite.groupcollide(self.aliens, self.player, True, False)
        if alien_to_player_collision:
            self.player.sprite.life -= 1  # Уменьшает количество жизней игрока при столкновении с пришельцем

    def _alien_movement(self): # Обнаруживает столкновения объектов игры и обрабатывает соответствующие последствия.
        move_sideward = False  # Флаг для перемещения пришельцев в сторону
        move_forward = False  # Флаг для перемещения пришельцев вниз
        for alien in self.aliens.sprites():
            # Проверяет, можно ли пришельцам двигаться в сторону или им нужно двигаться вниз
            if alien.to_direction == "right" and alien.rect.right < WIDTH or alien.to_direction == "left" and alien.rect.left > 0:
                move_sideward = True
                move_forward = False
            else:
                move_sideward = False
                move_forward = True
                alien.to_direction = "left" if alien.to_direction == "right" else "right"  # Меняет направление движения пришельцев
                break
        for alien in self.aliens.sprites():
            # Выполняет перемещение пришельцев в сторону или вниз, в зависимости от флагов
            if move_sideward and not move_forward:
                if alien.to_direction == "right":
                    alien.move_right()  # Перемещает пришельцев вправо
                if alien.to_direction == "left":
                    alien.move_left()  # Перемещает пришельцев влево
            if not move_sideward and move_forward:
                alien.move_bottom()  # Перемещает пришельцев вниз

    def _alien_shoot(self):
        for alien in self.aliens.sprites():
            # Проверяет, находится ли игрок в одном столбце с пришельцами
            if (WIDTH - alien.rect.x) // CHARACTER_SIZE == (WIDTH - self.player.sprite.rect.x) // CHARACTER_SIZE:
                alien._shoot()  # Выпускает пулю из пришельца
                break
    def _check_game_state(self):
        # Проверяет, завершилась ли игра из-за исчерпания жизней игрока
        if self.player.sprite.life <= 0:
            self.game_over = True  # Устанавливает флаг окончания игры
            self.display.game_over_message()  # Выводит сообщение об окончании игры
        for alien in self.aliens.sprites():
            # Проверяет, достигли ли пришельцы нижней границы экрана
            if alien.rect.top >= HEIGHT:
                self.game_over = True  # Устанавливает флаг окончания игры
                self.display.game_over_message()  # Выводит сообщение об окончании игры
                break
        # Проверяет, был ли завершен текущий уровень (все пришельцы уничтожены)
        if len(self.aliens) == 0 and self.player.sprite.life > 0:
            self.game_level += 1  # Увеличивает уровень игры на 1
            self._generate_aliens()  # Генерирует новых пришельцев для следующего уровня
            for alien in self.aliens.sprites():
                alien.move_speed += self.game_level - 1  # Увеличивает скорость пришельцев для следующего уровня

    def update(self):
        # Обнаруживает столкновения пуль, пришельцев и игрока и обрабатывает соответствующие последствия
        self._detect_collisions()
        # Позволяет пришельцам двигаться по экрану
        self._alien_movement()
        # Позволяет пришельцам стрелять в игрока
        self._alien_shoot()
        # Обновляет позиции и отрисовывает пули игрока
        self.player.sprite.player_bullets.update()
        self.player.sprite.player_bullets.draw(self.screen)
        # Обновляет позиции и отрисовывает пули пришельцев
        [alien.bullets.update() for alien in self.aliens.sprites()]
        [alien.bullets.draw(self.screen) for alien in self.aliens.sprites()]
        # Обновляет позицию и отрисовывает игрока
        self.player.update()
        self.player.draw(self.screen)
        # Отрисовывает пришельцев
        self.aliens.draw(self.screen)
        # Добавляет навигационную панель
        self.add_additionals()
        # Проверяет состояние игры
        self._check_game_state()
