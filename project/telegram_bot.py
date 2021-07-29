from telebot import telebot

from project.models import Customers, NotificationTasks, db
from secrets import token_hex
from datetime import datetime

token = token_hex()
print(token)

api_telegram = '1517223699:AAE4Y3oTuiCoWxPUP8nKYeulJ0FYhGA2ayA'
bot = telebot.TeleBot(api_telegram)


@bot.message_handler(commands=['start'])
def welcome(message):
    name = message.from_user.first_name
    bot.send_message(message.from_user.id, 'Hello, ' + str(name) + ' You must register to create your order.'
                                                                   'Please write /create ')
    bot.register_next_step_handler(message, c_name)


@bot.message_handler(commands=['create'])
def c_name(message):
    bot.reply_to(message=message, text=f"{message.from_user.first_name}, Create your login: ")
    custom = [i.c_name for i in Customers.query.all()]
    if message.from_user.id not in custom:
        bot.register_next_step_handler(message, password)
        bot.register_next_step_handler(message, phone)
        bot.register_next_step_handler(message, email)
        user = Customers(c_name=c_name(message.text),
                         password=password(message.text),
                         phone=phone(message.text),
                         email=email(message.text),
                         created_dt=datetime.now())
        db.session.add(user)
        db.session.commit()
        bot.send_message(message.from_user.id, text="Register")
    else:
        bot.send_message(message.from_user.id, text="Registered in base")

    bot.register_next_step_handler(message, order_name)


def password(message):
    bot.reply_to(message=message, text=f"{message.from_user.first_name}, Your login is: {message.text}, "
                                       f"create password")
    bot.register_next_step_handler(message, phone)


def phone(message):
    bot.reply_to(message=message, text=f"{message.from_user.first_name}, your password is:  {message.text}, "
                                       f"write your phone")
    bot.register_next_step_handler(message, email)


def email(message):
    bot.reply_to(message=message, text=f"{message.from_user.first_name}, your phone is: {message.text}, "
                                       f"write your email")


def order_name(message):
    bot.reply_to(message=message, text=f"{message.from_user.first_name} , Create your order name: ")
    bot.register_next_step_handler(message, description)


def description(message):
    bot.reply_to(message=message, text=f"{message.from_user.first_name}, Write description")
    bot.register_next_step_handler(message, order_type)


def order_type(message):
    bot.reply_to(message=message, text=f"{message.from_user.first_name}, Write number of order type choise:"
                                       f"1 - Order Type 1"
                                       f"2 - Order Type 2"
                                       f"3 - Order Type 3")
    bot.register_next_step_handler(message, order_create)


def order_create(message):
    order_add = NotificationTasks(name=order_name(message.text),
                                  message=description(message.text),
                                  order_id=order_type(message.text),
                                  create_dt=message.dt)
    db.session.add(order_add)
    db.session.flush()
    db.session.commit()
    bot.reply_to(message, 'Order created')


def notify(chat_id):
    message_to_send = input("Введите сообщение для отправки пользователю: ")
    bot.send_message(chat_id=chat_id, text=message_to_send)


@bot.message_handler(commands=["notify_all"])
def notify_all(message):
    _, user_token = message.text.split()
    if user_token == token:
        profiles = Customers.query.filter_by(is_subscribed=True)
        for profile in profiles:
            notify(chat_id=profile.profile_tg_chat_id)


@bot.message_handler(commands=["subscribe_me"])
def subscribe_profile(message):
    profile = Customers.query.get(int(message.text.split()[1]))
    profile.is_subscribed = True
    profile.chat_id = message.chat.id
    db.session.commit()


@bot.message_handler(commands=["unsubscribe_me"])
def unsubscribe_profile(message):
    profile = Customers.query.get(int(message.text.split()[1]))
    profile.is_subscribed = False
    profile.chat_id = None
    db.session.commit()


if __name__ == "__main__":
    bot.polling()
