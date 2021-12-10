from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, UserDetails, UserAuth, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from database import db
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = "JWT_secret_key"
app.config['JWT_BLACKLIST_ENABLE'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = 'secret key'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

#  user black listing
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    app.logger.info("usr blacklisted ")
    app.logger.info(jwt_payload)
    id_iam_looking_for = jwt_payload['jti']
    return id_iam_looking_for in BLACKLIST


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token expired'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': "You do not have privileges to view",
        'error': 'authorization required'
    }), 401

# user logout

# Custom error message. use belows
# @jwt.invalid_token_loader
#
# @jwt.needs_fresh_token_loader
#
# @jwt.unauthorized_loader
#
# @jwt.revoked_token_loader

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserDetails, '/user/<string:name>')
api.add_resource(UserRegister, '/singup')
api.add_resource(UserAuth, '/auth')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
