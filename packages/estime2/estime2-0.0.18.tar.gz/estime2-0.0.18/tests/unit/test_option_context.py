
import estime2
import pytest



class TestOptionContext:

    def test_option_context_basic(self):
        '''
        Test if the context manager `with estime2.option_context(...)` 
        works properly.
        '''

        # Setting 1 context
        pop_birth_before_context = estime2.options.pop.birth
        with estime2.option_context('pop.birth', 'Birth'):
            pop_birth_inside_context = estime2.options.pop.birth
        pop_birth_after_context = estime2.options.pop.birth

        # Setting 2+ contexts
        emi_before = estime2.options.comp_neg.emi
        immi_before = estime2.options.comp_pos.immi
        with estime2.option_context(
            'comp_neg.emi', 'Emi', 
            'comp_pos.immi', 'Immi'
        ):
            pop_birth_wo_specifics = estime2.options.pop.birth
            emi_inside = estime2.options.comp_neg.emi
            immi_inside = estime2.options.comp_pos.immi            
        emi_after = estime2.options.comp_neg.emi
        immi_after = estime2.options.comp_pos.immi

        assert pop_birth_before_context == 'BTH'
        assert pop_birth_inside_context == 'Birth'
        assert pop_birth_after_context == pop_birth_before_context
        assert pop_birth_wo_specifics == pop_birth_before_context
        assert [emi_before, immi_before] == ['EMI', 'IMM']
        assert [emi_inside, immi_inside] == ['Emi', 'Immi']
        assert [emi_after, immi_after] == ['EMI', 'IMM']

    def test_option_context_error_by_wrong_number_args(self):
        '''
        Test if `estime2.option_context(...)` raises a ValueError whenever
        no arguments or odd number arguments are provided.
        '''

        # No arg
        with pytest.raises(ValueError) as no_arg_error:
            with estime2.option_context():
                test1 = estime2.options.comp_neg.temp_out

        # Odd number of args
        with pytest.raises(ValueError) as odd_arg_error:
            with estime2.option_context('pop.sex', 'sex', 'tester'):
                test2 = estime2.options.comp_neg.npr_out

        msg =\
            "Need to invoke as " +\
            "option_context(pat, val, [(pat, val), ...])."
        
        assert str(no_arg_error.value) == msg
        assert str(odd_arg_error.value) == msg

    def test_option_context_error_by_invalid_option_setup(self):
        '''
        Test if `option_context(...)`:
            1. raises an error whenever an option provided does not exist;
            2. raises an error whenever an option pattern provided is
                ambiguous (i.e. a pattern matches multiple options);
            3. calls a validator equipped with that option and raises an 
                error from the validator. 
        '''

        # Case 1
        with pytest.raises(KeyError) as no_exist_error:
            with estime2.option_context('non.existent', 'option'):
                test = 1
        msg1 = '"No such keys: \'non.existent\'"'

        # Case 2
        with pytest.raises(KeyError) as multiple_ops_error:
            with estime2.option_context('comp_neg.i', 'which_i'):
                test = 2
        msg2 = "'Pattern matched multiple keys.'"

        # Case 3
        with pytest.raises(TypeError) as validator_error:
            with estime2.option_context('pop.birth', None):
                test = 3
        msg3 = 'pop.birth cannot be None; it must be a str.'

        assert str(no_exist_error.value) == msg1
        assert str(multiple_ops_error.value) == msg2
        assert str(validator_error.value) == msg3