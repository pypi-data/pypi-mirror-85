import os
import sys
import unittest


os.chdir("../")
sys.path[0] = os.getcwd()


import bitcoinfees


class UtilitsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_recommended(self):
        response = bitcoinfees.recommended()
        for speed in ['fastestFee', 'halfHourFee', 'hourFee']:
            self.assertTrue(speed in response)


if __name__ == "__main__":
    unittest.main()