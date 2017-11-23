# https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
# https://bytefish.de/blog/first_steps_with_sqlalchemy/
from pprint import pprint


import os
if os.path.exists('userdata.sqlite'):
    os.remove('userdata.sqlite') # not necessarily, just for testing

from sqlalchemy import create_engine
engine = create_engine('sqlite:///userdata.sqlite') # sql name can not contain any _ stuff, or exception be raised


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    password = Column(String)

    def __repr__(self):
        return "<User(id='%s', password='%s')>" %(self.id, self.password)


Base.metadata.create_all(engine) # when you build a new sql class like User, you have to init it using this command


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine) # we do everything by session
session = Session()

a_user = User(id="yingshaoxo", password="hi") # define a new user
session.add(a_user) # add that user to session
session.commit() # every time you made change, you have to commit to make it avaliabel on sql file.

some_one = session.query(User).filter_by(id='yingshaoxo').one() # how to find our user by id 
pprint(some_one)
print(some_one.id, some_one.password) # get user's info
exit()


pprint(dir(session)) # look how many commands you can use from session
pprint(dir(session.query(User))) # look how many commands you can use from query
