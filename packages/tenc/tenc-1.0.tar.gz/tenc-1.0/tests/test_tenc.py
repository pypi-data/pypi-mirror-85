import unittest
from tenc import Tenc

TencInstance = Tenc()
class TestStringMethods(unittest.TestCase):

    def test_encrypt(self):
        self.assertIsNotNone(TencInstance.encrypt('Test', '5a04ec902686fb05a6b7a338b6e07760'))

        with self.assertRaises(ValueError):
            TencInstance.encrypt('Test', '123')

        with self.assertRaises(AttributeError):
            TencInstance.encrypt('Test', None)

    def test_decrypt(self):
        self.assertEqual(TencInstance.decrypt(TencInstance.encrypt('Test', '5a04ec902686fb05a6b7a338b6e07760'), '5a04ec902686fb05a6b7a338b6e07760'), 'Test')

        with self.assertRaises(ValueError):
           TencInstance.decrypt(TencInstance.encrypt('Test', '5a04ec902686fb05a6b7a338b6e07760'), '12')


if __name__ == '__main__':
    unittest.main()
