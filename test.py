import telebot
from telebot import types
import random
import sqlite3


class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('dbbot', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_user(self, iduser):
        self.cursor.execute(f'SELECT iduser FROM users WHERE iduser={iduser}')
        return self.cursor.fetchone()

    def register(self, iduser, name):
        self.cursor.execute(f'INSERT INTO users (iduser, name) VALUES (?, ?)', (iduser, name))
        self.conn.commit()
        return True

    def update_balance(self, iduser,  balance, status):
        # status = True - add balance status = False - take balance
        if status:
            self.cursor.execute(f'UPDATE users SET balance=balance+? WHERE id=?', (balance, iduser))
        else:
            self.cursor.execute(f'UPDATE users SET balance=balance-? WHERE id=?', (balance, iduser))
        self.conn.commit()
        self.cursor.execute(f'SELECT balance FROM users WHERE iduser=?', (iduser,))

    def get_balance(self, iduser):
        self.cursor.execute(f'SELECT balance FROM users WHERE iduser=?', (iduser,))
        return self.cursor.fetchone()


db = Database()
token = 'token'
bot = telebot.TeleBot(token)

gifk = {
    1: '''(●'◡'●)''',
    2: '''༼ つ ◕_◕ ༽つ''',
    3: '''^_^''',
    4: ''':) ''', 
    5: '''-_-''', 

}


def random_gif():
    a = random.randint(1, 4)
    return a


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("Ещё")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text=f'Ваш баланс {db.get_balance(user_id)}', reply_markup=markup)
    bot.send_message(message.chat.id, text=gifk[random_gif()], reply_markup=markup)
    if db.get_user(user_id):
        bot.send_message(message.chat.id, text="Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)
    else:
        db.register(str(user_id), message.from_user.first_name)
        bot.send_message(message.chat.id,
                         text="Добро пожаловать, {0.first_name}!".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "Поздороваться":
        bot.send_message(message.chat.id, text="Привет)")
    elif message.text == "Ещё":
        bot.send_message(message.chat.id, text=gifk[random_gif()], reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Некоректный ввод")


if __name__ == '__main__':
    bot.infinity_polling()
