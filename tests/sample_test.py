import unittest


class BasicTest(unittest.TestCase):
    def setUp(self) -> None:
        print('Setting up')

    def tearDown(self) -> None:
        print('Tearing down :(')

    def test_sum(self):
        self.assertEqual(1 + 2, 3)

    def test_difference(self):
        self.assertEqual(2 - 1, 1)


if __name__ == '__main__':
    unittest.main()
