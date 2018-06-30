from flask import Flask
from flask_restful import Resource,reqparse
from flask_jwt_extended import fresh_jwt_required, jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
               type=float,
               required=True,
               help="This field can't be left blank"
        ) 
    
    parser.add_argument('store_id',
               type=int,
               required=True,
               help="Every item needs a store id"
        )                                            

    @jwt_required
    def get(self, name):
       item = ItemModel.find_by_name(name)
       if item:
           return item.json()
       return {"message": "item not found"},404
        # for item in items:0
        #     # if item['name']==name:
        #     #     return item
        #             or 
        # item = next(filter(lambda x: x['name'] == name, items), None) # if next fun doesn't find any item, it returns none 
        # return {'item': item}, 200 if item else 204

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}'already exists.".format(name)}, 404

        data = self.parser.parse_args()  # load data.

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return item.json(), 201


    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is admin']:
            return {'message': 'Admin privilege required'},401
            
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found' }
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))#our item list is a list result of filtering on lambda where name is not equal to the name,that was passed in.


    def put(self,name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if item is None: # Doubttttttttt
            item.price = data['price']
        else:
            item = ItemModel(name, **data)   
            

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [items.json() for items in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {'items': [item['name'] for item in ItemModel],
                'message': 'More data available if you log in.'}, 200
        
    #return {"item": [x.json() for x in ItemModel.query.all()]} # set comprehension
        