import unittest

from pylunar.calendar import *


class FuncTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGregorian2Lunar(self):
        self.assertEqual(Gregorian2Lunar((2012, 1, 3)), (2011, 12, 10, False))

    def testLunar2Gregorian(self):
        self.assertEqual(Lunar2Gregorian((2013, 4, 10, False)), (2013, 5, 19))

    def testGetLunarString(self):
        for a in GetLunarString((2013, 5, 26, False)):
            print (a)

        for a in GetLunarString(Gregorian2Lunar((2012, 6, 15))):
            print (a)

    def testGetLunarFeast(self):
        self.assertEqual(Get24LunarFeast((2013, 5, 5)), ('立夏', 4))
        self.assertEqual(Get24LunarFeast((2013, 5, 4)), ('', 3))

    def testGet8Zi(self):
        self.assertEqual(Get8Zi((2012, 5, 4, 0, 0)),
                         ('壬辰', '甲辰', '乙丑', '丙子', '甲午'))
        # 0时0分应为子时午分

if __name__ == '__main__':
    unittest.main()
