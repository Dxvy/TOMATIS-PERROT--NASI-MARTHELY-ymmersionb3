import sqlalchemy as db
from werkzeug.security import check_password_hash


class DataBase:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        engine = db.create_engine(f'mysql://{self.user}:{self.password}@{self.host}'
                                  f':{self.port}/{self.database}')
        connection = engine.connect()
        metadata = db.MetaData()
        users = db.Table('users', metadata, autoload_with=engine, extend_existing=True)
        products = db.Table('products', metadata, autoload_with=engine, extend_existing=True)
        return connection, users, products

    def get_all_products(self):
        connection, users, products = self.connect()
        query = db.select(products)
        result = connection.execute(query).fetchall()
        return result

    def get_product_by_id(self, product_id):
        connection, users, products = self.connect()
        query = db.select(products).where(products.columns.id == product_id)
        result = connection.execute(query).first()
        return result

    def get_recommended_products(self):
        connection, users, products = self.connect()
        query = db.select(products).order_by(db.func.rand()).limit(4)
        result = connection.execute(query)
        results_set = result.fetchall()
        return results_set

    def get_products_by_string(self, string):
        connection, users, products = self.connect()
        query = db.select(products).where(db.or_(products.columns.name.like(f'%{string}%'),
                                                 products.columns.type.like(f'%{string}%'),
                                                 products.columns.size.like(f'%{string}%'),
                                                 products.columns.sorting.like(f'%{string}%'),
                                                 products.columns.color.like(f'%{string}%'),
                                                 products.columns.price.like(f'%{string}%'),
                                                 products.columns.description.like(f'%{string}%')))
        result = connection.execute(query)
        results_set = result.fetchall()
        return results_set

    def add_product(self, name, type, size, sorting, color, price, description, quantity):
        connection, users, products = self.connect()
        query = db.insert(products).values(name=name, type=type, size=size, sorting=sorting, color=color, price=price, description=description, quantity=quantity)
        result = connection.execute(query)

        # if product downloaded failed
        if not self.get_product_by_id(self.get_last_product_id()):
            return False
        return result.inserted_primary_key[0]

    def get_user_by_id(self, user_id):
        connection, users, products = self.connect()
        query = db.select(users).where(users.columns.id == int(user_id))
        result = connection.execute(query)
        results_set = result.fetchall()
        return results_set

    def get_user_by_email(self, email):
        connection, users, products = self.connect()
        query = db.select(users).where(users.columns.email == email)
        result = connection.execute(query)
        results_set = result.fetchall()
        return results_set

    def get_user_by_phone(self, phone):
        connection, users, products = self.connect()
        query = db.select(users).where(users.columns.phone == phone)
        result = connection.execute(query)
        results_set = result.fetchall()
        return results_set

    def get_user_password(self, email):
        connection, users, products = self.connect()
        query = db.select(users).where(users.columns.email == email)
        result = connection.execute(query).first()
        return result.password

    def get_user_guid(self, email):
        connection, users, products = self.connect()
        query = db.select(users).where(users.columns.email == email)
        result = connection.execute(query).first()
        return result.guid

    def insert_user(self, email, name, lastname, phone, type, company, password):
        connection, users, products = self.connect()
        user = self.get_user_by_email(email)
        user_phone = self.get_user_by_phone(phone)
        if user or user_phone:
            return False
        query = db.insert(users).values(email=email, name=name, lastname=lastname, phone=phone, type=type, company=company, password=password)
        result = connection.execute(query)
        return True

    def check_login(self, email, password_input):
        connection, users, products = self.connect()
        print(email)
        print(password_input)
        user = self.get_user_by_email(email)
        print(user)
        password = self.get_user_password(email)
        print(password)
        if user and check_password_hash(password, password_input):
            print('Login successful')
            return True
        print('Login failed')
        return False

    def get_last_product_id(self):
        connection, users, products = self.connect()
        query = db.select(products).order_by(products.columns.id.desc()).limit(1)
        result = connection.execute(query).first()
        return result.id
