from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import Group, User

from telebot import TeleBot

bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


@bot.message_handler(commands=['groups'])
def send_groups(message):
    groups = Group.objects.all()
    chat_message = ''
    for group in groups:
        chat_message += f"{str(group.id)}: {group.group_name} \n"

    bot.send_message(message.chat.id, chat_message)


@bot.message_handler(commands=['users'])
def send_users(message):
    users = User.objects.all()
    chat_message = ''
    for user in users:
        user_group = Group.objects.filter(id=user.group_id_id).first()
        if user_group:
            chat_message += f"{str(user.id)}: {user.username} belongs to: {user_group.group_name} \n"

    bot.send_message(message.chat.id, chat_message)


class Command(BaseCommand):
    help = 'Command for running telegram bot'

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()
