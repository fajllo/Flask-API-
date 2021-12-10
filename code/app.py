from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager


from resources.user import UserRegister, UserDetails, UserAuth, TokenRefresh
from resources.item import Item, ItemList
from database import db
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = "JWT_secret_key"
app.secret_key = 'secret key'

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserDetails, '/user/<string:name>')
api.add_resource(UserRegister, '/singup')
api.add_resource(UserAuth, '/auth')
api.add_resource(TokenRefresh,'/refresh')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)