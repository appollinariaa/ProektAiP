import unittest
def divide(a, b):
    if b == 0:
        raise ValueError("Деление на ноль недопустимо")
    return a / b

class TestDivide(unittest.TestCase):

    def test_divide_correct(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 3), 3)

    def test_divide_zero_division(self):
        with self.assertRaises(ValueError):
            divide(10, 0)


from unittest.mock import Mock

def display_message():
    print("Привет, мир!")
mock_print = Mock()
print = mock_print
display_message()
mock_print.assert_called_with("Привет, мир!")
