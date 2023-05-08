import telebot
from config import TOKEN, keys
from extensions import MoneyConverter, ChangeException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы произвести конвертацию, введите запрос в следующем формате:\n" \
           "<название конвертируемой валюты><название валюты, в которую происходит конвертация>" \
           "<количество конвертируемой валюты>.\nПосмотреть список доступных валют: /values." \
           "\nУказывайте названия валют и сумму для конвертации через один пробел."
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты для конвертации:"
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ChangeException("запрошено слишком много параметров или неверная форма запроса")

        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote, base, amount)
    except ChangeException as ce:
        bot.reply_to(message, f"Ошибка пользователя: {ce}.")
    except Exception as exc:
        bot.reply_to(message, f"Не удалось обработать ваш запрос:\n{exc}")
    else:
        text = f"Стоимость запрошенной валюты:\n{amount} {quote} в {base} - {total_base}."
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
