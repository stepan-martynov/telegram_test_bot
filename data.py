# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import config
from psycopg2 import sql


def are_in_db(user):
    try:
        user = str(user)
        with psycopg2.connect(dbname=config.dbname, host=config.host, port=config.port) as con:
            with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                try:
                    cur.execute('''
                    SELECT * 
                    FROM users 
                    WHERE chat_id = 
                    %s''', (user,))

                    users_dict = dict(cur.fetchone())
                    if users_dict:
                        return users_dict
                    else:
                        return users_dict
                except Exception as e:
                    print(e)
    except Exception as e:
        print('Can\'t connect to database')


def create_table():
    try:
        with psycopg2.connect(dbname=config.dbname, host=config.host, port=config.port) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                CREATE TABLE users(
                id serial PRIMARY KEY,
                chat_id VARCHAR(100),
                phone_number VARCHAR(32),
                birth_day DATE,
                first_name VARCHAR(32),
                last_name VARCHAR(32),
                organization varchar(32),
                email VARCHAR(32),
                department VARCHAR(32)
                )
                ''')
    except:
        print("Can't create table users")


def new_record(table_name, params):
    try:
        with psycopg2.connect(dbname=config.dbname, host=config.host, port=config.port) as conn:
            with conn.cursor() as cur:
                try:
                    sql_string = sql.SQL("INSERT INTO {}({}) VALUES ({})").format(
                        sql.Identifier(table_name),
                        sql.SQL(', ').join(map(sql.Identifier, params)),
                        sql.SQL(', ').join(map(sql.Placeholder, params))
                    )
                    cur.execute(sql_string, params)
                except Exception as e:
                    print(e)
    except:
        print('Не могу подключиться к Базе данных')


def update_phone_number(chat_id, phone_number):
    chat_id = str(chat_id)
    phone_number = str(phone_number)
    try:
        with psycopg2.connect(dbname=config.dbname, host=config.host, port=config.port) as conn:
            with conn.cursor() as cur:
                cur.execute('''UPDATE users SET phone_number = %s WHERE chat_id = %s''',
                            (phone_number, chat_id))
    except Exception as e:
        print('Can\'t connect to db')


def update_state(chat_id, state, table_name='users'):
    try:
        with psycopg2.connect(dbname=config.dbname, host=config.host, port=config.port) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE %s SET state = %s WHERE chat_id = %s",
                            (table_name, state, chat_id))
    except Exception as e:
        print('Can\'t connect to db')
