# coding=utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import csv
from app import app, db
from flask import Flask, session

from app.helpers import get_search_criteria_values
from app.models import UserCreatedTextMapper, SearchCriteria, \
    SearchCriteriaValue

__author__ = 'arseniy.fomchenko'

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def populate_db_from_google_docs(filename):

    with open(filename, 'rb') as csvfile:
        search_criteria = filename.split('.')

        search_criteria_id = SearchCriteria.query.filter_by(
            text=search_criteria[0]).first()

        spamreader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(spamreader):
            if i == 0:
                continue
            print ', '.join(row)
            import pdb
            pdb.set_trace()

            search_criteria_value_id = SearchCriteriaValue.query.filter_by(
                text=row[1].decode('utf-8')).first()
            uctm = UserCreatedTextMapper(search_criteria=search_criteria_id.id,
                                         text=row[0].decode('utf-8'),
                                         search_criteria_value=search_criteria_value_id
                                         )
            db.session.add(uctm)
            db.session.commit()


@manager.command
def test():
    result = get_search_criteria_values(city=u'Маfсква')

if __name__ == "__main__":
    manager.run()