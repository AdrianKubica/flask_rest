from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    # this is a list of items, whenever we create StoreModel object,
    # we also create all items connected with that store_id, its can be expensive operation
    # w tym celu mozemy wykorzystac lazy='dynamic' to prevent for that situation
    # jesli korzystamy z lazy dynamic to self.items wygeneruje blad chybaze jawnie wywolamy metode .all()

    def __init__(self, name):
        self.name = name

    def json(self):  # to znaczy ze dopoki nie wywolamy metody json() wykorzystujacej jawnie .all() items ze store nie beda tworzone
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
