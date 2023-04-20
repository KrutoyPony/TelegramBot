import json

# файл для классов
class APIException(Exception):
	pass

class ConvertionException(APIException):

	@staticmethod
	# Проверка на ошибку при малом или большём количестве данных
	def convertion_one(value: list):
		if len(value) > 3 or len(value) < 3:
			raise ConvertionException('Ошибка пользователя\nНеверное кол-во данных')

	@staticmethod
	#Проверкf ошибки при конвертации одинаковых валют
	def convertion_two(quote, base):
		if quote == base or base == quote:
			raise ConvertionException('Ошибка сервера\nНельзя конвертировать одну и ту же валюту!')

	@staticmethod
	def convertion_three(quote, base, amount):
		if any([type(quote) == int,
				type(quote) == float,
				type(base) == int,
				type(base) == float,]):
			raise ConvertionException('Ошибка сервера\nВалюта и валюта конвертации не могут быть числовыми значениями!')

	@staticmethod
	def convertion_four(quote, base):
		if quote not in currencies.keys():
			raise ConvertionException(f'Валюта {quote} отсутствует')
		if base not in currencies.keys():
			raise ConvertionException(f'Валюта {base} отсутствует')

with open('currencies.json', 'r', encoding= 'utf-8') as c:
	currencies = json.load(c)

