class UsersModel:
    """Сущность пользователей"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(20) UNIQUE,
                             password_hash VARCHAR(128),
                             email VARCHAR(20),
                             is_admin INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, email, is_admin=False):
        """Вставка новой записи"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin) 
                          VALUES (?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin)))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name):
        """Проверка, есть ли пользователь в системе"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        row = cursor.fetchone()
        return (True, row[2], row[0]) if row else (False,)

    def get(self, user_id):
        """Возврат пользователя по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех пользователей"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows


class DealersModel:
    """Сущность центров"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS shop 
                            (dealer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20) UNIQUE,
                             address VARCHAR(128)
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, address):
        """Добавление центра"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO shop 
                          (name, address) 
                          VALUES (?,?)''',
                       (name, address))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск центра по названию"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dealers WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, dealer_id):
        """Запрос центра по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dealers WHERE dealer_id = ?", (str(dealer_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех центров"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM shop")
        rows = cursor.fetchall()
        return rows

    def delete(self, dealer_id):
        """Удаление центра"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM shop WHERE dealer_id = ?''', (str(dealer_id)))
        cursor.close()
        self.connection.commit()


class CarsModel:
    """Сущность цветов"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS footwear 
                            (car_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             model VARCHAR(20),
                             price INTEGER,
                             power INTEGER,
                             color VARCHAR(20),
                             dealer INTEGER
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, model, price, power, color, dealer):
        """Добавление вида цветов"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO footwear 
                          (model, price, color, dealer) 
                          VALUES (?,?,?,?)''',
                       (model, str(price), str(power), color, str(dealer)))
        cursor.close()
        self.connection.commit()

    def exists(self, model):
        """Поиск цветов по виду"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM footwear WHERE model = ?",
                       model)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, car_id):
        """Поиск вида по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM footwear WHERE footwear_id = ?", (str(car_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех видов"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, footwear_id FROM footwear")
        rows = cursor.fetchall()
        return rows

    def delete(self, car_id):
        """Удаление вида"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM footwear WHERE footwear_id = ?''', (str(footwear_id)))
        cursor.close()
        self.connection.commit()

    def get_by_price(self, start_price, end_price):
        """Запрос вида по цене"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, footwear_id FROM footwear WHERE price >= ? AND price <= ?", (str(start_price), str(end_price)))
        row = cursor.fetchall()
        return row

    def get_by_dealer(self, dealer_id):
        """Запрос вида по магазину"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, footwear_id FROM cars WHERE dealer = ?", (str(dealer_id)))
        row = cursor.fetchall()
        return row