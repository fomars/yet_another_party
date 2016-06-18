def get_restaurants(user_id, city, **kwargs):
    """
    Main function - returns list of restaurants according to user preferences
    :param user_id: integer, user's facebook id
    :param city: string
    :param kwargs: user preferences in key-value manner
    :return: list (up to 5) of restaurants, which satisfied user preferences
    """
    pass


def get_query_ids(**kwargs):
    """
    Returns query ids for users preferences
    :param kwargs: key-value user preferences
    :return: dict, like {key_name: query_id}
    """
    pass


def get_rest_ids_by_query_ids(**query_ids):
    """
    Returns restaurants' ids for specified criterias
    :param query_ids: key-value user preferences, translated in
    DB-understandable language
    :return: list (up to 5 elements) of restaurants ids
    """
    pass
    # get query_id by text 
    rest_id = 1
    return rest_id


def return_rest_info_by_rest_id(rest_id):
    """
    Returns rest_info for specified rest_id
    :param rest_id: id of the restaurant
    :return: dict with restaurant info
    """
    pass






#  settings  


def set_user_city(user_id, city):
    """

    :param user_id:
    :param city:
    :return:
    """
    pass


def get_user_city(user_id):
    pass
    return '' or None