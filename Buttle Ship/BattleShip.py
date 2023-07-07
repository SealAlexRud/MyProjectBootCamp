from random import randint


class BoardException(Exception):  #базовый класс для исключений
  pass


class BoardOutException(
    BoardException):  #исключение, когда координаты выходят за пределы доски

  def __str__(self):
    return "Эти координаты вне доски"


class BoardUsedException(BoardException):  #когда клетка уже использована

  def __str__(self):
    return "Вы уже стрелялил в эту клетку"


class BoardWrongShipException(BoardException
                              ):  #когда размещение корабля некорректно
  pass


class Dot:  #для точки на доске

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):  #переопределять оператор сравнения для точек
    # __eq__ для опредения поведения оператора равенства для объектов класса
    return self.x == other.x and self.y == other.y

  def __str__(self):  #переопределяем метод для вывода точки в виде строки
    return f"({self.x}, {self.y})"


class Ship:  #для корабля

  def __init__(self, bow, l, o):  #с начальной точкой, длиной и ориентацией
    self.bow = bow
    self.l = l
    self.o = o
    self.lives = l

  @property
  #@ функций декораторов. Декораторы -функция, которая позволяет обернуть другую функцию для расширения ее функциональности без непосредственного изменения ее кода
  # @property используем для определения методов класса, которые дейтсвуют как атрибуты
  def dots(self):  #для получения всех точек корабля
    ship_dots = []
    for i in range(self.l):
      cur_x = self.bow.x
      cur_y = self.bow.y
      if self.o == 0:
        cur_x += i
      elif self.o == 1:
        cur_y += i
      ship_dots.append(Dot(cur_x,
                           cur_y))  #append добавляет элемент в конец списка
    return ship_dots

  def shooten(self, shot):  #для проверки был ли корабль подбит по данной точке
    return shot in self.dots


class Board:  #для доски

  def __init__(
      self,
      hid=False,
      size=6
  ):  #инициализируем доску с опциональным скрытием кораблей и размеров
    self.size = size
    self.hid = hid
    self.count = 0  #счетчик
    self.field = [["O"] * size for _ in range(size)
                  ]  #создаем поле доски с заданным параметром
    self.busy = []  #список занятых клеток
    self.ships = []  #список кораблей

  def add_ship(self, ship):  #для добавления корабля на доску
    for d in ship.dots:
      if self.out(
          d
      ) or d in self.busy:  #проверяем выходит ли корабль за пределы доски или пересекается с другими кораблями
        raise BoardWrongShipException(
        )  #raise позволяет принудительно вызвать исключение в любом месте кода

    for d in ship.dots:  #если корабль размещен корректно, добавляем его на доску и помечаем занятые клетки
      self.field[d.x][d.y] = "🞒"
      self.busy.append(d)

    self.ships.append(ship)
    self.contour(ship)  # помечаем контур корабля на доске

  def contour(self, ship, verb=False):#для пометки контура корабля на доске
    near = [(-1, -1), (-1,0),(-1,1),(0,-1),(0, 0), (0,1), (1,-1), (1,0), (1,1)]#список координат соседних ячеек вокруг заданной
    for d in ship.dots:
      for dx, dy in near:
        cur = Dot(dx+dx, dy+dy)#координаты соседних ячеек
        if not(self.out(cur)) and cur not in self.busy:
          if verb:
            self.field[cur.x][cur.y] = "."
          self.busy.append(cur)
        
        
       

  def __str__(self):  #для вывода доски в виде строки
    res = ""
    res += " |1|2|3|4|5|6|"
    for i, row in enumerate(self.field):
      res += f"\n{i+1}|" + "|".join(row) + "|"

    if self.hid:  #если скрытие кораблей включено, заменяем символы кораблей на символы пустых клеток
      res = res.replace("🞒", "O")
    return res

  def out(self, d):  #для проверки выходит ли точка за пределы доски
    return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

  def shot(self, d):  #метод для выстрела по заданной точке на доске
    if self.out(d):
      raise BoardOutException()
    if d in self.busy:
      raise BoardUsedException()

    self.busy.append(d)  #добавляем точку в список использованных

    for ship in self.ships:  #проверяем попал ли выстрел в корабль
      if d in ship.dots:
        ship.lives -= 1
        self.field[d.x][d.y] = "X"

        if ship.lives == 0:  # если корабль полностью подбит
          self.count += 1
          self.contour(ship, verb=True)
          print("Корабль уничтожен")
          return 1

        else:
          print("Корабль ранен")
          return 0

      self.field[d.x][d.y] = "."
      print("Мимо!")
      return -1

  def begin(self):  #метод для начала новой игры
    self.busy = []


# класс игрока
class Player:

  def __init__(self, board,
               enemy):  #инициализируем игрока с его доской и доской противника
    self.board = board
    self.enemy = enemy

  def ask(self, flag=False):  # для получения координат выстрела от игрока
    raise NotImplementedError()  #будет ошибка если метод будет непереопределен

  def move(self):  #для осуществления хода игрока
    flag = False
    while True:
      try:
        target = self.ask(flag)  #получаем координаты выстрела от игрока
        repeat = self.enemy.shot(
          target)  #осуществляем выстрел по заданной точке на доске противника
        if repeat == 0:  #Если выстрел повторяется, просим игрока повторить ход
          flag = True
          continue

        elif repeat == 1 and self.__class__.__name__ == 'AI':  #если корабль противника полностью подбит, сбрасываем цель AI
          self.target = None

        return repeat
      except BoardException as e:  #обрабатываем возможные исключения
        print(e)


class AI(Player):  #класс компьютерного игрока
  target = None

  def ask(self, flag=False):
    while True:
      if flag or self.target is not None:
        newD = Dot(
          self.enemy.busy[-1].x, self.enemy.busy[-1].y
        )  #новая точка которая будет равна предыдущей точке выстрела
        x = self.enemy.busy[-1].x
        y = self.enemy.busy[-1].y

      if flag:
        self.target = self.enemy.busy[-1]

      if self.target is not None:
        newD = self.target
        x = newD.x
        y = newD.y

      while True:
        num = randint(1, 4)
        if num == 1:
          newD = Dot(x - 1, y)
        elif num == 2:
          newD = Dot(x, y - 1)
        elif num == 3:
          newD = Dot(x + 1, y)
        elif num == 4:
          newD = Dot(x, y + 1)
        if newD in self.enemy.busy or newD.x < 0 or newD.y < 0 or newD.x > (
            self.enemy.size - 1) or (newD.y > self.enemy.size - 1):
          continue
        print(f"Ход компьютера: {newD.x+1} {newD.y+1}")
        return newD


class User(Player):  #класс игрока

  def ask(self, flag=False):
    while True:
      #запрашиваем координаты выстрела для игрока
      coords = input("Ваш ход: ").split()

      if len(coords) != 2:
        print("Введите 2 координаты!")
        continue

      x, y = coords

      if not (x.isdigit()) or not (y.isdigit()):
        #isdigit проверяет не тип данных, а цифра это или нет
        print("Введите числа!")
        continue

      x, y = int(x), int(y)

      return Dot(x - 1, y - 1)


class Game:

  def __init__(self, size=6):
    self.size = size
    pl = self.random_board()
    co = self.random_board()
    co.hid = True
    self.ai = AI(co, pl)
    self.us = User(pl, co)

  def random_board(self):
    # создает случайную доску с кораблями.
    board = None
    while board is None:
      board = self.random_place()
    return board

  def random_place(self):
    #генерирует случайное размещение кораблей на доске
    len = [3, 2, 2, 1, 1, 1, 1]
    board = Board(size=self.size)
    attempts = 0
    for l in len:
      while True:
        attempts += 1
        if attempts > 2000:
          return None
        ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l,
                    randint(0, 1))
        try:
          board.add_ship(ship)
          break
        except BoardWrongShipException:
          pass
    board.begin()
    return board

  def greet(self):
    print(" формат ввода: x y ")
    print(" x - номер строки ")
    print(" y - номер столбца ")

  def loop(self):
    num = 0
    while True:
      print("-" * 20)
      print("Доска пользователя: ")
      print(self.us.board)
      print("-" * 20)
      print("Доска компьютера: ")
      print(self.ai.board)
      if num % 2 == 0:
        print("-" * 20)
        print("Ходит пользователь")
        repeat = self.us.move()
      else:
        print("-" * 20)
        print("Ходит компьютер")
        repeat = self.ai.move()

      if self.ai.board.count == 7:
        print("-" * 20)
        print("Вы победили!")
        break
      if self.us.board.count == 7:
        print("-" * 20)
        print("Вы проиграли!")
        break
      num += 1

  def start(self):
    self.greet()
    self.loop()


g = Game()
g.start()
