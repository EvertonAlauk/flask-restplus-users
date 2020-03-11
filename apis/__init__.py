# -*- coding: utf-8 -*-

from flask_restplus import Api

from .users import api as users

api = Api(title='API REST', version='1.0', description='Lista de APIS')

api.add_namespace(users)