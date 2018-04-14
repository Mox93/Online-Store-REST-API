from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field can not be left blank!")
    parser.add_argument("store_id", type=int, required=True, help="Every item needs a home!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        return item.json() if item else {"message":"Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message":"An item with the name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "Couldn't save the item due to an error!"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted!"}
        return {"message": "Item doesn't exist!"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data["price"]
            item.store_id = data["store_id"]
        else:
            item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "Couldn't update the item due to an error!"}, 500
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}

