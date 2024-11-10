import unittest
from constant import constant  # replace 'your_module' with the actual module name
from uncertainties import ufloat
from pint import UnitRegistry
ureg = UnitRegistry()

class TestConstant(unittest.TestCase):

    def setUp(self):
        # Create sample constants for testing
        self.c1 = constant(value=10.0, 
                           uncertainty=1.0, 
                           unit='m', 
                           abbreviation='c1', 
                           name='Test Constant 1',
                           lower_bound = 5,
                           upper_bound = 15)
        
        self.c2 = constant(value=-5.0, 
                           uncertainty=0.5, 
                           unit='m', 
                           abbreviation='c2', 
                           name='Test Constant 2',
                           lower_bound = -6,
                           upper_bound = -4)


if __name__ == '__main__':
    unittest.main()