import pytz
import unittest
from datetime import datetime

class TestTimeZones(unittest.TestCase):

    def test_without_timezone(self):
        beginning_of_time = datetime(1970,1,1,0,0)
        self.assertEqual(beginning_of_time.timestamp(), 0.0)

    def test_with_timezone(self):
        actual_beginning_of_time = datetime(1970,1,1,0,0, tzinfo=pytz.timezone("UTC"))
        self.assertEqual(actual_beginning_of_timestamp(), 0.0)
if __name__ == '__main__":
    unittest.main()
