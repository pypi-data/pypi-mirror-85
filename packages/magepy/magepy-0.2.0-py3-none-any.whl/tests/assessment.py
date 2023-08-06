import mage
import time
import unittest

class TestAssessment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mage.connect()

    def setUp(self):
        self.a = mage.Assessment.create('EXTERNAL', name='TEST')
        self.ar_id = None

    def tearDown(self):
        if self.ar_id:
            mage.AssessmentRun.stop(assessment_run_id=self.ar_id)
        if self.a:
            self.a.delete()

    def test_create_assessment(self):
        self.assertIsInstance(self.a,mage.Assessment)

    def test_find_assessment_by_id(self):
        #BUG: created items are not always immediately findable
        time.sleep(2)
        result = mage.Assessment.eq(id=self.a.id).limit(1).search()
        self.assertEqual(len(result),1)

    def test_find_assessment_by_name(self):
        #BUG: created items are not always immediately findable
        time.sleep(2)
        result = mage.Assessment.eq(name=self.a.name).limit(1).search()
        self.assertEqual(len(result),1)

    def test_list_assessment(self):
        #BUG: created items are not always immediately findable
        time.sleep(2)
        result = mage.Assessment.list()
        self.assertTrue(len(result) > 0)

    def test_update_assessment_by_assignment(self):
        self.a.name = "KILROY"
        self.assertEqual(self.a.name, 'KILROY')

    def test_update_assessment_by_call(self):
        self.a.update(name="KILROY")
        self.assertEqual(self.a.name, 'KILROY')

    def test_start_assessment(self):
        self.ar_id = self.a.start()
        self.assertIsNotNone(self.ar_id)

    def test_load_assets(self):
        data = {'ips':['127.0.0.1']}
        self.a.load_assets(data)
        self.assertEqual(len(self.a.assets), 1)

    def test_delete_assessment(self):
        self.assertIsNotNone(self.a.delete())
        self.a = None

    def test_list_runs(self):
        self.a.runs
        pass

if __name__ == '__main__':
    unittest.main()
