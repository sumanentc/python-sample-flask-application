from flask import request
from flask_restplus import Resource, fields, Namespace

from models.item import ItemModel
from schemas.item import ItemSchema

ITEM_NOT_FOUND = "Item not found."


item_ns = Namespace('item', description='Item related operations')
items_ns = Namespace('items', description='Items related operations')

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

#Model required by flask_restplus for expect
item = items_ns.model('Item', {
    'name': fields.String('Name of the Item'),
    'price': fields.Float(0.00),
    'store_id': fields.Integer
})


class Item(Resource):

    def get(self, id):
        item_data = ItemModel.find_by_id(id)
        if item_data:
            return item_schema.dump(item_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self,id):
        item_data = ItemModel.find_by_id(id)
        if item_data:
            item_data.delete_from_db()
            return {'message': "Item Deleted successfully"}, 200
        return {'message': ITEM_NOT_FOUND}, 404

    @item_ns.expect(item)
    def put(self, id):
        item_data = ItemModel.find_by_id(id)
        item_json = request.get_json()

        if item_data:
            item_data.price = item_json['price']
            item_data.name = item_json['name']
        else:
            item_data = item_schema.load(item_json)

        item_data.save_to_db()
        return item_schema.dump(item_data), 200


class ItemList(Resource):
    @items_ns.doc('Get all the Items')
    def get(self):
        return item_list_schema.dump(ItemModel.find_all()), 200

    @items_ns.expect(item)
    @items_ns.doc('Create an Item')
    def post(self):
        item_json = request.get_json()
        item_data = item_schema.load(item_json)
        item_data.save_to_db()

        return item_schema.dump(item_data), 201
