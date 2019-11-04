from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True, help='This field cannot be left blank')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': f'Item {name} not found'}, 404

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return None, 204

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(data.name, **data)
        else:
            item.price = data.price
            item.store_id = data.store_id
        item.save_to_db()  # because that item is uniquely identified by id (then if exists it will be updated if not it i will be created
        return item.json()


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True, help='This field cannot be left blank')

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

    def post(self):
        data = ItemList.parser.parse_args()
        if ItemModel.find_by_name(data.name):
            return {'message': f'Item {data.name} already exists'}, 400
        item = ItemModel(**data)
        item.save_to_db()
        return item.json(), 201
