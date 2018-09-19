# coding=utf-8
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

# 创建对象基类
Base = declarative_base()

# 初始化数据库连接
engine = create_engine('sqlite:///catalog.db')

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32))
    description = Column(String(256), index=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'cat_id': self.category_id,
            'description': self.description,
            'id': self.id,
            'title': self.title
        }




# 提交全部修改
Base.metadata.create_all(engine)