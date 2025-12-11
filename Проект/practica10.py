import unittest
def divide(a, b):
    """
    Divide two numbers.
    :param a: The first number.
    :type a: int
    :param b: The second number.
    :type b: int
    :return: The result of the division.
    :rtype: int or float
    :raises: TypeError or ValueError

    """
    if b == 0:
        raise ValueError("Деление на ноль недопустимо")
    return a / b

class TestDivide(unittest.TestCase):
    """
    Check the division.
    """

    def test_divide_correct(self):
        """
        Test the result of the division.
        """
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 3), 3)

    def test_divide_zero_division(self):
        """
        Test the mistake of the division.
        """
        with self.assertRaises(ValueError):
            divide(10, 0)


def process_data(input_data):
    """

    :param input_data: The input data.
    :type input_data: str or int or float
    :return:  The result of the process_data.
    rtype: str or int or float
    raises: TypeError or ValueError
    """
    if input_data is None:
        raise ValueError("Входные данные не должны быть None")
    result = input_data * 2  # пример обработки
    return result