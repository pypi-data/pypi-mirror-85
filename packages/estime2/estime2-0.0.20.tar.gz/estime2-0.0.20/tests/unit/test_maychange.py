
import estime2
import pytest



class TestMaychange:
    '''
    Test behaviours of `estime2.config` module that may change in later
    versions of `estime2`.
    '''

    def test_maychange_options_pattern(self):
        '''
        Test that the pattern matching via `re` module is NOT applied to 
        `estime2.options.x.y`.
        '''

        # Case 1: unique matching NOT supported
        with pytest.raises(KeyError) as keyerror_context1:
            pop_st = estime2.options.pop.st

        # Case 2: multiple matching NOT supported
        with pytest.raises(KeyError) as keyerror_context2:
            comp_neg_i = estime2.options.comp_neg.i

        msg = "'No such option exists.'"
        assert str(keyerror_context1.value) == msg
        assert str(keyerror_context2.value) == msg
