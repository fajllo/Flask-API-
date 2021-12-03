from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):

    # parser = reqparse.RequestParser()
    # parser.add_argument("name",
    #                     required=False,
    #                     type=float,
    #                     help="This field cannot be left blank!"
    #                     )


    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"An store with name '{name}' already exists."}

        # data = Store.parser.parse_args()

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message' : 'item deleted'}

        return {'message': 'no item to deleted'}




class StoreList(Resource):

    def get(self):
        return {"stores": [store.json() for store in StoreModel.finde_all()]}
