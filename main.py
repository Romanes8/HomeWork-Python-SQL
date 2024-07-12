import psycopg2
from tabulate import tabulate
import functions as f


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    print("Выберите действие: ")
    print("1 - создать таблицы БД")
    print("2 - добавить клиента")
    print("3 - добавить телефон клиенту")
    print("4 - добавить email клиенту")
    print("5 - изменить данные о клиенте")
    print("6 - удалить номер телефона клиента")
    print("7 - удалить email клиента")
    print("8 - удалить клиента")
    print("9 - выполнить поиск клиента")
    action = str(input("Введите номер действия: "))
    if action == '1':
        f.create_db(conn) #вызов функции создания таблиц
    if action == '2':
        name = input("Введите имя клиента: ")
        lastname = input("Введите фамилию клиента: ")
        phone_number = input("Введите номер телефона клиента или нажмите ENTER, чтобы пропустить: ")
        phone=0
        if phone_number == '':
            phone = None
        else:
            phone = phone_number
        client_email = input("Введите email клиента или нажмите ENTER, чтобы пропустить: ")
        email='mail'
        if email == '':
            email = None
        else:
            email = client_email
        f.add_client(conn, name, lastname, email, phone) #вызов функции добавления клиента
        print("Клиент успешно добавлен")
    if action == '3':
        clients_id = input("Введите id клиента: ")
        phone = input("Введите номер телефона клиента: ")
        f.add_phone(conn, clients_id, phone) #вызов функции добавления телефона
        print("Номер телефона успешно добавлен")
    if action == '4':
        clients_id = input("Введите id клиента: ")
        e_mail = input("Введите email клиента: ")
        f.add_email(conn, clients_id, e_mail) #вызов функции добавления email
        print("email успешно добавлен")
    if action == '5':
        id = input("Введите id клиента: ")
        client_name = input("Введите имя клиента или нажмите ENTER, чтобы пропустить: ")
        name='name'
        if client_name == '':
            name = None
        else:
            name = client_name
        client_lastname = input("Введите фамилию клиента или нажмите ENTER, чтобы пропустить: ")
        lastname = 'lastname'
        if client_lastname == '':
            lastname = None
        else:
            lastname = client_lastname
        phone_number = input("Введите номер телефона клиента или нажмите ENTER, чтобы пропустить: ")
        phone = 0
        if phone_number == '':
            phone = None
        else:
            phone = phone_number
        client_email = input("Введите email клиента или нажмите ENTER, чтобы пропустить: ")
        email = 'mail'
        if email == '':
            email = None
        else:
            email = client_email
        f.client_change(conn, id, name, lastname, email, phone) #вызов функции изменения данных о клиенте
        print("Данные о клиенте успешно изменены")
    if action == '6':
        id = input("Введите id клиента: ")
        phone = input("Введите номер телефона клиента: ")
        f.delete_phone(conn, id, phone) #вызов функции удаления телефона
    if action == '7':
        id = input("Введите id клиента: ")
        e_mail = input("Введите email клиента: ")
        f.delete_email(conn, id, e_mail) #вызов функции удаления email
    if action == '8':
        id = input("Введите id клиента: ")
        f.delete_client(conn, id) #вызов функции удаления клиента
    if action == '9':
        client_name = input("Введите имя клиента или нажмите ENTER, чтобы пропустить: ")
        name = 'name'
        if client_name == '':
            name = None
        else:
            name = client_name
        client_lastname = input("Введите фамилию клиента или нажмите ENTER, чтобы пропустить: ")
        lastname = 'lastname'
        if client_lastname == '':
            lastname = None
        else:
            lastname = client_lastname
        phone_number = input("Введите номер телефона клиента или нажмите ENTER, чтобы пропустить: ")
        phone = 0
        if phone_number == '':
            phone = None
        else:
            phone = phone_number
        client_email = input("Введите email клиента или нажмите ENTER, чтобы пропустить: ")
        email = 'mail'
        if email == '':
            email = None
        else:
            email = client_email
        f.find_client(conn, name, lastname, email, phone) #вызов функции поиска клиента
conn.close()
