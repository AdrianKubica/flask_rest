from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)  # custom id's such as uuid() need to be explicitly implemented in __init__ method
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # stores refers to table name and id refers to column name
    store = db.relationship('StoreModel')  # every item has property store which is the store that matches suitable store_id
    # order_id integer REFERENCES orders ON DELETE CASCADE  w ten sposob mozemy obluzyc usuwanie kaskadowe, ale dziala tylko przy PostgreSQL

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM __tablename__ WHERE name = name LIMIT 1 - this returns item model object

    def save_to_db(self):
        db.session.add(self)  # session is a collection of objects to write to database
        db.session.commit()  # SQLAlchemy can handle update and insert for us, if we get data from database its know that there is an id that can serve to update data in database

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
