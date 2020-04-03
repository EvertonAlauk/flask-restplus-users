#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import uuid

from flask_restplus import Namespace
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import reqparse
from flask_restplus import abort
from flask_restplus import marshal_with
from werkzeug.security import generate_password_hash

from models import User
from db import session
from decorators import token_required

api = Namespace('users', description='Operacoes relacionadas aos usuarios')

user = {
    'id': fields.String(required=True, description='Identificador'),
    'username': fields.String(required=True, description='Primeiro nome'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Senha'),
}

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)

@api.route('/<uuid:id>')
@api.param('id', 'Identificador')
@api.response(404, 'Usuario nao encontrado')
class UserAPI(Resource):
    @marshal_with(user)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="Usuario {} nao encontrado".format(id))
        return user

    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="Usuario {} nao encontrado".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    @marshal_with(user)
    def put(self, id):
        parsed_args = parser.parse_args()
        user = session.query(User).filter(User.id == id).first()
        user.username = parsed_args['username']
        user.email = parsed_args['email']
        session.add(user)
        session.commit()
        return user, 200

@api.route('/')
class UserListAPI(Resource):
    @marshal_with(user)
    @token_required
    def get(self):
        print(session.query(User).all())
        return session.query(User).all()

    @marshal_with(user)
    def post(self):
        parsed_args = parser.parse_args()
        user = session.query(User).filter(User.email==parsed_args['email']).first()
        if user:
            abort(404, message="Usuario ja cadastrado com o e-mail: {}".format(user.email))
        user = User(id=uuid.uuid4(), username=parsed_args['username'], email=parsed_args['email'], password=generate_password_hash(parsed_args['password']))
        session.add(user)
        session.commit()
        return user, 200