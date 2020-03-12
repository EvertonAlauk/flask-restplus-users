#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings import DB_URI

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    first_name = Column(String(255))
    email = Column(String(255))
    post = relationship("Post", cascade="all,delete")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    user = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    post = Column(String(255))

if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)