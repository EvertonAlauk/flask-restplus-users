#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string

RESTPLUS_VALIDATE = True
DEBUG = True
SECRET_KEY = "".join(random.choice((string.ascii_letters + string.digits + string.ascii_uppercase)) for i in range(12))
DB_URI = 'postgresql://alaukdev:dev2020@localhost:5432/flaskdb'
