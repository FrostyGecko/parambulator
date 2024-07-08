import unittest
import parambulator.twobody.twobody as tbp
import numpy as np


class Testtwobody(unittest.TestCase):
    def test_InverseSquare1(self):
        I0      = 400
        R0      = 400
        R1      = 800
        
        flux    = tbp.InverseSquare(I0, R0, R1)
        
        self.assertEqual(flux, 100)
        
        
    def test_tbp0000_EccVec_1(self):
        R = np.array([7000,200,3000])
        V = np.array([1,9.5,1.5])
        
        e_vec = tbp.tbp0000_EccVec_1(R, V)
        
        self.assertAlmostEqual(e_vec[0],0.68955,3)
        self.assertAlmostEqual(e_vec[1],-0.2987,3)
        self.assertAlmostEqual(e_vec[2],0.259502,3)
        
        
    def test_tbp0000_Cart_to_Kep(self):
        R = np.array([7000,200,3000])
        V = np.array([1,9.5,1.5])
        
        kep = tbp.tbp0000_Cart_to_Kepler(R,V)
        self.assertAlmostEqual(kep['a'],35776.11,2)
        self.assertAlmostEqual(kep['i'],23.7562,2)

                

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
    