from .abstract import *
from .. import schema

class Client(ListableAPIResource, MutableAPIResource):
    _GET_FN    = 'get_client'
    _LIST_FN   = 'list_clients'
    _SEARCH_FN = 'search_clients'
    _UPDATE_FN = 'update_client'
    _DELETE_FN = 'delete_client'

    __field_names__ = schema.Client.__field_names__
