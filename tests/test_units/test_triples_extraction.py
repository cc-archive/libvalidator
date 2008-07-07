# -*- coding: utf-8 -*-
import nose.tools

class TestTriplesExtraction():
    def __init__(self, *args, **kargs):
        pass
    
    def test_positive(self):
        pass
    
    def test_negative(self):
        def blow_up():
            assert False
        nose.tools.assert_raises(AssertionError, blow_up)
