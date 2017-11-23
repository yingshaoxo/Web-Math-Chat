# https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
# https://bytefish.de/blog/first_steps_with_sqlalchemy/
from pprint import pprint
import os

from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///{dir}/userdata.sqlite'.format(dir=os.path.abspath(os.path.dirname(__file__)))) # sql name can not contain any _ stuff, or exception be raised
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    password = Column(String)
    token = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_loggin = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User(id='%s', password='%s')>" %(self.id, self.password)

Base.metadata.create_all(engine) # when you build a new sql class like User, you have to init it using this command


class MySession():
    Session = sessionmaker(bind=engine) # we do everything by session
    s = Session()
    
    def query(self):
        return self.s.query(User)

    def get_all(self):
        return self.query().all()

    def find_one(self, *args, **kwargs):
        if kwargs != dict():
            q = self.query().filter_by(**kwargs)
            if q.count() == 0:
                return None
            else:
                return q.one()
        if args != tuple() and len(args) == 1:
            q = self.query().filter_by(id=args[0])
            if q.count() == 0:
                return None
            else:
                return q.one()

    def add(self, id, password):
        user = User(id=id, password=password)
        self.s.add(user)

    def delete(self, id):
        user = self.find_one(id) 
        self.s.delete(user)

    def commit(self):
        self.s.commit()

    

# a_user = User(id="yingshaoxo", password="hi") # define a new user
# session.add(a_user) # add that user to session
# session.commit() # every time you made change, you have to commit to make it avaliabel on sql file.
# 
# some_one = session.query(User).filter_by(id='yingshaoxo').one() # how to find our user by id 
# pprint(some_one)
# print(some_one.id, some_one.password) # get user's info

# session.query(User).filter(User.created_time < datetime.utcnow().date()).all() # Get all users created yesterday
# exit()


# pprint(dir(session)) # look how many commands you can use from session
# pprint(dir(session.query(User))) # look how many commands you can use from query
