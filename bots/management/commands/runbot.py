from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import Group, User

from telebot import TeleBot, types

bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


@bot.message_handler(commands=['start'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    groups_button = types.KeyboardButton('Show all groups')
    users_button = types.KeyboardButton('Show all users')

    markup.add(groups_button, users_button)
    bot.send_message(message.chat.id, 'Welcome!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.chat.type == 'private':
        if message.text == 'Show all groups':
            groups = Group.objects.all()
            chat_message = ''
            if groups:
                for group in groups:
                    chat_message += f"{str(group.id)}: {group.group_name} \n"
            else:
                chat_message = "groups list is empty"

            bot.send_message(message.chat.id, chat_message)
        elif message.text == 'Show all users':
            users = User.objects.all()
            chat_message = ''
            for user in users:
                user_group = Group.objects.filter(id=user.group_id_id).first()
                if users:
                    if user_group:
                        chat_message += f"{str(user.id)}: {user.username} belongs to: {user_group.group_name} \n"
                else:
                    chat_message = "users list is empty"

            bot.send_message(message.chat.id, chat_message)


class Command(BaseCommand):
    help = 'Command for running telegram bot'

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()
