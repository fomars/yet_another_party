import os

basedir = os.path.abspath(os.path.dirname(__file__))

DB_USERNAME = 'dev'
DB_PWD = ''
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pwd}@localhost:3306/yet_another_party?charset=utf8'.format(user=DB_USERNAME, pwd=DB_PWD)
SESSION_TYPE = 'redis'
SQLALCHEMY_TRACK_MODIFICATIONS = False
