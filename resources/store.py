from flask import request
from flask_restplus import Resource, fields, Namespace

from models.store import StoreModel
from schemas.store import StoreSchema

STORE_NOT_FOUND = "Store not found."
STORE_ALREADY_EXISTS = "Store '{}' Already exists."

store_ns = Namespace('store', description='Store related operations')
stores_ns = Namespace('stores', description='Stores related operations')

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

# Model required by flask_restplus for expect
store = stores_ns.model('Store', {
    'name': fields.String('Name of the Store')
})


class Store(Resource):
    def get(self, id):
        store_data = StoreModel.find_by_id(id)
        if store_data:
            return store_schema.dump(store_data)
        return {'message': STORE_NOT_FOUND}, 404

    def delete(self, id):
        store_data = StoreModel.find_by_id(id)
        if store_data:
            store_data.delete_from_db()
            return {'message': "Store Deleted successfully"}, 200
        return {'message': STORE_NOT_FOUND}, 404


class StoreList(Resource):
    @stores_ns.doc('Get all the Stores')
    def get(self):
        return store_list_schema.dump(StoreModel.find_all()), 200

    @stores_ns.expect(store)
    @stores_ns.doc('Create a Store')
    def post(self):
        store_json = request.get_json()
        name = store_json['name']
        if StoreModel.find_by_name(name):
            return {'message': STORE_ALREADY_EXISTS.format(name)}, 400

        store_data = store_schema.load(store_json)
        store_data.save_to_db()

        return store_schema.dump(store_data), 201
