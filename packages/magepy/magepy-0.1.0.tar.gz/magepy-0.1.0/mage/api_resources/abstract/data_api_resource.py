class DataAPIResource(object):
    """
    This class manages the data object for subclasses.
    It redirects attribute requests to the data object if they are not
    found in the subclass.  In order to access an attribute in the data
    object that also exists in the subclass it must be explicitly
    referenced like self.data.attr instead of just self.attr.
    """

    @classmethod
    def init(cls, data):
        """
        This creates a new cls instance with data.

        Args:
            data: The data for this instance

        Returns:
            New class instance
        """
        self = cls.__new__(cls)
        self.data = data
        return self


    def __init__(self):
        """
        Classes that inherit from DataAPIResource must be instantiated with the init method.

        Raises: NotImplementedError
        """
        raise NotImplementedError


    def __getattr__(self, attr):
        """
        This redirects all unfound attribute queries to the data object.
        If the attribute is a field name that is not found locally then
        :meth:`refresh` is called to retrieve it.

        Args:
            attr (str): The attribute to get

        Returns:
            The attribute
        """

        if attr == '__field_names__':
            return object.__getattribute__(self, attr)

        if hasattr(self, '__field_names__') and attr in self.__field_names__ and attr not in self.data:
            self.refresh()

        return object.__getattribute__(self.data, attr)


    def __setattr__(self, attr, val):
        """
        This calls the class's update function which will update
        the object server-side and refresh the data object.
        """

        if attr == 'data':
            object.__setattr__(self, attr, val)
        else:
            self.update(**{attr:val})


    def __repr__(self):
        """
        When returning this class as a string, just return the data portion.

        Returns:
            The data member as a string
        """

        return '%s' % (self.data)


    def _nested_resource(self, newcls, name, select = None):
        if name not in self.data:
            if select:
                from .filterable_api_resource import Filter
                query = self.eq(id=self.id).select(**{name: Filter().select(select)}).limit(1)
            else:
                query = self.eq(id=self.id).select(name).limit(1)
            q = query[0]
            self.data[name] = q.data[name]
        return newcls.init(self.data[name])


    def _nested_resource_list(self, newcls, name, select = None):
        """
        """
        from .listable_api_resource import ListObject
        from .filterable_api_resource import Filter

        #BUG: this new query wipes out any sorting that may have been done previously (as an example)
        if select:
            query = self.eq(id=self.id).select(**{name: Filter().select(select)}).limit(1)
        else:
            query = self.eq(id=self.id).select(name).limit(1)

        # if there is no data then get it
        if not hasattr(self.data, name):
            setattr(self.data, name, getattr(query[0].data, name))

        return ListObject(cls=newcls, fn=self._SEARCH_FN, params=query._params, items=self.data[name].items, next_token=self.data[name].next_token, subresult=[name])


    def refresh(self, field = None):
        """
        Retrieve the object from the server.

        Args:
            field (str, optional): Name of the field to update.  (Default: update all fields)

        Returns:
            None
        """

        if not hasattr(self.data, 'id'):
            return

        a = self.eq(id=self.data.id)
        if field is None:
            if hasattr(self, '__field_names__'):
                fields = [name for name in self.__field_names__ if name != 'client']
                a = a.select(*fields)
            a = a.limit(1)[0]
            self.data = a.data
        else:
            a = a.select(field).limit(1)[0]
            self.data[field] = a.data[field]
