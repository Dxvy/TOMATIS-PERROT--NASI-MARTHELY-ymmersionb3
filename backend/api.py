import sqlalchemy as db


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
