from app.models import UserCreatedTextMapper, SearchCriteria


def get_restaurants(**kwargs):
    """
    Main function - returns list of restaurants according to user preferences
    :param user_id: integer, user's facebook id
    :param kwargs: user preferences in key-value manner
    :return: list of restaurants, which satisfied user preferences
    """
    result = []
    search_criteria_values = get_search_criteria_values(**kwargs)
    if search_criteria_values:
        rest_ids = get_rest_ids_by_search_criteria(search_criteria_values)
        if rest_ids:
            for id in rest_ids:
                result.append(get_rest_info_by_rest_id(id))

    return result


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
                text=item[1],
                search_criteria=search_criteria.id).first()
            if uctm:
                result[item[0]] = uctm.search_criteria_value
            else:
                # situation, when we can't find search_criteria_value_id for
                # the specified user query in UserCreatedTextMapper
                # we return 0, to signalize, that we didn't search anything
                return None

        else:
            raise Exception('Wrong search criteria: {}'.format(search_criteria))
    return result


def get_rest_ids_by_search_criteria(**query_ids):
    """
    Returns restaurants' ids for specified criterias
    :param query_ids: key-value user preferences, translated in
    DB-understandable language
    :return: list (up to 5 elements) of restaurants ids
    """

    rest_id = 1
    return rest_id


def get_rest_info_by_rest_id(rest_id):
    """
    Returns rest_info for specified rest_id
    :param rest_id: id of the restaurant
    :return: dict with restaurant info
    """
    pass
