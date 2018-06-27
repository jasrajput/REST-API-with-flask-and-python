from flask import Flask
from flask_restful import Api #reqparse- designed to provide simple and uniform access to any variable 
from flask_jwt import JWT
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'jas'
api = Api(app)

jwt = JWT(app, authenticate, identity) 
# jwt creates a new endpoint(/auth).when we call auth
# we send it username and password and then jwt extens. takes the username and password and 
# send it to the authenticate function

api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>') #http:127.0.0.1.5000/item/item_name
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

