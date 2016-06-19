import os

basedir = os.path.abspath(os.path.dirname(__file__))

DB_USERNAME = 'dev'
DB_PWD = ''
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pwd}@localhost:3306/yet_another_party?charset=utf8'.format(user=DB_USERNAME, pwd=DB_PWD)
SESSION_TYPE = 'redis'
SQLALCHEMY_TRACK_MODIFICATIONS = False


#redis
EXPIRE = 200

BOOKING_URL = "http://leclick.myterranet.com/booking/add/restaurantId/{rest_id}/creator/partner/partner/telegramBot/params/?date={date}&time={time}&persons={persons}&wishes={wishes}&firstName={firstName}&lastName={lastName}&email={email}&fullPhone={phone}"
