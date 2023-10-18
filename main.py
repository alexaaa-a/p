import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()

bot = telebot.TeleBot("6443265113:AAGe9qByfM-tDNdwAy69IT3uxmooNtgpNOU",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Полезные каналы"
text_button_1 = "Суточная норма калорий"
text_button_2 = "Счётчик калорий"
text_button_3 = "Дневник тренировок"


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Вот, что у меня есть:',
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, '[BIOMACHINE - канал, с помощью которого ты можешь узнать все нюансы тренировочного процесса](https://youtube.com/@bmchn?si=Cnk4gr1ahlh_WAev)')
    bot.send_message(message.chat.id, '[GetFit - поможет тебе составить твой рацион](https://youtube.com/@GetFit_Nikolay_Panasyuk?si=_31BS1bULAbJQF9N)')
    bot.send_message(message.chat.id, '[Здоровое Будущее - канал, который поможет прокачать твой функцианал](https://youtube.com/@FitTherapyOfficial?si=DVMKWN3hWobufu-n)')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! Приятно познакомиться `возраст?`')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Суточная норма калорий", '(https://food.ru/kalkulyator-kalorii?ysclid=lnuinz5y9s673166784)',reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Счётчик калорий",'(https://www.fatsecret.com/Default.aspx)', reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Дневник тренировок", '(https://gymup.pro)',reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()