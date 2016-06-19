# -*- coding: utf-8 -*
import re
import requests
from requests.exceptions import HTTPError

import app
from app.config import BOOKING_URL
from app.models import UserCreatedTextMapper, SearchCriteria, QuickSearch, \
    RestInfo
from app import db


def get_restaurants(**kwargs):
    """
    Main function - returns list of restaurants according to user preferences
    :param user_id: integer, user's facebook id
    :param kwargs: user preferences in key-value manner
    :return: list of restaurants, which satisfied user preferences
    """
    search_criteria_values = get_search_criteria_values(**kwargs)
    if search_criteria_values:
        rest_ids = get_rest_ids_by_search_criteria(**search_criteria_values)
        if rest_ids:
            return get_rest_info_by_rest_id(rest_ids)

    print 'There was nothing found'
    return []


def get_search_criteria_values(**kwargs):
    """
    Returns search criteria values for users preferences
    :param kwargs: key-value user preferences, like: {"city": u"Moscow"}
    :return: dict, like {"city": 1}
    """
    result = {}
    for item in kwargs.items():
        search_criteria = SearchCriteria.query.filter_by(text=item[0]).first()
        if search_criteria:
            uctm = UserCreatedTextMapper.query.filter_by(
                user_text=item[1],
                search_criteria=search_criteria.id).first()
            if uctm:
                result[item[0]] = uctm.search_criteria_value
            else:
                return None
        else:
            raise Exception('Wrong search criteria: {}'.format(search_criteria))
    return result


def get_rest_ids_by_search_criteria(**kwargs):
    """
    Returns restaurants' ids for specified criterias
    :param query_ids: key-value user preferences, translated in
    DB-understandable language
    :return: list of restaurants ids
    """

    rest_ids = db.session.query(QuickSearch.id_rest).filter_by(
        **kwargs).distinct()
    return [r[0] for r in rest_ids]


def get_rest_info_by_rest_id(rest_ids):
    """
    Returns list of RestInfo objects
    :param rest_ids: list of rest_ids
    :return: list of RestInfo objects
    """
    rests = RestInfo.query.filter(RestInfo.id.in_(rest_ids)).all()
    print "Rests: {}".format(rests)
    return rests


def book_a_table(rest_id, date, time, persons, firstName, lastName, email,
                 phone, wishes='No'):
    """
    Books a table via leclick.ru get-request
    :param rest_id: integer - id of the restaurant
    :param date:  timestamp of booking date
    :param time:  timestamp of booking time (might be the same as date)
    :param persons: integer - number of persons
    :param firstName: string - person's name
    :param lastName: string - persons's last_name
    :param email: string - person's email
    :param phone: string - persons's phone (not in a strict format)
    :param wishes: string - person's special wishes for the booking
    :return: tuple (success, booking_id) -
    """
    url = BOOKING_URL.format(rest_id=rest_id, date=date, time=time,
                             persons=persons, firstName=firstName,
                             lastName=lastName, email=email, phone=phone,
                             wishes=wishes)

    try:
        response = requests.get(url)
        data = response.text
        if response.status_code == 200:
            if 'success' in data:
                error_text = re.search(r'"id":"(\d+)","', data)
                if error_text.groups():
                    print 'Success: {}'.format(error_text.group(1))
                    return False, error_text.group(1)
            elif 'error' in data:
                error_text = re.search(r'"message":"(.*)","', data)
                if error_text.groups():
                    print 'Error: {}'.format(error_text.group(1))
                    return False, error_text.group(1)

    except HTTPError as err:
        app.logger.error('HttpError while booking: {}'.format(err))


