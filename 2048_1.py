
#ПОДГОТОВКА К КОДИНГУ---------------------------------------------------
import pygame #ИМПОРТ ПАЙГЕЙМА
import random #ИМПОРТ РАНДОМА
import math #ИМПОРТ МАТЕМАТИКИ

pygame.init() #ИНИЦИАЛИЗАЦИЯ ПАЙГЕЙМА

FPS = 60 # ПЕРЕМЕННАЯ, С КОЛЛИЧЕСТВОМ КАДРОВ В СЕКУНДУ

WIDTH, HEIGHT = 800, 800 # ШИРИНА И ВЫСОТА ОКНА
ROWS = 4 # КОЛЛИЧЕСТВО РЯДОВ
COLS = 4 # КОЛЛИЧЕСТВО СТОЛБОВ

RECT_HEIGHT = HEIGHT // ROWS #ВЫСОТА ПЛИТКИ
RECT_WIDTH = WIDTH // COLS #ШИРИНА ПЛИТКИ

OUTLINE_COLOR = (187, 173, 160) # ЦВЕТ ОКАНТОВКИ
OUTLINE_THICKNESS = 10 # ШИРИНА ОКАНТОВКИ
BACKGROUND_COLOR = (205, 192, 180) # ЦВЕТ ЗАДНЕГО ФОНА
FONT_COLOR = (119, 110, 101) # ЦВЕТ ШРИФТА

FONT = pygame.font.SysFont("comicsans", 60, bold=True) #ШРИФТ
MOVE_VEL = 20 #СКОРОСТЬ ДВИЖЕНИЯ

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) #СОЗДАНИЕ ОКНА
pygame.display.set_caption("2048") #НАЗВАНИЕ ОКНА

#ОСНОВНАЯ ЧАСТЬ----------------------------------------------------------
class Tile:
    COLORS = [  #список со всеми нужными для плиток цветами
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    	(237, 197, 63),
        (237, 194, 46)
    ]

    def __init__(self, value, row, col): #ПИШЕМ ВСЕ, ЧТО ПОНАДОБИТЬСЯ ДЛЯ СОЗДАНИЯ КЛАССА------------------
        self.value = value #
        self.row = row #СТОЛБЫ
        self.col = col #СТРОКИ
        self.x = col * RECT_WIDTH #РАСПОЛОЖЕНИЕ ПЛИТКИ ПО КООРДИНАТЕ X
        self.y = row * RECT_HEIGHT #РАСПОЛОЖЕНИЕ ПЛИТКИ ПО КООРДИНАТЕ Y

    def get_color(self): #ОПРЕДЕЛЕНИЕ ЦВЕТА В ЗАВИСИМОСТИ ОТ ЧИСЛА НА ПЛИТКЕ-------------------------------
        color_index = int(math.log2(self.value)) - 1 # с помощью формулы вычисляешь какой цвет нужен в зависимости от числа
        color = self.COLORS[color_index] #сохранение цвета в переменную
        return color #возвращение цвета

    def draw(self, window): # ОТРИСОВКА ПЛИТКИ-------------------------------------------------------------
        color = self.get_color() #присвоение цвета с помощью дефки выше
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT)) #отрисовка квадрата

        text = FONT.render(str(self.value), 1, FONT_COLOR) #из числа делаем картинку с текстом
        
        # |число прикрепляется к середине плитки
        # |
        # V
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False): #ОПРЕДЕЛЯЕМ ПОЗИЦИЮ
        if ceil: #проверка занята ли клетка
            self.row = math.ceil(self.y / RECT_HEIGHT) #
            self.col = math.ceil(self.x / RECT_WIDTH) #
        else:
            self.row = math.floor(self.y / RECT_HEIGHT) #
            self.col = math.floor(self.x / RECT_WIDTH) #

    def move(self, delta): # ПЕРЕДВИЖЕНИЕ
        self.x += delta[0] #передвежение по х
        self.y += delta[1] #передвижение по y


def draw_grid(window): # СОЗДАЕМ ОКАНТОВКУ
    for row in range(1, ROWS): # повторить 4 раза
        y = row * RECT_HEIGHT #номер строки умножить на ее высоту
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS) # отрисовка линии

    for col in range(1, COLS): # повторить 4 раза
        x = col * RECT_WIDTH #номер столюа умножить на ее ширину
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS) # отрисовка линии

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS) #отрисовка окантовки


def draw(window, tiles): # ОТРИСОВКА БГ И СЕТКИ
    window.fill(BACKGROUND_COLOR) #заливка одним цветом заднего фона

    for tile in tiles.values(): # для всех плиток в списке
        tile.draw(window) #отрисовывать плитку

    draw_grid(window) #рисовать окантовку

    pygame.display.update() #обновление экрана


def get_random_pos(tiles): #СОЗДАНИЕ РАНДОМНОЙ ПОЗИЦИИ ДЛЯ ПЛИТКИ
    row = None #строки = ничему
    col = None #столбы = ничему
    while True: # бесконечный цикл
        row = random.randrange(0, ROWS) #рандом положение строки
        col = random.randrange(0, COLS) #рандом положение столба

        if f"{row}{col}" not in tiles: #если занята
            break #прекратить

    return row, col #вернуть рандом положение для плитки


def move_tiles(window, tiles, clock, direction): #ДВИЖЕНИЕ ПЛИТОК
    updated = True # переменная
    blocks = set() # еще одна
 
    if direction == "left":  # Влево
        sort_func = lambda x: x.col  # Сортируем плитки слева направо
        reverse = False  # Не переворачиваем порядок
        delta = (-MOVE_VEL, 0)  # Двигаем по X влево
        boundary_check = lambda tile: tile.col == 0  # Проверяем, дошли ли до края
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")  # Получаем соседнюю плитку слева
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL  # Можно ли объединить плитки
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL  # Можно ли подвинуть без столкновения
        )
        ceil = True  # Флаг, скорее всего, для прилипания к краю
    elif direction == "right":  # Вправо
        sort_func = lambda x: x.col  # Сортируем плитки по колонке
        reverse = True  # Переворачиваем порядок
        delta = (MOVE_VEL, 0)  # Двигаем по X вправо
        boundary_check = lambda tile: tile.col == COLS - 1  # Проверяем, дошли ли до края
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")  # Получаем соседнюю плитку справа
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL  # Можно ли объединить плитки
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x # Можно ли подвинуть без столкновения
        )
        ceil = False  # Не ограничиваем движение "сверху", т.к. двигаемся по горизонтали

    elif direction == "up":  # ВВЕРХ
        sort_func = lambda x: x.row  # Сортируем по строке (сверху вниз)
        reverse = False  # Не переворачиваем порядок
        delta = (0, -MOVE_VEL)  # Двигаем по Y вверх
        boundary_check = lambda tile: tile.row == 0  # Проверяем, у верхней границы ли плитка
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")  # Получем соседнюю плитку сверху
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL  # Можно ли объединить плитки
        move_check = (  
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL # Можно ли подвинуть без столкновения
        )
        ceil = True  # Ограничиваем движение сверху
    elif direction == "down":  # ВНИЗ
        sort_func = lambda x: x.row  # Сортируем по строке (сверху вниз)
        reverse = True  # Переворачиваем порядок
        delta = (0, MOVE_VEL)  # Двигаем по Y вниз
        boundary_check = lambda tile: tile.row == ROWS - 1  # Проверяем, у нижней границы ли плитка
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")  # Получаем соседнюю плитку снизу
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL  # Можно ли объединить плитки
        move_check = (  
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y # Можно ли подвинуть без столкновения
        ) 
        ceil = False  # Сверху не ограничиваем
    while updated: #ПЕРЕРИСОВКА ВСЕГО НА ЭКРАНЕ ПРИ ДВИЖЕНИИ
        clock.tick(FPS) #ФПС Чтобы с картинкой вбыло все ок
        updated = False # переменная
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse) #сохраняем отсортированые плитки

        for i, tile in enumerate(sorted_tiles): # для всех плиток
            if boundary_check(tile): # Если у границы — пропускаем
                continue #

            next_tile = get_next_tile(tile) # Получаем соседнюю плитку
            if not next_tile: # Если соседа нет
                tile.move(delta) #  Просто двигаем
            elif (
                tile.value == next_tile.value # Если значения равны
                and tile not in blocks   # И обе не участвовали в слиянии
                and next_tile not in blocks 
            ):
                if merge_check(tile, next_tile):  # Есть пространство между ними — подвинем
                    tile.move(delta) 
                else: #Иначе объединяем
                    next_tile.value *= 2  # Удваиваем значение
                    sorted_tiles.pop(i)  # Убираем текущую плитку
                    blocks.add(next_tile)  # Помечаем как слитую
            elif move_check(tile, next_tile): # Можно подвинуть без объединения
                tile.move(delta)
            else: # Иначе
                continue  # 
            tile.set_pos(ceil) # Обновляем позицию плитки
            updated = True# Что-то сдвинулось — запускаем цикл ещё раз
 
        update_tiles(window, tiles, sorted_tiles) # Обновляем отображение плиток

    return end_move(tiles) # Проверяем, конец ли игры


def end_move(tiles): #ПРОИГРЫШ, ЕСЛИ ВСЕ КЛЕТКИ ЗАПОЛНЕНЫ
    if len(tiles) == 16: # Все клетки заняты?
        return "lost" # Проигрыш

    row, col = get_random_pos(tiles) # Ищем случайную свободную позицию
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col) # Создаём новую плитку
    return "continue" # Игра продолжается


def update_tiles(window, tiles, sorted_tiles): #ОБНОВЛЕНИЕ ПЛИТОК
    tiles.clear() # Очищаем старые плитки
    for tile in sorted_tiles: # для всех плиток в сортированых плитках
        tiles[f"{tile.row}{tile.col}"] = tile #Перезаписываем заново

    draw(window, tiles) # Рисуем всё на экране


def generate_tiles(): #СОЗДАНИЕ ПЛИТКИ
    tiles = {} # Словарь для плиток
    for _ in range(2): # Создаём две стартовые
        row, col = get_random_pos(tiles) #рандом позиция
        tiles[f"{row}{col}"] = Tile(1024, row, col) #создание плитки

    return tiles # Возвращаем начальные плитки


def main(window): #СЧИТАЙ ЧТО ИГРОВОЙ ЦИКЛ, НО НАПИСАН ФУНКЦИЕЙ
    clock = pygame.time.Clock() # Часы для контроля времени
    run = True # Переменная для запуска цикла

    tiles = generate_tiles() # Стартовые плитки

    while run:#  Пока игра не завершена
        clock.tick(FPS) # Фиксированный FPS

        for event in pygame.event.get(): # Все эвенты проверяются
            if event.type == pygame.QUIT: # Закрыть окно
                run = False #
                break #

            if event.type == pygame.KEYDOWN: # Нажатие клавиши
                if event.key == pygame.K_LEFT:# Нажата кнопка влево
                    move_tiles(window, tiles, clock, "left")# Плитки двигаются влево
                if event.key == pygame.K_RIGHT:# Нажата кнопка вправо
                    move_tiles(window, tiles, clock, "right") # Плитки двигаются вправо
                if event.key == pygame.K_UP:# Нажата кнопка вверх
                    move_tiles(window, tiles, clock, "up")# Плитки двигаются вверх
                if event.key == pygame.K_DOWN: # Нажата кнопка вниз
                    move_tiles(window, tiles, clock, "down")# Плитки двигаются вниз

        draw(window, tiles)# Рисуем текущие плитки

    pygame.quit()# Выход из игры


if __name__ == "__main__": #ПРОДОЛЖЕНИЕ ИГРОВОГО ЦИКЛА
    main(WINDOW)# Запуск игры
