#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DB_URI

Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DB_URI))
session = scoped_session(Session)