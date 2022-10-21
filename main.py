import psycopg2

def delete_db(cursor):
    '''Удаление таблиц'''
    cursor.execute("""
           DROP TABLE phone;
           DROP TABLE client;
       """)
    print('Таблицы успешно удалены')


def create_db(cursor):
    '''Создание таблиц'''
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client(
        client_id SERIAL PRIMARY KEY,
        first_name VARCHAR(64),
        last_name VARCHAR(64),
        email VARCHAR(64),
        phones VARCHAR(64)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phone(
        phone_id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES client(client_id),
        phone_number VARCHAR(64) NOT NULL
    );
    """)
    print("Таблица успешно создана")


def add_client(cursor, first_name, last_name, email, phones=None):
    """Добаление нового клиента"""
    cursor.execute("""
        INSERT INTO client(first_name, last_name, email, phones) VALUES(%s, %s, %s, %s);
        """, (first_name, last_name, email, phones))
    print("Новый клиент успешно добавлен")

def add_phone(cursor, client_id, phone):
    '''Добавление нового номера телефона к клиенту'''
    cursor.execute("""
        INSERT INTO phone(client_id, phone_number) VALUES(%s, %s);
        """, (client_id, phone))
    print("Добавление номера телефона к клиенту произошло")


def change_client(cursor, client_id, first_name=None, last_name=None, email=None, phones=None):
    '''Изменение данных о клиенте'''
    if first_name:
        cursor.execute("""
        UPDATE client SET first_name =%s
        WHERE client_id =%s;
        """, (first_name, client_id))
        if last_name:
            cursor.execute("""
                UPDATE client SET last_name =%s
                WHERE client_id =%s;
                """, (last_name, client_id))
            if email:
                cursor.execute("""
                    UPDATE client SET email =%s
                    WHERE client_id =%s;
                    """, (email, client_id))
                if phones:
                    cursor.execute("""
                        UPDATE client SET phones =%s
                        WHERE client_id =%s;
                        """, (phones, client_id))
                    print('Все данные успешно изменены!')
                else:
                    print('Колонки first_name, last_name, email изменены')
            else:
                print('Колонки first_name, last_name изменены')
        else:
            print('Колонка first_name изменена')
    else:
        print("Данные для изменения не введены!")



def delete_phone(cursor, client_id, phone):
    '''Удаление телефона для существующего клиента'''
    cursor.execute("""
        DELETE FROM phone
        WHERE client_id = %s AND
        phone_number = %s;
    """, (client_id, phone))
    print('Номер телефона успешно удален')

def delete_clients(cursor, client_id):
    '''Удаление существующего клиента'''
    cursor.execute("""
        DELETE FROM client
        WHERE client_id = %s;
    """, (client_id,))
    print('Удаление существующего клиента произошло')

def find_client(cursor, first_name=None, last_name=None, email=None, phone=None):
    '''Поиск клиента по его данным'''
    if first_name and last_name and email:
        cursor.execute("""
            SELECT * FROM client c
            JOIN phone p ON c.client_id = p.client_id
            WHERE c.first_name = %s AND
                c.last_name = %s AND
                c.email = %s;
            """, (first_name, last_name, email))
        print(cur.fetchall())
    else:
        cursor.execute("""
            SELECT * FROM client c
            JOIN phone p ON c.client_id = p.client_id
            WHERE c.first_name = %s AND
                c.last_name = %s AND
                p.phone_number = %s;
            """, (first_name, last_name, phone))
        print(cur.fetchall())




if __name__ == "__main__":

    with psycopg2.connect(database="personal_db", user='postgres', password='postgres') as conn:
        with conn.cursor() as cur:
            create_db(cur)
            add_client(cur, 'Amir', 'Dautov', 'amr@mail.ru')
            add_phone(cur, 1, '79833892211')
            change_client(cur, 1, 'Alesha', 'Popkov', 'amrt@yandex.ru', '7919400034')
            delete_phone(cur, 1, '79833892211')
            delete_clients(cur, 1)
            find_client(cur, 'Alesha', 'Popkov', phone='79833892211')

    conn.close()


