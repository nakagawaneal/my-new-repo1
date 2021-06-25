#save this file as test_calc.py --> this is normally the right nomenclature..test_"what the purpose is".
import unittest #this is the standard library, no need to install
import calc #we need to import the module that we want to test...because calc is in the same directory, ie (calc.py), we don't need to specify the location.

class TestCalc(unittest.TestCase):
    #this will give us access to different testing capabilities within this class...


    def test_add(self):
        result = calc.add(10,5)
        self.assertEqual(result, 15) # we can execute this from the command line...
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(calc.subtract(10, 5), 5)
        self.assertEqual(calc.subtract(-1, 1), -2)
        self.assertEqual(calc.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(calc.multiply(10,5), 50)
        self.assertEqual(calc.multiply(-1,1), -1)
        self.assertEqual(calc.multiply(-1,-1), 1)

    def test_divide(self):
        self.assertEqual(calc.divide(10,5), 2)
        self.assertEqual(calc.divide(-1,1), -1)
        self.assertEqual(calc.divide(-1,-1), 1)
        #self.assertRaises(ValueError, calc.divide, 10, 0) #this will determine whether the valuerror will arise when divded by 0

        #another way of doing this below
        with self.assertRaises(ValueError):
            calc.divide(10, 0) #this also satisfies the requirement

if __name__ == '__main__': #this will allow us to run the test within the editor.
#This __name__ = __main__ is not related to unittesting, rather, run the code within the conditional, which is the test_add. So when you run python test_calc.py in the command terminal, you'll get a output. You can also run this in the editor.
  unittest.main()


'''
- make sure that your test starts with 'test_'.
    - if not, then the test will not execute
    - you can either do result = calc.add(10,5) and then self.assertEqual(result, 15)....
        - or, simplify and make the code self.assertEqual(calc.add(10,5), 15)
    - make sure that you include different edge cases
    - for the number of cases you input, you'll see dots.
        - for instance, if you have 4 test cases, and all 4 test cases pass, you'll see ....
            - if one case failed, let's say the 3rd case, it'll look like '..F.'

- IMPORTANT: Make sure that your TESTS ARE ISOLATED
    - This MEANS -- DO NOT HAVE YOUR TEST INCLUDED IN ANOTHER TEST
- make sure that your test is updated with any new bugs that you discover. The point of this is to make sure that your code is bug free

- in line 31, there's asertRaises().
    - this will test whether the specific ERROR (i.e ValueError in the above example) is passed
        - if that specific value error is passed, then the test passed.
    - line 32:
        - we're using the context manager, 'WITH'
        - doing this simplifies the code and makes the code look prettier. \
        - recommended to use context manager when testing for Errors
'''
