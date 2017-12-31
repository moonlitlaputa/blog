from flask import Blueprint
from flask_restful import Api

from .token import Token
from .permission import (PostPermission,
                         CommentPermission,
                         UserPermission)
from .password import Password
from .auth import (SendEmailAuth,
                   EmailExist,
                   EmailAuth,
                   UsernameExist)


api_auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(api_auth)

api.add_resource(Token, '/token/')
api.add_resource(EmailAuth, '/email_auth/<token>/',
                 endpoint='email_auth')
api.add_resource(PostPermission, '/post_permission/',
                 endpoint='post_permission')
api.add_resource(CommentPermission, '/comment_permission',
                 endpoint='comment_permission')
api.add_resource(UserPermission, '/user_permission',
                 endpoint='user_permission')
api.add_resource(SendEmailAuth, '/send_email_auth/',
                 endpoint='send_email_auth')
api.add_resource(Password, '/password/')
api.add_resource(EmailExist, '/email_exist/',
                 endpoint='email_exist')
api.add_resource(UsernameExist, '/username_exist/',
                 endpoint='username_exist')
