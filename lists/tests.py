from django.test import TestCase

# Create your tests here.
class SmokeTest(TestCase):
    '''тест на токсичность'''

    def test_bad_maths(self):
        '''тест: неправильные математические вычислениея'''
        self.assertEqual(1 + 1, 3)
