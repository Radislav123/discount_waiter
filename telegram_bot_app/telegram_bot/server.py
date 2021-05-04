from constants.secure.telegram_bot import API_TOKEN
# noinspection PyPackageRequirements
import telebot


bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types = ["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    try:
        print("running on the local machine")
        bot.polling(none_stop = True)
    finally:
        pass
