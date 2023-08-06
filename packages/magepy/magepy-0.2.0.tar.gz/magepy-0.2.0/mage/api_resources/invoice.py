import json
from .abstract import *

class Invoice( ListableAPIResource ):
    @classmethod
    def get(cls, invoice_id):
        """
        Gets an invoice by ID.

        Args:
            invoice_id (str):

        Returns:
            dict on success, None on error

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Invoice.get('11111111-1111-1111-1111-111111111111')
        """

        from mage import client_id

        retval = cls._retrieve_all('get_single_invoice', client_id=client_id, invoice_id=invoice_id)
        if len(retval) > 0:
            return retval[0].data
        else:
            return None

    @classmethod
    def list(cls):
        """
        Lists recent invoices.

        Returns:
            list of dict

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Invoice.list()
        """

        from .client import Client
        from mage import client_id
        retval = Client.eq(id=client_id).select('invoices')[0]
        if retval is not None:
            return json.loads(retval.invoices)['data']
        return []
