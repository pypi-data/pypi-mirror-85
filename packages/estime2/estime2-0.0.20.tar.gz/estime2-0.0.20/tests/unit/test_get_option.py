
import estime2
import pytest



class TestGetOption:
    '''
    Tests for `estime2.get_option('x.y')` as well as `estime2.options.x.y`.
    '''

    def test_get_option_is_affected_by_assignment(self):
        '''
        Test if an assignment via `estime2.options.x.y = z` change the 
        return value of `estime2.options.x.y` as well as `get_option()` 
        (it should).
        '''

        pop_age_via_options1 = estime2.options.pop.age
        estime2.options.pop.age = 'age'
        pop_age_via_options2 = estime2.options.pop.age
        pop_age_via_get_option = estime2.get_option('pop.age')

        assert pop_age_via_options1 == 'Age'
        assert pop_age_via_options2 == 'age'
        assert pop_age_via_get_option == 'age'

    def test_get_option_matches_patterns(self):
        '''
        Test if the pattern matching for `get_option(...)` works properly.
        That is:
            1. Test if `get_option('xxx.yzw')` returns a proper global
                option whenever one and only one option matches the pattern
                'xxx.yzw'.
            2. Test if `get_option('xxx.y')` raises a KeyError whenever
                there are multiple options matching the pattern 'xxx.y'.
        '''

        # Case 1: unique matching
        pop_st = estime2.get_option('pop.st')
        pop_start = estime2.get_option('pop.start') # Only op that matches

        # Case 2: multiple matching
        with pytest.raises(KeyError) as matching_context:
            comp_neg_i = estime2.get_option('comp_neg.i')
        msg = "'Pattern matched multiple keys.'"

        assert pop_st == pop_start
        assert str(matching_context.value) == msg

    def test_get_option_raises_keyerror_no_ops(self):
        '''
        Test if `get_option('x.y')` raises error whenever 
        `estime2.options.x.y` does not exist.
        '''

        # Case 1: using estime2.options
        with pytest.raises(KeyError) as key_error_context1:
            estime2.options.nonexistent.op = 21
        msg1 = "'No such option exists.'"

        # Case 2: using get_option(...)
        fake_op = 'this_op.none'
        with pytest.raises(KeyError) as key_error_context2:
            nonexisting_op = estime2.get_option(fake_op)        
        msg2 = '"No such keys: \'{}\'"'.format(fake_op)

        assert str(key_error_context1.value) == msg1
        assert str(key_error_context2.value) == msg2

    def test_get_option_returns_same_vals(self):
        '''
        Test if `get_option('x.y')` returns the global option value
        `options.x.y`.
        '''

        method_via_options  = estime2.options.method  # one dot
        age_max_via_options = estime2.options.age.max # two dots
        method_via_get_option  = estime2.get_option('method')
        age_max_via_get_option = estime2.get_option('age.max')

        assert method_via_options == method_via_get_option
        assert age_max_via_options == age_max_via_get_option