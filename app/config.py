import os

basedir = os.path.abspath(os.path.dirname(__file__))

DB_USERNAME = ''
DB_PWD = ''
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pwd}@localhost:3306/yet_another_party'.format(user=DB_USERNAME, pwd=DB_PWD)
