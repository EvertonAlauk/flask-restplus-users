#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, uuid
from models import Post, User
from db import session

from flask_restplus import (
    Namespace,
    Resource,
    fields,
    reqparse,
    abort,
    marshal_with
)

api = Namespace('posts', description='Operacoes relacionadas as postagens')

post = {
    'id': fields.String(required=True, description='Identificador'),
    'user': fields.String(required=True, description='Usuario'),
    'post': fields.String(required=True, description='Postagem'),
}

parser = reqparse.RequestParser()
parser.add_argument('user', type=str)
parser.add_argument('post', type=str)


@api.route('/<uuid:id>')
@api.param('id', 'Identificador')
@api.response(404, 'Postagem nao encontrada')
class PostAPI(Resource):
    @marshal_with(post)
    def get(self, id):
        post = session.query(Post).filter(Post.id == id).first()
        if not post:
            abort(404, message="Postagem {} nao encontrada".format(id))
        return post

    def delete(self, id):
        post = session.query(Post).filter(Post.id == id).first()
        if not post:
            abort(404, message="Postagem {} nao encontrada".format(id))
        session.delete(post)
        session.commit()
        return {}, 204

    @marshal_with(post)
    def put(self, id):
        parsed_args = parser.parse_args()
        post = session.query(Post).filter(Post.id == id).first()
        if not post:
            abort(404, message="Postagem {} nao encontrada".format(id))
        post.post = parsed_args['post']
        session.add(post)
        session.commit()
        return post, 200

@api.route('/')
class PostListAPI(Resource):
    @marshal_with(post)
    def get(self):
        return session.query(Post).all()

    @marshal_with(post)
    def post(self):
        parsed_args = parser.parse_args()
        try:
            user = session.query(User).filter(User.id==parsed_args['user']).first()
        except:
            abort(404, message="Usuario nao encontrado")
        post = Post(
            id=uuid.uuid4(),
            user=user.id,
            post=parsed_args['post']
        )
        session.add(post)
        session.commit()
        return post, 200