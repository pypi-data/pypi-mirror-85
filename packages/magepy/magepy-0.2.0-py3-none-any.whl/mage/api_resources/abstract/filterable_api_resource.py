from .util import to_camel_case

"""
MAGE supports two separate sets of queries depending on where
the data is coming from.

Common methods:
    eq, ne, gt, lt, ge (list)/gte (search), le (list)/lte (search), between (list)/range (search)

List methods:
    Supported:
        contains, not_contains, begins_with
    Not Currently Supported:
        attribute_exists, attribute_type, size

search methods:
    Supported:
        match, match_phrase, match_phrase_prefix, wildcard, regexp
    Not Currently Supported:
        multi_match, exists
"""

class FilterBase:
    """
    This class contains the common filters shared between list and search.  Actions default to list.
    """

    def __init__(self, cls=None, **params):
        self._cls = cls
        self._params = params

    def __repr__(self):
        return 'BaseFilter(%s)' % (self._params)

    def __getattr__(self, name):
        if name not in ['list', 'search']:
            raise AttributeError("%r object has no attribute %r" %
                             (self.__class__.__name__, name))

        attr =  getattr(self._cls, name)
        _params = self._params
        if callable(attr):
            def hook(**params):
                nonlocal attr
                nonlocal _params
                return attr(**_params, **params)
            return hook
        return attr


    @classmethod
    def normalize_list_filters(cls, params):
        if 'filter' in params:
            for key in list(params['filter']):
                for mode in list(params['filter'][key]):
                    if mode == 'lte':
                        params['filter'][key]['le'] = params['filter'][key][mode]
                    elif mode == 'gte':
                        params['filter'][key]['ge'] = params['filter'][key][mode]
                    elif mode == 'range':
                        params['filter'][key]['between'] = params['filter'][key][mode]
        if 'select' in params:
            for key in list(params['select']):
                if params['select'][key]:
                    normalize_list_filters(cls, params['select'][key]._params)

    @classmethod
    def normalize_search_filters(cls, params):
        if 'filter' in params:
            for key in list(params['filter']):
                for mode in list(params['filter'][key]):
                    if mode == 'between':
                        params['filter'][key]['range'] = params['filter'][key][mode]
        if 'select' in params:
            for key in list(params['select']):
                if params['select'][key]:
                    normalize_search_filters(cls, params['select'][key]._params)

    def _filter(self, mode, **kwargs):
        f = self._params.get('filter', {})
        for key in kwargs:
            if key in f:
                f[key][mode] = kwargs[key]
            else:
                f[key] = {mode: kwargs[key]}
        self._params['filter'] = f
        return self

    def eq(self, **kwargs):
        """
        Filters on equalty.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.eq(name='My Test')[0]
        """
        return self._filter('eq', **kwargs)

    def ne(self, **kwargs):
        """
        Filters on unequalty.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.ne(name='My Test')
        """
        return self._filter('ne', **kwargs)

    def lt(self, **kwargs):
        """
        Filters less than a value.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.AssessmentRun.lt(score=60))
        """
        return self._filter('lt', **kwargs)

    def lte(self, **kwargs):
        """
        Filters less than or equal to a value.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.AssessmentRun.lte(score=60))
        """
        return self._filter('lte', **kwargs)

    def gt(self, **kwargs):
        """
        Filters greater than a value.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.AssessmentRun.gt(score=60))
        """
        return self._filter('gt', **kwargs)

    def gte(self, **kwargs):
        """
        Filters greater than or equal to a value.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.AssessmentRun.gte(score=60))
        """
        return self._filter('gte', **kwargs)

    def limit(self, count):
        """
        Limits the results returned from the query to a maximum number of records.

        Args:
            count (int):  Max number of results to return

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.Finding.limit(10))
        """
        self._params['limit'] = count
        return self

    def select(self, *params, **kwparams):
        """
        Select specific fields to return from the query.

        Args:
            *params: array of strings
            **kwparams: Filter instances to select nested fields

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRun.select('id', 'score').last()[0]
        """

        s = self._params.get('select', {})
        for p in params:
            if isinstance(p, list) or isinstance(p, tuple):
                for i in p:
                    if i not in s:
                        s[i] = None
            elif isinstance(p, str):
                if p not in s:
                    s[p] = None
            else:
                raise RuntimeError("Unsupported type", type(p))
        for p in kwparams:
            if isinstance(kwparams[p], Filter):
                s[p] = kwparams[p]
            else:
                raise RuntimeError("Unsupported type", type(p))

        self._params['select'] = s
        return self

    def range(self, **kwargs):
        """
        Filter by a range of values.  Alias for `between`.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.AssessmentRun.range(score=[60, 70]))
        """
        return self._filter('range', **kwargs)

    def between(self, **kwargs):
        """
        Filter by a range of values.  Alias for `range`.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.AssessmentRun.between(score=[60, 70]))
        """
        return self._filter('between', **kwargs)


class ListFilter(FilterBase):
    def __iter__(self):
        """Refer to `ListObject.__iter__`."""
        return self.list().__iter__()

    def auto_paging_iter(self):
        """Refer to `ListObject.auto_paging_iter`."""
        return self.list().auto_paging_iter()

    def __getitem__(self, item):
        """Refer to `ListObject.__getitem__`."""
        result = self.list()
        return result[item]

    def __len__(self):
        """Refer to `ListObject.__len__`."""
        return self.list().__len__()

    def __repr__(self):
        return 'ListFilter(%s)' % (self._params)

    def _to_listfilter(self):
        """Converts a `Filter` instance to a `ListFilter`."""
        if isinstance(self, Filter):
            return ListFilter(self._cls, **self._params)
        return self

    def contains(self, **kwargs):
        """
        Reference https://docs.amazonaws.cn/en_us/amazondynamodb/latest/developerguide/LegacyConditionalParameters.Conditions.html.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.Assessment.contains(name='web'))
        """
        return self._to_listfilter()._filter('contains', **kwargs)

    def not_contains(self, **kwargs):
        """
        Reference https://docs.amazonaws.cn/en_us/amazondynamodb/latest/developerguide/LegacyConditionalParameters.Conditions.html.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.Assessment.not_contains(name='database'))
        """
        return self._to_listfilter()._filter('not_contains', **kwargs)

    def begins_with(self, **kwargs):
        """
        Filters based on the start of a string.

        Reference https://docs.amazonaws.cn/en_us/amazondynamodb/latest/developerguide/LegacyConditionalParameters.Conditions.html.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.Asset.begins_with(asset_identifier='www.'))
        """
        return self._to_listfilter()._filter('begins_with', **kwargs)


class SearchFilter(FilterBase):
    def __iter__(self):
        """Refer to `ListObject.__iter__`."""
        return self.search().__iter__()

    def auto_paging_iter(self):
        """Refer to `ListObject.auto_paging_iter`."""
        return self.search().auto_paging_iter()

    def __getitem__(self, item):
        """Refer to `ListObject.__getitem__`."""
        result = self.search()
        return result[item]

    def __len__(self):
        """Refer to `ListObject.__len__`."""
        return self.search().__len__()

    def __repr__(self):
        return 'SearchFilter(%s)' % (self._params)

    def _to_searchfilter(self):
        """Converts a `Filter` instance to a `SearchFilter`."""
        if isinstance(self, Filter):
            return SearchFilter(self._cls, **self._params)
        return self


    def match(self, **kwargs):
        """
        Filters case insensitive text.

        Reference https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.match(name='web')

        """
        return self._to_searchfilter()._filter('match', **kwargs)


    def match_phrase(self, **kwargs):
        """
        Reference https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query-phrase.html.
        """
        return self._to_searchfilter()._filter('match_phrase', **kwargs)


    def match_phrase_prefix(self, **kwargs):
        """
        Reference https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query-phrase-prefix.html.
        """
        return self._to_searchfilter()._filter('match_phrase_prefix', **kwargs)


    def wildcard(self, **kwargs):
        """
        Filters with single (?) or multiple (*) wildcards, matching single words.  Use lowercase text.

        Reference https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-wildcard-query.html.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.Asset.regexp(asset_identifier='*.example.com').select('asset_identifier'))
        """
        return self._to_searchfilter()._filter('wildcard', **kwargs)


    def regexp(self, **kwargs):
        """
        Filters results with regular expressions.  Attempting to match across spaces won't work because the expression is tested word by word.

        Reference https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-regexp-query.html

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.Asset.regexp(asset_identifier='.*.example.com').select('asset_identifier'))
        """

        return self._to_searchfilter()._filter('regexp', **kwargs)


    def sort(self, field=None):
        """
        Sorts ascending.

        Args:
            field (str, optional): Field to sort on

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRun.sort().search()
        """

        item = self._to_searchfilter()
        if not item._cls:
            item._params['sort_direction'] = 'ASC'
        else:
            field = field or getattr(item._cls,'_SORT_FIELD',None) or 'created_at'
            item._params['sort'] = {
                'direction': 'asc',
                'field': to_camel_case(field)
            }
        return item


    def sort_desc(self, field=None):
        """
        Sorts descending.

        Args:
            field (str, optional): Field to sort on

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRun.sort_desc().search()
        """

        item = self._to_searchfilter()
        if not item._cls:
            item._params['sort_direction'] = 'DESC'
        else:
            field = field or getattr(item._cls,'_SORT_FIELD',None) or 'created_at'
            item._params['sort'] = {
                'direction': 'desc',
                'field': to_camel_case(field)
            }
        return item


    def first(self, count=1, field=None):
        """
        Sorts ascending and limits the results.

        Args:
            count (int, optional): Maximum number of records to return
            field (str, optional): Field to sort on

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRun.first(10).search()
        """

        return self.sort(field).limit(count)


    def last(self, count=1, field=None):
        """
        Sorts descending and limits the results.

        Args:
            count (int, optional): Maximum number of records to return
            field (str, optional): Field to sort on

        Example:
            >>> import mage
            >>> mage.connect()
            >>> list(mage.AssessmentRun.last(10))
        """

        return self.sort_desc(field).limit(count)


class Filter(ListFilter, SearchFilter):
    """
    This class is the generic filter class.  Choosing certain methods
    like `SearchFilter.sort` limits future method calls to `SearchFilter` while other
    calls like `ListFilter.contains` limits to `ListFilter`.
    """

    def __repr__(self):
        return 'Filter(%s)' % (self._params)


    def __iter__(self):
        """
        Iterating on a Filter is shorthand for calling search or list and
        iterating on the results.  These two are equivalent:

        >>> for finding in mage.Finding.last(10):

        >>> for finding in mage.Finding.last(10).search():
        """
        try:
            return self.list().__iter__()
        except NotImplementedError:
            return self.search().__iter__()


    def auto_paging_iter(self):
        """Refer to `ListObject.auto_paging_iter`."""
        try:
            return self.list().auto_paging_iter()
        except NotImplementedError:
            return self.search().auto_paging_iter()


    def __len__(self):
        """
        Finding the length of a Filter is shorthand for calling search or list and
        finding the length of the result.  These two are equivalent:

        >>> len(mage.Finding.match(title='http'))

        >>> len(mage.Finding.match(title='http').search())
        """
        try:
            return self.list().__len__()
        except NotImplementedError:
            return self.search().__len__()


    def __getitem__(self, item):
        """
        Getting an item from a Filter is shorthand for calling search or list and
        getting an item from the result.  These two are equivalent:

        >>> mage.Finding.last()[0]

        >>> mage.Finding.last().search()[0]
        """
        try:
            result = self.list()
        except NotImplementedError:
            result = self.search()
        return result[item]


class FilterableAPIResource():
    """Inherit this class to provide filtering on queries."""

    #####  FilterBase methods
    @classmethod
    def eq(cls, **kwargs):
        """Refer to `FilterBase.eq`."""
        return Filter(cls).eq(**kwargs)

    @classmethod
    def ne(cls, **kwargs):
        """Refer to `FilterBase.ne`."""
        return Filter(cls).ne(**kwargs)

    @classmethod
    def lt(cls, **kwargs):
        """Refer to `FilterBase.lt`."""
        return Filter(cls).lt(**kwargs)

    @classmethod
    def lte(cls, **kwargs):
        """Refer to `FilterBase.lte`."""
        return Filter(cls).lte(**kwargs)

    @classmethod
    def gt(cls, **kwargs):
        """Refer to `FilterBase.gt`."""
        return Filter(cls).gt(**kwargs)

    @classmethod
    def gte(cls, **kwargs):
        """Refer to `FilterBase.gte`."""
        return Filter(cls).gte(**kwargs)

    @classmethod
    def limit(cls, count):
        """Refer to `FilterBase.limit`."""
        return Filter(cls).limit(count)

    @classmethod
    def select(cls, *params, **kwparams):
        """Refer to `FilterBase.select`."""
        return Filter(cls).select(*params, **kwparams)

    @classmethod
    def range(cls, **kwargs):
        """Refer to `FilterBase.range`.  Alias: `FilterBase.between`."""
        return Filter(cls).range(**kwargs)

    @classmethod
    def between(cls, **kwargs):
        """Refer to `FilterBase.between`.  Alias: `FilterBase.range`."""
        return Filter(cls).between(**kwargs)


    #####  SearchFilter methods
    @classmethod
    def sort(cls, field='created_at'):
        """Refer to `SearchFilter.sort`."""
        return Filter(cls).sort(field)

    @classmethod
    def sort_desc(cls, field='created_at'):
        """Refer to `SearchFilter.sort_desc`."""
        return Filter(cls).sort_desc(field)

    @classmethod
    def first(cls, count=1, field=None):
        """Refer to `SearchFilter.first`."""
        return Filter(cls).sort(field).limit(count)

    @classmethod
    def last(cls, count=1, field=None):
        """Refer to `SearchFilter.last`."""
        return Filter(cls).sort_desc(field).limit(count)

    @classmethod
    def match(cls, **kwargs):
        """Refer to `SearchFilter.match`."""
        return Filter(cls).match(**kwargs)

    @classmethod
    def match_phrase(cls, **kwargs):
        """Refer to `SearchFilter.match_phrase`."""
        return Filter(cls).match_phrase(**kwargs)

    @classmethod
    def match_phrase_prefix(cls, **kwargs):
        """Refer to `SearchFilter.match_phrase_prefix`."""
        return Filter(cls).match_phrase_prefix(**kwargs)

    @classmethod
    def wildcard(cls, **kwargs):
        """Refer to `SearchFilter.wildcard`."""
        return Filter(cls).wildcard(**kwargs)

    @classmethod
    def regexp(cls, **kwargs):
        """Refer to `SearchFilter.regexp`."""
        return Filter(cls).regexp(**kwargs)


    #####  ListFilter methods
    @classmethod
    def contains(cls, **kwargs):
        """Refer to `ListFilter.contains`."""
        return Filter(cls).contains(**kwargs)

    @classmethod
    def not_contains(cls, **kwargs):
        """Refer to `ListFilter.not_contains`."""
        return Filter(cls).not_contains(**kwargs)

    @classmethod
    def begins_with(cls, **kwargs):
        """Refer to `ListFilter.begins_with`."""
        return Filter(cls).begins_with(**kwargs)
