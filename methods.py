# -*-coding: utf-8 -*-

from telebot import types
import os
import config
import json


def call_number(keyboard):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text=keyboard[0], request_contact=True)
    markup.add(button_phone)
    return markup


def create(keyboard):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in keyboard:
        markup.add(item)
    return markup


def create_inline(keyboard):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for item in keyboard:
        buttons.append(types.InlineKeyboardButton(
            text=item['text'],
            callback_data=item['callback_data']))
    buttons.append(types.InlineKeyboardButton(
        text='отмена',
        callback_data='back'))
    markup.add(*buttons)

    return markup


def generate(state):
    if state['type'] is 'inline_keyboard':
        return create_inline(state['keyboard'])
    if state['type'] is 'keyboard':
        return create(state['keyboard'])


def save_state_to_history(chat_id, message_id, state):
    global full_states_history
    file_path = os.path.join(os.getcwd(), config.states_dir, '.'.join([chat_id, 'json']))
    try:
        with open(file_path) as f:
            full_states_history = json.load(f)
    except Exception as e:
        print(e)
        full_states_history = {}

    finally:
        if message_id not in full_states_history:
            full_states_history[message_id] = []

        full_states_history[message_id].append(state['name'])

        with open(file_path, 'w') as f:
            json.dump(full_states_history, f, indent=2, ensure_ascii=False)


def get_last_state(chat_id, message_id):
    global full_states_history
    file_path = os.path.join(os.getcwd(), config.states_dir, '.'.join([chat_id, 'json']))
    try:
        with open(file_path) as f:
            full_states_history = json.load(f)
    except Exception as e:
        print(e)
        full_states_history = {}

    finally:
        if message_id in full_states_history:
            state_name = full_states_history[message_id].pop()
        else:
            return 'History is lost'

        with open(file_path, 'w') as f:
            json.dump(full_states_history, f, indent=2, ensure_ascii=False)

        return state_name


def remove_message_history(chat_id, message_id):
    global full_states_history
    file_path = os.path.join(os.getcwd(), config.states_dir, '.'.join([chat_id, 'json']))

    try:
        with open(file_path) as f:
            full_states_history = json.load(f)
    except Exception as e:
        print(e)
        full_states_history = {}

    finally:
        if message_id in full_states_history:
            del full_states_history[message_id]
        else:
            return 'History is lost'

        with open(file_path, 'w') as f:
            json.dump(full_states_history, f, indent=2, ensure_ascii=False)
