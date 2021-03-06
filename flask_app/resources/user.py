from extensions import jwt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restplus import Namespace, Resource
from models.user import UserModel

api = Namespace('User', description='Log in or sign up')



@api.route("auth")
class UserLogIn(Resource):

    parser = api.parser()
    parser.add_argument("username", default='mark_newman', required=True)
    parser.add_argument("password", default='code*3', required=True)


    @api.doc(security=None, responses={200:'OK', 401: 'No authorization'})
    @api.expect(parser)
    def post(self):
        data = UserLogIn.parser.parse_args()
    
        user = UserModel.find_user_by_username(data['username'])
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.username)
            print(access_token)
            return {"messgae": "Welcome", "access_token":access_token, "tip": "copy the access_token, click on Authorize button on the top, then input 'BEARER <your_token>' as your JWT value." }, 200

        else:
            return {"message": "Bad username and/or password"}, 401
        


@api.route("register")
@api.hide
class UserRegister(Resource):

    parser = api.parser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)


    @api.doc(security=None, responses={201:'Created', 400: 'Bad request: item already exsits'})
    @api.expect(parser)
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_user_by_username(data['username']):
            return {"message": "User already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
