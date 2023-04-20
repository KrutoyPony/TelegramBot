# Собственные модули
from extensions import APIException, ConvertionException

# Чужие модули
import requests
import telebot
import json

# Класс для конвертации валют
class CryptoConvert:
	
	@staticmethod
	def convertor(message, username):
		try:
			values = message.text.split(' ')
			ConvertionException.convertion_one(value= values)
		except ConvertionException as f:
			bot.reply_to(message, f)
			print(f'{username} ввёл не верное кол-во данных') # Инфо. для админа
		else:
			try:
				quote, base, amount = values
				ConvertionException.convertion_two(quote= quote, base= base)
			except ConvertionException as f:
				bot.reply_to(message, f)
				print(f'{username} ввёл одну и ту же валюту!') # Инфо. для админа
			else:
				try:
					int(amount)
				except Exception:
					print(f'{username} ввёл вместо числа текст') # Инфо. для админа
					bot.reply_to(message, f'Значние {amount} не является числом')
				else:
					try:
						ConvertionException.convertion_three(quote= quote, base= base, amount= amount)
					except ConvertionException as f:
						bot.reply_to(message, f)
						print(f'{username} ввёл не верные значения!') # Инфо. для админа
					else:
						try:
							ConvertionException.convertion_four(quote= quote, base= base)
						except ConvertionException as f:
							bot.reply_to(message, f)
							print(f'{username} не нашёл нужных валют ({quote}, {base})') # Инфо. для админа
						else:
							quote_ticker, base_ticker = currencies[quote], currencies[base]
							# С помощью GET запроса получаю данные о курсе валют
							link = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
							total_base = json.loads(link.content)[base_ticker]
							text = f'Цена {amount} {quote_ticker} в {base_ticker} - {total_base * int(amount)}'
							bot.send_message(message.chat.id, text)
# Открываем директорию для получения токена
with open('tele_token.json', 'r', encoding='utf-8') as t:
    token = json.load(t)
    TOKEN = token['TOKEN']

# Открывает директорию для получения валют
with open('currencies.json', 'r', encoding='utf-8') as c:
    currencies = json.load(c)

# Определяем объект Telebot
bot = telebot.TeleBot(TOKEN)

# Определяем обработчик который работает с командами /start и /help
@bot.message_handler(commands=['start', 'help'])
def help_and_start(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\nКоманды\n\nДля получения валют напишите /values \
'
    bot.reply_to(message, text)

# Обработчик отправляет валюты благодаря команде /value
@bot.message_handler(commands=['values'])
def values(message):
	text = 'Доступные валюты: '
	for key in currencies.keys():
		text = '\n'.join((text, key.title(), ))
	bot.reply_to(message, text)

# Обработчик для конвертации
@bot.message_handler(content_types= ['text',])
def convert(message):
	username = message.from_user.username # Беру имя пользователя для аудита
	CryptoConvert.convertor(message, username)
	
# Запуск бота
bot.polling()

# if message.text == 'morokil':
# 		bot.send_message(message.chat.id, f'Morokil лучший канал!')