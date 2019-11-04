from flask_restful import Resource, reqparse

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name=name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def delete(self, name):
        store = StoreModel.find_by_name(name=name)
        if store:
            store.delete_from_db()
            return None, 204
        return {'message': f'Store with name {name} doesnt exists'}


class StoreList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')

    def get(self):
        stores = StoreModel.query.all()
        return {'stores': [store.json() for store in stores]}

    def post(self):
        data = self.parser.parse_args()
        store = StoreModel.find_by_name(name=data.name)
        if store:
            return {'message': f'A store with name {data.name} already exists'}, 400
        store = StoreModel(**data)
        store.save_to_db()
        return store.json(), 201
