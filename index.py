from flask import Flask, session, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersModel, CarsModel, DealersModel
from forms import LoginForm, RegisterForm, AddCarForm, SearchPriceForm, SearchDealerForm, AddDealerForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
UsersModel(db.get_connection()).init_table()
CarsModel(db.get_connection()).init_table()
DealersModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    """
    ������� ��������
    :return:
    �������� �������� �����, ���� �������� �� ����������
    """
    # ���� ������������ �� �����������, ������ ��� �� �������� �����
    if 'username' not in session:
        return redirect('/login')
    # ���� �����, �� ��� �� ���� ��������
    if session['username'] == 'admin':
        return render_template('index_admin.html', username=session['username'])
    # ���� ������� ������������, �� ��� �� ����
    cars = CarsModel(db.get_connection()).get_all()
    return render_template('car_user.html', username=session['username'], title='�������� ����', cars=cars)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    �������� �����������
    :return:
    ������������� �� �������, ���� ����� ����� �����������
    """
    form = LoginForm()
    if form.validate_on_submit():  # ����� ����� � ������
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        # ��������� ������� ������������ � �� � ���������� ������
        if user_model.exists(user_name)[0] and check_password_hash(user_model.exists(user_name)[1], password):
            session['username'] = user_name  # ���������� � ������ ��� ������������ � ������ �� �������
            return redirect('/index')
        else:
            flash('������������ ��� ������ �� �����')
    return render_template('login.html', title='�����������', form=form)


@app.route('/logout')
def logout():
    """
    ����� �� �������
    :return:
    """
    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    ����� �����������
    """
    form = RegisterForm()
    if form.validate_on_submit():
        # ������� ������������
        users = UsersModel(db.get_connection())
        if form.user_name.data in [u[1] for u in users.get_all()]:
            flash('����� ������������ ��� ����������')
        else:
            users.insert(user_name=form.user_name.data, email=form.email.data,
                         password_hash=generate_password_hash(form.password_hash.data))
            # �������� �� ������� ��������
            return redirect(url_for('index'))
    return render_template("register.html", title='����������� ������������', form=form)


"""������ � ������"""


@app.route('/car_admin', methods=['GET'])
def car_admin():
    """
    ����� ���� ���������� �� ���� ������� �����
    :return:
    ���������� ��� ��������������� ������������
    """
    # ���� ������������ �� �����������, ������ ��� �� �������� �����
    if 'username' not in session:
        return redirect('/login')
    # ���� �����, �� ��� �� ���� ��������
    if session['username'] != 'admin':
        flash('������ ��������')
        redirect('index')
    # ���� ������� ������������, �� ��� �� ����
    cars = CarsModel(db.get_connection()).get_all()
    return render_template('car_admin.html',
                           username=session['username'],
                           title='�������� �����',
                           cars=cars)


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    """
    ���������� ������ �����
    """
    # ���� ������������ �� �����������, ������ ��� �� �������� �����
    if 'username' not in session:
        return redirect('login')
    # ���� �����, �� ��� �� ���� ��������
    if session['username'] != 'admin':
        return redirect('index')
    form = AddCarForm()
    available_dealers = [(i[0], i[1]) for i in DealersModel(db.get_connection()).get_all()]
    form.dealer_id.choices = available_dealers
    if form.validate_on_submit():
        # ������� ����������
        cars = CarsModel(db.get_connection())
        cars.insert(model=form.model.data,
                    price=form.price.data,
                    power=form.power.data,
                    color=form.color.data,
                    dealer=form.dealer_id.data)
        # �������� �� ������� ��������
        return redirect(url_for('car_admin'))
    return render_template("add_car.html", title='���������� �����', form=form)


@app.route('/car/<int:car_id>', methods=['GET'])
def car(car_id):
    """
    ����� ���� ���������� � ������
    :return:
    ���������� ��� ��������������� ������������
    """
    # ���� ������������ �� �����������, ������ ��� �� �������� �����
    if 'username' not in session:
        return redirect('/login')
    # ���� �� �����, �� ��� �� ������� ��������
    '''if session['username'] != 'admin':
        return redirect(url_for('index'))'''
    # ����� ������ ����������
    car = CarsModel(db.get_connection()).get(car_id)
    dealer = DealersModel(db.get_connection()).get(car[5])
    return render_template('car_info.html',
                           username=session['username'],
                           title='�������� �����',
                           car=car,
                           dealer=dealer[1])


@app.route('/search_price', methods=['GET', 'POST'])
def search_price():
    """
    ������ �����, ��������������� ������������ ����
    """
    form = SearchPriceForm()
    if form.validate_on_submit():
        # �������� ��� ������ �� ������������ ����
        cars = CarsModel(db.get_connection()).get_by_price(form.start_price.data, form.end_price.data)
        # �������� �� �������� � ������������
        return render_template('car_user.html', username=session['username'], title='�������� ����', cars=cars)
    return render_template("search_price.html", title='������ �� ����', form=form)


@app.route('/search_dealer', methods=['GET', 'POST'])
def search_dealer():

    form = SearchDealerForm()
    available_dealers = [(i[0], i[1]) for i in DealersModel(db.get_connection()).get_all()]
    form.dealer_id.choices = available_dealers
    if form.validate_on_submit():
        #
        cars = CarsModel(db.get_connection()).get_by_dealer(form.dealer_id.data)
        # �������� �� ������� ��������
        return render_template('car_user.html', username=session['username'], title='�������� ����', cars=cars)
    return render_template("search_dealer.html", title='������ �� ����', form=form)


'''������ � ���������'''


@app.route('/dealer_admin', methods=['GET'])
def dealer_admin():

    # ���� ������������ �� �����������, ������ ��� �� �������� �����
    if 'username' not in session:
        return redirect('/login')
    # ���� �����, �� ��� �� ���� ��������
    if session['username'] != 'admin':
        flash('������ ��������')
        redirect('index')
    # ����� ��� �����
    dealers = DealersModel(db.get_connection()).get_all()
    return render_template('dealer_admin.html',
                           username=session['username'],
                           title='�������� �� ���������',
                           dealers=dealers)


@app.route('/dealer/<int:dealer_id>', methods=['GET'])
def dealer(dealer_id):
    """
    ����� ���� ���������� � ��������
    :return:
    ���������� ��� ��������������� ������������
    """
    # ���� ������������ �� �����������, ������ ��� �� �������� �����
    if 'username' not in session:
        return redirect('/login')
    # ���� �� �����, �� ��� �� ������� ��������
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    # ����� ������ ����������
    dealer = DealersModel(db.get_connection()).get(dealer_id)
    return render_template('dealer_info.html',
                           username=session['username'],
                           title='�������� ���������� � ��������',
                           dealer=dealer)


@app.route('/add_dealer', methods=['GET', 'POST'])
def add_dealer():
    """
    ���������� �������� � ����� �� ����� ���������� � ���
    """
    # ���� ������������ �� �����������, ������ ��� �� �������� �����
    if 'username' not in session:
        return redirect('/login')
    # ���� �����, �� ��� �� ���� ��������
    if session['username'] == 'admin':
        form = AddDealerForm()
        if form.validate_on_submit():
            # ������� ������
            dealers = DealersModel(db.get_connection())
            dealers.insert(name=form.name.data, address=form.address.data)
            # �������� �� ������� ��������
            return redirect(url_for('index'))
        return render_template("add_dealer.html", title='���������� ���������� ������', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
class UsersModel:
    """�������� �������������"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """������������� �������"""
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
        """������� ����� ������"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin) 
                          VALUES (?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin)))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name):
        """��������, ���� �� ������������ � �������"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        row = cursor.fetchone()
        return (True, row[2], row[0]) if row else (False,)

    def get(self, user_id):
        """������� ������������ �� id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """������ ���� �������������"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows


class DealersModel:
    """�������� �������"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """������������� �������"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS shop 
                            (dealer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20) UNIQUE,
                             address VARCHAR(128)
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, address):
        """���������� ������"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO shop 
                          (name, address) 
                          VALUES (?,?)''',
                       (name, address))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """����� ������ �� ��������"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dealers WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, dealer_id):
        """������ ������ �� id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dealers WHERE dealer_id = ?", (str(dealer_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """������ ���� �������"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM shop")
        rows = cursor.fetchall()
        return rows

    def delete(self, dealer_id):
        """�������� ������"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM shop WHERE dealer_id = ?''', (str(dealer_id)))
        cursor.close()
        self.connection.commit()


class CarsModel:
    """�������� �����"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """������������� �������"""
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
        """���������� ������ �����"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO footwear 
                          (model, price, color, dealer) 
                          VALUES (?,?,?,?)''',
                       (model, str(price), str(power), color, str(dealer)))
        cursor.close()
        self.connection.commit()

    def exists(self, model):
        """����� ����� �� ������"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM footwear WHERE model = ?",
                       model)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, car_id):
        """����� ������ �� id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM footwear WHERE footwear_id = ?", (str(car_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """������ ���� �������"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, footwear_id FROM footwear")
        rows = cursor.fetchall()
        return rows

    def delete(self, car_id):
        """�������� ������"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM footwear WHERE footwear_id = ?''', (str(footwear_id)))
        cursor.close()
        self.connection.commit()

    def get_by_price(self, start_price, end_price):
        """������ ������ �� ����"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, footwear_id FROM footwear WHERE price >= ? AND price <= ?", (str(start_price), str(end_price)))
        row = cursor.fetchall()
        return row

    def get_by_dealer(self, dealer_id):
        """������ ������ �� ��������"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, price, footwear_id FROM cars WHERE dealer = ?", (str(dealer_id)))
        row = cursor.fetchall()
        return row