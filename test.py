# -*- coding: utf-8 -*-

import telebot
import config
import states
import methods
import data
import time
from states import state_handler

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def call_number(message):
    user_dict = data.are_in_db(message.chat.id)
    if user_dict and user_dict['phone_number']:
        bot.send_message(message.chat.id,
                         'И снова здраствуйте, {} {}!'.format(
                             user_dict['first_name'], user_dict['last_name']))
        state = states.base_state
        bot.send_message(message.chat.id, state['msg'], reply_markup=methods.generate(state))

        return
    elif user_dict and not user_dict['phone_number']:
        pass

    elif not user_dict:
        user = {
            'chat_id': message.chat.id,
            'first_name': message.chat.first_name,
            'last_name': message.chat.last_name
        }
        data.new_record('users', user)

    state = states.ask_phone
    bot.send_message(message.chat.id, state['msg'],
                     reply_markup=methods.call_number(state['keyboard']))


@bot.message_handler(func=lambda message: True, content_types=['contact'])
def check_contact(message):
    # The user send their own contact?
    if message.from_user.id == message.contact.user_id:
        # yes
        bot.send_message(message.chat.id,
                         'Спасибо, {} {}!'.format(message.chat.first_name, message.chat.last_name))
        data.update_phone_number(message.chat.id, message.contact.phone_number)
        state = states.base_state
        bot.send_message(message.chat.id, state['msg'], reply_markup=methods.generate(state))
    else:
        # no
        state = states.ask_phone
        bot.send_message(message.chat.id, 'Попробуйте отправить {}'.format(state['msg']),
                         methods.call_number(state['keyboard']))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    if message.text == 'Узнать погоду':
        state = states.choose_date
        bot.send_message(message.chat.id, state['msg'], reply_markup=methods.generate(state))


@bot.callback_query_handler(func=lambda callback: True)
def inline_answer(callback):
    # нужно написать модуль изменения состояния чата с гет и пост запросами
    print(callback)

    state = state_handler[callback.data]
    new_state = state_handler[state['next_state']]

    bot.edit_message_text(chat_id=callback.message.chat.id,
                          message_id=callback.message.message_id,
                          text=new_state['msg'],
                          reply_markup=methods.generate(new_state))


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(15)
