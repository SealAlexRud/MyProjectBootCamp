import requests
import enum  #модуль перечисления
#Enum - класс, который представляет собой набор именнованных значений


class Valutes(enum.Enum):
  RUB = "RUB"
  USD = "USD"
  EUR = "EUR"


class ERRORS(enum.Enum):
  INCORRECT_ANOUNT = "Некорректно задано число!"


class MESSAGES(enum.Enum):
  HELP = "Вас приветствует бот, который поможет вам в конвертации валют! \n Выберите валюты и напишите кол-во!"
  VALUES = "Доступные валюты для использования: \n *ЕВРО (EUR)\n*ДОЛЛАР (USD)\n*РУБЛЬ (RUB)"
  FIRST_VALUTE = "Валюта для конвертации"
  SECOND_VALUTE = "Валюта, в которую хотите переконвертирвоать"
  AMOUNT_VALUTE = "Введите кол-во первой валюты"


class Convertor:

  def __init__(self, base, quote, amount):
    self.base = base
    self.quote = quote
    self.amount = amount

  def get_price(self):
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    if self.base == Valutes.RUB.value:
      valueBase = 1.0
    else:
      valueBase = float(data.json()["Valute"][self.base]["Value"])

    if self.quote == Valutes.RUB.value:
      valueQuote = 1.0
    else:
      valueQuote = float(data.json()["Valute"][self.quote]["Value"])

    heft = self.amount / valueQuote
    return round(heft * valueBase, 5)


class APIException(Exception):

  def __init__(self, error):
    self.error = error
