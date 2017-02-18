import unittest
from pythonbuzzfeed import BuzzFeedAPI
from datetime import datetime

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.API = BuzzFeedAPI()
    def test_timerange(self):
        start_test_date = "2017-02-01 00:00:00"
        end_test_date = "2017-02-03 00:00:00"
        start_datetime = datetime.strptime(start_test_date, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(end_test_date, '%Y-%m-%d %H:%M:%S')
        feed = "lol"
        buzzes = self.API.get_timerange(feed, start_test_date, end_test_date)
        for buzz in buzzes:
            self.assertTrue(buzz is not None)
            self.assertTrue(buzz['published_date'] is not None)
            date = datetime.strptime(buzz['published_date'], '%Y-%m-%d %H:%M:%S')
            self.assertTrue(date > start_datetime)
            self.assertTrue(date < end_datetime)
    def test_popular(self):
        start_test_date = "2017-02-01 00:00:00"
        end_test_date = "2017-02-3 00:00:00"
        start_datetime = datetime.strptime(start_test_date, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(end_test_date, '%Y-%m-%d %H:%M:%S')
        feed = "lol"
        buzzes = self.API.get_popular(feed, start_test_date, end_test_date, 10)
        for buzz in buzzes:
            self.assertTrue(buzz is not None)
            self.assertTrue(buzz['published_date'] is not None)
            date = datetime.strptime(buzz['published_date'], '%Y-%m-%d %H:%M:%S')
            self.assertTrue(date > start_datetime)
            self.assertTrue(date < end_datetime)
            comments = self.API.get_num_comments(buzz['id'])
            self.assertTrue(comments >= 10)

if __name__ == '__main__':
    unittest.main()
