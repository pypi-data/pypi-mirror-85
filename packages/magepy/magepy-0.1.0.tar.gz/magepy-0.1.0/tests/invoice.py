import mage
import time
import unittest

class TestInvoice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mage.connect()

    def test_list(self):
        invoices = mage.Invoice.list()
        self.assertTrue(len(invoices) > 0)

    def test_get(self):
        invoices = mage.Invoice.list()
        self.assertTrue(len(invoices) > 0)
        self.assertIsNotNone(mage.Invoice.get(invoices[0]['id']))

if __name__ == '__main__':
    unittest.main()
