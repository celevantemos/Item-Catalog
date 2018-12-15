from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# A User table with their very basic information
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    provider = Column(String(250))


# Category table with a Foreign key with the main user created them
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
         'id': self.id,
         'name': self.name
        }


# Items table that connects with the category and a user
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(1024), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, backref='items')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
         'cat_id': self.category_id,
         'description': self.description,
         'id': self.id,
         'title': self.name,
        }


engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.create_all(engine)
