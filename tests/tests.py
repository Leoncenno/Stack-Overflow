import unittest
from app.validations import  Validators

class test_validators(unittest.TestCase):
    def setUp(self):
        self.val = Validators()
        
    
    def test_validate_missing_post(self):
        self.assertTrue(self.val.validate_missing_post(' '))

    def test_validate_empty_post(self):
        self.assertTrue(self.val.validate_empty_post(''))

    def test_remove_spaces(self):
        self.assertEqual('No way', self.val.remove_spaces('  No way '))

    def test_validate_nonstring_input(self):
        self.assertTrue(self.val.validate_nonstring_input('23'))

    def test_validate_date_of_birth_format(self):
        self.assertTrue(self.val.validate_date_of_birth_format('1991-08-22'))

if __name__ == '__main__':
    unittest.main()