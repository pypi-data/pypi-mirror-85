import json

from .data_api_resource import DataAPIResource
from .filterable_api_resource import FilterableAPIResource
from .filterable_api_resource import Filter
from .util import *
from ...schema import schema
from ... import logger
from sgqlc.operation import Operation


class ListObjectIterator:
    ''' Iterator class '''
    def __init__(self, lo):
        self._lo = lo   #: object reference
        self._index = 0 #: member variable to keep track of current index

    def __next__(self):
        """
        If `mage.auto_page` is set then this iterator
        becomes an auto paging iterator
        """
        from ... import auto_page

        while True:
            if not self._lo:
                raise StopIteration

            if self._index < len(self._lo):
                result = self._lo[self._index]
                self._index += 1
                return result

            if auto_page:
                self._lo = self._lo.next_page()
                self._index = 0
            else:
                raise StopIteration


class ListObject():
    """
    The ListObject class is a list-like container for results
    returned from the MAGE server.  It additionally tracks a
    'next_token' which enables it to retrieve additional results
    from the server as needed.
    """

    def __init__(self, cls, fn, params, items, next_token, subresult=[]):
        self.cls = cls #: the class of objects stored in the list
        self.fn = fn   #: the function used as the main query for more records
        self.data = items #: the data received from the server
        self.next_token = next_token #: the token to use for more results
        self._params = params       #: params used to generate the results
        self._subresult = subresult #: the field to use for a nested result

    def __iter__(self):
        return ListObjectIterator(self)

    def __len__(self):
        return getattr(self, 'data', []).__len__()

    def __getitem__(self, item):
        return self.cls.init(getattr(self, 'data', [])[item])

    def next_page(self):
        """
        Retrieves the next set of results from the server.
        """
        if self.next_token:
            logger.debug("Getting next page...")
            p = self._params
            for sr in self._subresult:
                if p['select'][sr] is None:
                    p['select'][sr] = Filter()
                p = p['select'][sr]._params

            p['next_token'] = self.next_token

            lo = self.cls._retrieve(self.fn, **self._params)
            if self._subresult:
                lo._subresult = self._subresult
                first = lo.data[0]
                lo.data = first
                for sr in self._subresult:
                    lo.next_token = lo.data[sr].next_token
                    lo.data = lo.data[sr].items
            return lo
        return None

    def auto_paging_iter(self):
        """
        Iterates through all results from the query, retrieving more
        from the server as needed.

        Yields:
            all results items.
        """
        page = self

        while page:
            for item in page:
                yield item

            page = page.next_page()


class ListableAPIResourceMeta(type):
    def __iter__(self):
        """
        Iterating on a ListableAPIResource is shorthand for calling search or
        list and iterating on the results.  This iterator will automatically
        fetch additional results from the server.  These two are equivalent:

        >>> for f in mage.Finding:

        >>> for f in mage.Finding.search().auto_paging_iter():
        """
        try:
            return self.list().auto_paging_iter()
        except NotImplementedError:
            return self.search().auto_paging_iter()


class ListableAPIResource(DataAPIResource, FilterableAPIResource, metaclass=ListableAPIResourceMeta):
    """
    This parent class provides functionality for retrieving data from the server.
    """

    @classmethod
    def _retrieve(cls, fn, **params):
        op = Operation(schema.Query)

        fields = dict(getattr(schema.Query, fn).args)
        for p in params:
            if p != 'select' and p not in fields:
                raise ValueError("%s does not support the '%s' parameter" % (fn, p))

        if 'filter' in dict(getattr(schema.Query, fn).args):
            filter_fields = dict(getattr(schema.Query, fn).args)['filter'].type.__field_names__
            for f in params.get('filter', {}):
                if f not in filter_fields:
                    raise ValueError("%s does not support filtering on '%s'." % (fn, f))

        update_subfields(op, fn, params, query=schema.Query)
        logger.debug(op.__to_graphql__(auto_select_depth=1))

        from mage import endpoint
        result = endpoint(op.__to_graphql__(auto_select_depth=1))
        #logger.debug(result)

        if 'errors' in result:
            for e in result['errors']:
                logger.error(e['message'])
        if 'data' in result and result['data']:
            data = getattr((op + result), fn)
            if getattr(schema.Query, fn).type == schema.AWSJSON:
                data = json.loads(data)
                items = data.get('items', [data])
            else:
                items = getattr(data, 'items', None)
                if items is None:
                    if hasattr(data, 'next_token'):
                        raise RuntimeError("'next_token' is present but 'items' is missing.")
                    else:
                        # usually results are like {'data': {'items': [something]}}
                        # but sometimes it is {'data': something}
                        # that case is covered here
                        items = [data]

            items = list(filter(None, items))
            next_token = getattr(data, 'next_token', None)
            if next_token:
                logger.debug("More data available")
            else:
                logger.debug("No More data")
            return ListObject(cls=cls, fn=fn, params=params, items=items, next_token=next_token)

    @classmethod
    def list(cls, **params):
        """
        Queries the server backend for data.

        Args:
            **params: Parameters to include in the query.  These are indirectly passed in via calls to 'select', 'contains', etc.

        Returns:
            `ListObject` of class instances

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.list()
        """
        fn = getattr(cls,'_LIST_FN',None)
        if not fn:
            raise NotImplementedError("%s does not support 'list'" % cls.__name__)

        Filter.normalize_list_filters(params)

        if 'limit' in params:
            return cls._retrieve_all(fn, **params)
        else:
            return cls._retrieve(fn, **params)

    @classmethod
    def search(cls, **params):
        """
        Queries the server backend that supports sorting and other useful features.

        Args:
            **params: Parameters to include in the query.  These are indirectly passed in via calls to 'sort', 'match', etc.

        Returns:
            `ListObject` of class instances

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Finding.search()
        """
        fn = getattr(cls,'_SEARCH_FN',None)
        if not fn:
            raise NotImplementedError("%s does not support 'search'" % cls.__name__)

        Filter.normalize_search_filters(params)

        if 'limit' in params:
            return cls._retrieve_all(fn, **params)
        else:
            return cls._retrieve(fn, **params)

    @classmethod
    def get(cls, id):
        """
        Gets a single result from the server for those classes that support it.

        Args:
            id (str): ID of the object to retrieve

        Returns:
            Object instance of the the class

        Results:
            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.get('12345')
        """

        fn = getattr(cls,'_GET_FN',None)
        if not fn:
            raise NotImplementedError("%s does not support 'get'" % cls.__name__)
        result = cls._retrieve_all(fn, id=id)
        if result and len(result) > 0:
            return result[0]
        return None


    @classmethod
    def _retrieve_all(cls, fn, **orig_params):
        """
        Retrieves all results from the server unless a limit is provided.
        Note that limits are handled in this method and not passed to the
        server because the server's backend doesn't handle it well.
        """
        items = []
        params = orig_params.copy()
        limit = params.pop('limit', 0)
        next_token = None

        while True:
            lo = cls._retrieve(fn, **params)
            if lo is None:
                break
            items += lo.data
            next_token = lo.next_token

            if next_token and (limit == 0 or len(items) < limit):
                params['next_token'] = next_token
                continue
            break

        if limit != 0:
            items = items[:limit]

        return ListObject(cls=cls, fn=fn, params=orig_params, items=items, next_token=None)
