from .data_api_resource import DataAPIResource
from .util import *
from mage.schema import schema
from sgqlc.operation import Operation
from mage import logger
import re

class MutableAPIResource(DataAPIResource):
    """
    This parent class provides functionality to update server data.
    """
    @classmethod
    def mutate(cls, fn, **params):
        """
        The generic method for sending mutation requests to the server.
        """
        op = Operation(schema.Mutation)

        update_subfields(op, fn, params, query=schema.Mutation)
        logger.debug(op.__to_graphql__(auto_select_depth=1))

        from mage import endpoint
        result = endpoint(op.__to_graphql__(auto_select_depth=1))
        if 'errors' in result:
            for e in result['errors']:
                logger.error(e['message'])
        if 'data' in result and result['data']:
            data = getattr((op + result), fn)
            return data

        return None

    @class_or_instance_method
    def update(ctx, **params):
        """
        Updates a resource on the server
        """
        fn = getattr(ctx,'_UPDATE_FN',None)
        if not fn:
            raise NotImplementedError
        if isinstance(ctx, type):
            return ctx.mutate(fn, input={**params})
        else:
            data = ctx.mutate(fn, input={'id': ctx.id, **params})
            if data:
                ctx.data = data

    @class_or_instance_method
    def delete(ctx, **params):
        """
        Deletes a resource on the server
        """
        fn = getattr(ctx,'_DELETE_FN',None)
        if not fn:
            raise NotImplementedError
        if isinstance(ctx, type):
            return ctx.mutate(fn, input={**params})
        else:
            return ctx.mutate(fn, input={'id': ctx.id})
