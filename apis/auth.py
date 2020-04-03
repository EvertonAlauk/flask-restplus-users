#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt
import datetime

from flask import request, jsonify, make_response
from flask_restplus import Namespace
from flask_restplus import Resource
from werkzeug.security import check_password_hash

from db import session
from config import SECRET_KEY
from models import User

api = Namespace('auth', description='Operacoes relacionadas a autenticacao')

@api.route('/')
class AuthAPI(Resource):
    def get(self):
        auth = request.authorization
        if auth:
            user = session.query(User).filter(User.username == auth.username).first()
            if user and check_password_hash(user.password, auth.password):
                return jsonify({ "token": jwt.encode({ "user": auth.username }, SECRET_KEY).decode('UTF-8') })
        return make_response('Could verify!', 401, { 'WWW-Authenticate': 'Basic realm="Login Required"' })
