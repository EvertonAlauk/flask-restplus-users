#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, uuid
from models import User
from db import session

from flask_restplus import (
    Namespace,
    Resource,
    fields,
    reqparse,
    abort,
    marshal_with
)

api = Namespace('users', description='Operacoes relacionadas aos usuarios')

user = {
    'id': fields.Integer(required=True, description='Identificador'),
    'first_name': fields.String(required=True, description='Primeiro nome'),
    'email': fields.String(required=True, description='Email'),
}

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str)
parser.add_argument('email', type=str)

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
        user.first_name = parsed_args['first_name']
        user.email = parsed_args['email']
        session.add(user)
        session.commit()
        return user, 200

@api.route('/')
class UserListAPI(Resource):
    @marshal_with(user)
    def get(self):
        return session.query(User).all()

    @marshal_with(user)
    def post(self):
        parsed_args = parser.parse_args()
        user = session.query(User).filter(User.email==parsed_args['email']).first()
        if user:
            abort(404, message="Usuario ja cadastrado com o e-mail: {}".format(user.email))
        user = User(id=uuid.uuid4(), first_name=parsed_args['first_name'], email=parsed_args['email'])
        session.add(user)
        session.commit()
        return user, 200