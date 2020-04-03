#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt

from flask import request
from flask import jsonify
from flask_restplus import abort
from functools import wraps
from config import SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            abort(404, message="Token is missing!")
        try:
            data = jwt.decode(token, SECRET_KEY)
        except:
            abort(404, message="Token is invalid!")
        return f(*args, **kwargs)
    return decorated