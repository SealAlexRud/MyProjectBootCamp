from random import randint

VERTICAL = ('0', '1', '2')  #МАССИВ ЗНАЧЕНИЙ ПО ВЕРТИКАЛИ


# Функция назначения роли для пользователя
def role():
  choice = input('Кем будешь играть?(х, 0): ')
  while choice not in ('x', '0'):
    print('Такого нет. Выбери еще раз')
    choice = input('Кем будешь играть?(х, 0): ')
  return choice


# Функция для печати горизонтальных полей
def horizontal(field):
  print(' ', '0', '1', '2')
  for y, v in enumerate(VERTICAL):
    # enumerate счетчик+значение
    print(v, ' '.join(field[y]))
    # .join() объединение, присоединение


# функция хода игрока
def user_step(field):
  u_x, u_y = 0, 0
  while True:
    coord_x = input('Введи координату x: ')
    coord_y = input('Введи координату y: ')
    y = coord_y
    x = coord_x
    if int(x) not in (0, 1, 2) or y not in VERTICAL:
      print('Координаты вне поля(допустимые символы 0, 1, 2 )')
      continue
      # continue дает возможность пропустить часть цикла
    u_x, u_y = int(x), VERTICAL.index(y)
    if field[u_y][u_x] == ' ':
      break  #цикл насильно прерывается и переходит к 37стр
    else:
      print('Клетка уже занята')
  return u_x, u_y


# Функция роли компьютера
def role_comp(step):
  return '0' if step == 'x' else 'x'


# Функция окончания игры
def end_game(step, field):
  comp_step = role_comp(step)
  # проверка строк
  for y in range(3):
    if comp_step not in field[y] and ' ' not in field[y]:
      return True

  # проверка колонок
  for x in range(3):
    column = [field[0][x], field[1][x], field[2][x]]
    if comp_step not in column and ' ' not in column:
      return True

  # проверка диагоналей
  diagonal = [field[0][0], field[1][1], field[2][2]]
  if comp_step not in diagonal and ' ' not in diagonal:
    return True
  diagonal = [field[0][2], field[1][1], field[2][0]]
  if comp_step not in diagonal and ' ' not in diagonal:
    return True
  return False


# функция определение хода компьютера
def opponent_step(field):
  check = computer
  for i in range(2):
    # проверка строк
    for y in range(3):
      if field[y].count(check) == 2 and ' ' in field[y]:
        return y, field.index(' ')
    # проверка колонн
    for x in range(3):
      column = [field[0][x], field[1][x], field[2][x]]
      if column.count(check) == 2 and ' ' in column:
        return column.index(' '), x
    # проверка диагоналей
    diagonal = [field[0][0], field[1][1], field[2][2]]
    if diagonal.count(check) == 2 and ' ' in diagonal:
      return diagonal.index(' '), diagonal.index(' ')

    diagonal = [field[0][2], field[1][1], field[2][0]]
    if diagonal.count(check) == 2 and ' ' in diagonal:
      if diagonal.index(' ') == 0:
        return 0, 2
      if diagonal.index(' ') == 1:
        return 1, 1
      if diagonal.index(' ') == 2:
        return 2, 0

    check = choice
    angles = [field[0][0], field[2][0], field[0][2], field[2][2]]
    if field[1][1] == choice and ' ' in angles:
      pair_values = [(0, 0), (2, 0), (0, 2), (2, 2)]
      return pair_values[randint(0, angles.count(' ') - 1)]

    x, y = randint(0, 2), randint(0, 2)
    while field[y][x] != ' ':
      x, y = randint(0, 2), randint(0, 2)
    return x, y


# функция проверки остаись ли пустые клетки(ничья)
def game_field(field):
  count = 0
  for y in range(3):
    if ' ' in field[y]:
      count += 1
  print("Count: " + str(count))
  return count == 0


field = [[' ' for x in range(3)] for y in range(3)]
choice = role()
computer = role_comp(choice)

while True:
  horizontal(field)
  x, y = user_step(field)
  field[y][x] = choice
  if end_game(choice, field):
    print('ПОБЕДА!')
    break

  if game_field(field):
    print('НИЧЬЯ!')
    break

  y, x = opponent_step(field)
  field[y][x] = computer
  if end_game(computer, field):
    print('ТЫ ПРОИГРАЛ!')
    break
