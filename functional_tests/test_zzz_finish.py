#!/usr/bin/env python

from .base import FunctionalTest
import unittest

class FinishTestWriting(FunctionalTest):
    '''Check nothing but make a reminder'''

    @unittest.skip("not ready yet")
    def test_zzz_fail(self):
        '''test: functional tests are not done yet!'''
        self.fail('Закончить написание тестов!!!')
