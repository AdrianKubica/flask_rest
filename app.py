from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt import JWT
from flask_restful import Api
from security import authenticate, identity
from resources.user import UserRegister

from resources.item import Item, ItemList
from resources.store import Store, StoreList  # if we dont import appropraite models table for stores wont be created

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # sqlite db is placed in a root directory of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Main SQLAlchemy has its own modification tracker which is better than Flask-SQLAlchemy one
app.secret_key = 'jose'
# app.config['JWT_VERIFY_EXPIRATION'] = False  # nie będzie wygasał token - na produkcji nie jest to zalecane
# app.config['JWT_AUTH_URL_RULE'] = '/login'  # zmiana url do uzyskania autoryzacji
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)  # zmiana dlugosci waznosci tokenu
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'  # zmiana przekazywanych parametrow jakie musza znalezc sie w payload podczas uzyskiwania tokena
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()  # tworzy wszystkie tabele automatycznie o ile juz nie istnieja w bazie danych


jwt = JWT(app, authenticate, identity)  # creates new endpoint /auth


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
