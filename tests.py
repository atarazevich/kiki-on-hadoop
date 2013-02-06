import unittest
import time
import datetime
from StringIO import StringIO

try:
    import simplejson as json
except ImportError:
    import json

from job import AnalyticJob

class MRTest(unittest.TestCase):
    def setUp(self):
        self.job = AnalyticJob()

    def test_mapper_with_simple_log(self):
        self.job.sandbox(stdin=StringIO('2013-02-05T13:52:08Z hdfs.test.search {}'))
        self.job.run_mapper()

        emit1, emit2 =  self.job.parse_output()
        keys, values = emit1

        self.assertEqual(values, {'search': 1})
        self.assertEqual(keys['dt'], '2013-02-05')

        self.assertIsNone(emit2[0]['source'])
        self.assertIsNone(emit2[0]['feed'])
        self.assertIsNone(emit2[0]['market'])


    def test_mapper_with_unknown_type(self):
        self.job.sandbox(stdin=StringIO('2013-02-05T13:52:08Z {}'))
        self.job.run_mapper()

        self.assertEqual(self.job.parse_output(), [])

    def test_mapper_with_invalid_input(self):
        self.job.sandbox(stdin=StringIO('aaa|aaa\nbbb\naaa|{}\n'))
        self.job.run_mapper()

        self.assertEqual(self.job.parse_output(), [])

    def test_mapper(self):
        timestamp = int(time.time())
        self.job.sandbox(stdin=StringIO('2013-02-05T08:24:06Z   hdfs.test.click {"source":"bing","cohort":"ccc"}'))
        self.job.run_mapper()

        _, emit = self.job.parse_output()
        keys, values = emit

        self.assertIsNone(keys['feed'])
        self.assertEqual(keys['cohort'], 'ccc')
        self.assertEqual(keys['source'], 'bing')
        self.assertEqual(keys['dt'], '2013-02-05')

        self.assertEqual(values, {'click': 1})

    def test_reducer(self):
        key = {'source': 'aaa'}
        values = [{'clicks': 5}, {'clicks': 3}, {'searches': 2}, {'impressions': 3}, {'impressions': 7}]
        protocol = self.job.INTERNAL_PROTOCOL()
        data = '\n'.join(protocol.write(key, value) for value in values)

        self.job.sandbox(stdin=StringIO(data))
        self.job.run_reducer()

        result = self.job.parse_output()[0]
        _, values = result

        self.assertEqual(values['clicks'], 8)
        self.assertEqual(values['searches'], 2)
        self.assertEqual(values['impressions'], 10)


if __name__ == '__main__':
    unittest.main()
