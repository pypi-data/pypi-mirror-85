import mage
import time
import unittest

class TestScore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mage.connect()

    def test_by_date(self):
        self.assertTrue(len(mage.Score.by_date('YEAR')) > 0)

if __name__ == '__main__':
    unittest.main()
