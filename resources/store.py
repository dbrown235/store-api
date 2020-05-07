from flask_restful import Resource
from models.store import StoreModel

class Store(Resource): #extending the Resource methods
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with the name {} already exists'.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'An error occurred when attempting to save the store'}, 500
        return store.json()

    def delete(self,name):
        if StoreModel.find_by_name(name):
            store = StoreModel(name)
            try:
                store.delete_from_db()
            except:
                {'message': 'An error occured deleting the store from the database'}
            return {'message': 'Store {} has been deleted from the database'.format(name)}
        return {'message': 'Store {} does not exist'.format(name)}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json for store in StoreModel.query.all()]}
        # list(map(lambda x: x.json(),StoreModel.query.all()))