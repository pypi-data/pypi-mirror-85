
import estime2
import pytest



class TestSetOption:
    '''
    Tests for `estime2.set_option('x.y')` as well as 
    `estime2.options.x.y = z`.
    '''

    def test_set_option_is_equivalent_to_assignment(self):
        '''
        Test if `set_option('x.y', z)` does the same job as
        `estime2.options.x.y = z` (it should).
        '''

        to_set = [
            estime2.options.comp_pos.npr_in, 
            estime2.options.comp_pos.interprov_in
        ]
        prev_comp_end = estime2.options.comp.end
        
        # Way 1: assignment
        estime2.options.comp.end = to_set
        setting_way1 = estime2.options.comp.end
        estime2.options.comp.end = prev_comp_end

        # Way 2: using set_option(...)
        estime2.set_option('comp.end', to_set)
        setting_way2 = estime2.options.comp.end
        estime2.set_option('comp.end', prev_comp_end)

        assert setting_way1 == setting_way2

    def test_set_option_configures_multiple_ops(self):
        '''
        Test that `set_option(...)` is able to set multiple options at 
        once. Also, check that `set_option(...)` finds an option that
        matches a pattern.
        '''

        estime2.set_option('pop.se', 'sex', 'comp_neg.d', 'Death')
        assert estime2.options.pop.sex == 'sex'
        assert estime2.options.comp_neg.death == 'Death'

    def test_set_option_error_by_wrong_number_args(self):
        '''
        Test if `estime2.set_option(...)` raises a ValueError whenever
        no arguments or odd number arguments are provided.
        '''

        # No arg
        with pytest.raises(ValueError) as no_arg_error:
            estime2.set_option()
        
        # Odd number of args
        with pytest.raises(ValueError) as odd_arg_error:
            estime2.set_option('pop.sex', 'sex', 'tester')
        
        msg = "Must provide an even number of non-keyword arguments."

        assert str(no_arg_error.value) == msg
        assert str(odd_arg_error.value) == msg
    
    def test_set_option_error_by_invalid_option_setup(self):
        '''
        Test if `set_option(...)`:
            1. raises an error whenever an option provided does not exist;
            2. raises an error whenever an option pattern provided is
                ambiguous (i.e. a pattern patches multiple options);
            3. calls a validator equipped with that option and raises an
                error from the validator.
        '''

        # Case 1
        with pytest.raises(KeyError) as no_exist_error:
            estime2.set_option('non.existent', 'option')
        msg1 = '"No such keys: \'non.existent\'"'

        # Case 2
        with pytest.raises(KeyError) as multiple_ops_error:
            estime2.set_option('comp_pos.i', 'which_i')
        msg2 = "'Pattern matched multiple keys.'"

        # Case 3
        with pytest.raises(TypeError) as validator_error:
            with estime2.option_context('pop.at_least', 1.2):
                test = 3
        msg3 =\
            "pop.at_least must be <class 'int'>, not of <class 'float'>."

        assert str(no_exist_error.value) == msg1
        assert str(multiple_ops_error.value) == msg2
        assert str(validator_error.value) == msg3

