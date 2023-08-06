
def to_camel_case(snake_str):
    """
    From https://stackoverflow.com/questions/19053707/converting-snake-case-to-lower-camel-case-lowercamelcase
    """
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(camel_str):
    """
    From https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    Note that this function doesn't cover all cases in general, but it covers ours.
    """
    return ''.join(['_'+c.lower() if c.isupper() else c for c in camel_str]).lstrip('_')


class class_or_instance_method(classmethod):
    """Decorate a class method with this to know if it is called as a class method or instance method.  Sourced from https://stackoverflow.com/questions/28237955/same-name-for-classmethod-and-instancemethod.

    Example:
        .. code-block::

            class X:
                @class_or_instancemethod
                def foo(self_or_cls):
                    if isinstance(self_or_cls, type):
                        return f"bound to the class, {self_or_cls}"
                    else:
                        return f"bound to the instance, {self_or_cls}"
    """

    def __get__(self, instance, type_):
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)


def update_subfields(field, key, value, query):
    """
    This function goes through a request to the server to select and exclude fields from the request.
    """
    soft_exclude=['recon']
    hard_exclude = ['client', 'arn', 'execution_arn', 'write_key', 'secret_key', 'session_token', 'additional_data', 'stripe_subscription_id', 'stripe_latest_invoice_status', 'stripe_customer_id', 'stripe_customer', 'stripe_subscription_status']
    params = value.copy()
    select = params.pop('select',{})

    # e.g., a = op.search_assessments(limit=1)
    a = getattr(field, key)(**params)

    # e.g., q = schema.Query.search_assessments.type
    q = getattr(query, key).type
    if not hasattr(q, '__field_names__'):
        return a

    if 'items' in q.__field_names__:
        a.items()
        a.next_token()
        update_subfields(a, 'items', {'select': select}, q)
    else:
        if select:
            try:
                a.id()
            except AttributeError:
                pass
            for k in select:
                v = select[k]
                if k not in hard_exclude:
                    if v is None:
                        #getattr(a, k)()
                        update_subfields(a, k, {}, q)
                    else:
                        update_subfields(a, k, v._params, q)
        else:
            for f in q.__field_names__:
                if f not in hard_exclude + soft_exclude:
                    if not hasattr(getattr(q, f).type, '__field_names__'):
                        getattr(a, f)()
    return a


