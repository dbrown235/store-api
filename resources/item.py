
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#every resource has to be a class - RESTful returns a dictionary and auto jsonifies
class Item(Resource):
    parser = reqparse.RequestParser ()  # create new parser object
    # only allow price to come through in body of json
    parser.add_argument ( 'price',
                          type = float,
                          required = True,
                          help = "This field cannot be left blank!" )
    parser.add_argument ( 'store_id',
                          type = int,
                          required = True,
                          help = "Every store needs a store id" )


    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'This item does not exist'}


    def post(self, name):
        #check if item already exist in the system, if so return error
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exist".format(name)}, 400 #bad request
        data = Item.parser.parse_args ()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201 #201 is for created 202 accepted



    def put(self,name):
        data = Item.parser.parse_args ()
        #data = request.get_json() #get all json sent in body
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'],data['store_id'])  # or **data
        else:
            item.price(data['price'])

        item.save_to_db()
        return item.json()

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'Item has been deleted'}
        return {'message':'The item is not found'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # alternate list(map(lambda x: x.json(), ItemModel.query.all()))
        #{'items': [item.json]}