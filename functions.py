import psycopg2
from tabulate import tabulate


#функция создания таблиц clients, phones, email
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS clients
                            (id SERIAL PRIMARY KEY,
                             name VARCHAR(20) NULL,
                             lastname VARCHAR(20) NULL
                            );"""
                    );

        cur.execute("""CREATE TABLE IF NOT EXISTS phones
                                (id SERIAL PRIMARY KEY,
                                clients_id INTEGER NOT NULL REFERENCES clients(id),
                                phone VARCHAR(60) NULL
                                );"""
                    );

        cur.execute("""CREATE TABLE IF NOT EXISTS email
                                 (id SERIAL PRIMARY KEY,
                                 clients_id INTEGER NOT NULL REFERENCES clients(id),
                                 email VARCHAR(60) NULL
                                 );"""
                    );
        print("Таблицы clients, phones, email успешно созданы.")
    conn.commit()

#функция добавления клиента
def add_client(conn, name, lastname, e_mail=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO clients (name, lastname) VALUES(%s, %s) RETURNING id;
                    """, (name, lastname));

        #id клиента сохраняется в переменной clients_id для его передачи в связанные таблицы email и phones
        clients_id = cur.fetchone()[0]

        cur.execute("""INSERT INTO email (clients_id, email) VALUES(%s, %s);
                    """, (clients_id, e_mail));

        cur.execute("""INSERT INTO phones (clients_id, phone) VALUES(%s, %s);
                    """, (clients_id, phone));
    conn.commit()



#функция добавления телефона клиенту
def add_phone(conn, clients_id, phone):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phones (clients_id, phone) VALUES(%s, %s);
                    """, (clients_id, phone))
    conn.commit()

#функция добавления email клиенту
def add_email(conn, clients_id, e_mail):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO email (clients_id, email) VALUES(%s, %s);
                    """, (clients_id, e_mail))
    conn.commit()


#функция изменения данных о клиенте
def client_change(conn, id, name=None, lastname=None, email=None, phone=None):
    with conn.cursor() as cur:
        if name != None:
            cur.execute("""UPDATE clients
                           SET name=%s
                           WHERE id=%s;
                           """, (name, id));
        else:
            pass

        if lastname != None:
            cur.execute("""UPDATE clients
                           SET lastname=%s
                           WHERE id=%s
                           """, (lastname, id));
        else:
            pass

        if email != None:
            cur.execute("""SELECT COUNT(clients_id) FROM email
                           WHERE clients_id=%s""", (id,));
            count = cur.fetchone()[0]
            if count > 1:
                print(f"Клиент имеет {count} адресов e-mail, выберите адрес для изменения: ")

                cur.execute("""SELECT clients_id, email FROM email
                               WHERE clients_id=%s""", (id,));
                numbers=cur.fetchall()
                for cortage in numbers:
                    print(cortage[1])
                update_email = input("Введите адрес e-mail, который хотите изменить: ")
                cur.execute("""UPDATE email
                               SET email=%s
                               WHERE clients_id=%s AND email=%s""", (email, id, update_email));
                print(f"Адрес e-mail {update_email} изменен на {email}")
            else:
                cur.execute("""UPDATE email
                               SET email=%s
                               WHERE clients_id=%s""", (email, id,));
                print(f"Адрес e-mail изменен на {email}")
        else:
            pass


        if phone != None:
            cur.execute("""SELECT COUNT(clients_id) FROM phones
                        WHERE clients_id=%s""", (id,));
            count = cur.fetchone()[0]
            if count > 1:
                print(f"Клиент имеет {count} номеров телефона, выберите телефон для изменения: ")

                cur.execute("""SELECT clients_id, phone FROM phones
                       WHERE clients_id=%s""", (id,));
                numbers=cur.fetchall()
                for cortage in numbers:
                    print(cortage[1])
                update_number = int(input("Введите номер телефона, который хотите изменить: "))
                cur.execute("""UPDATE phones
                               SET phone=%s
                               where clients_id=%s AND phone=%s""", (phone, id, update_number));
                print(f"Номер телефона {update_number} изменен на {phone}")
            else:
                cur.execute("""UPDATE phones
                               SET phone=%s
                               where clients_id=%s""", (phone, id,));
                print(f"Номер телефона изменен на {phone}")
        else:
            pass
    conn.commit()


#функция удаления номера телефона
def delete_phone(conn, id, phone):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phones
                       WHERE clients_id=%s AND phone=%s""", (id, phone,));
        print(f"Номер телефона {phone} удален.")
    conn.commit()

#функция удаления email
def delete_email(conn, id, e_mail):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM email
                       WHERE clients_id=%s AND email=%s""", (id, e_mail,));
        print(f"email адрес {e_mail} удален.")
    conn.commit()


#функция удаления клиента
def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM email
                       WHERE clients_id=%s""", (id,));

        cur.execute("""DELETE FROM phones
                       WHERE clients_id=%s""", (id,));

        cur.execute("""DELETE FROM clients
                       WHERE id=%s""", (id,));
        print(f"Клиент с id={id} удален.")
    conn.commit()


#функция поиска клиента
def find_client(conn, name=None, lastname=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""SELECT c.id, name, lastname, phone, email
                       FROM clients c
                       LEFT JOIN phones p ON c.id = p.clients_id
                       LEFT JOIN email e ON c.id = e.clients_id
                       WHERE name=%s OR lastname=%s OR email=%s OR phone=%s;
                       """, (name, lastname, email, phone));

        data = cur.fetchall()
        print(data)
        # вывод таблицы с использованием модуля tabulate
        headers = ['id', 'name', 'lastname', 'phone', 'email']
        print(tabulate(data, headers=headers, tablefmt='grid'))


