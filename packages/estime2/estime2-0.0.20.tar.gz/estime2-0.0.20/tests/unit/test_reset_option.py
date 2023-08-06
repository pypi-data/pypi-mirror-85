
import estime2
import pytest



class TestResetOption:
    '''
    Tests for `estime2.reset_option('x.y')`.
    '''

    def test_reset_option_basic(self):
        '''
        Test if `reset_option('x.y')` resets the value of 
        `estime2.options.x.y` to its factory setting.
        '''

        prev_pop_at_least = estime2.options.pop.at_least
        estime2.options.pop.at_least = 2
        pop_at_least_before_reset = estime2.options.pop.at_least
        estime2.reset_option('pop.at_least')
        pop_at_least_after_reset = estime2.options.pop.at_least

        assert pop_at_least_before_reset == 2
        assert pop_at_least_after_reset == prev_pop_at_least
    
    def test_reset_option_all(self):
        '''
        Test if `reset_option('all')` resets all the modifications made
        in the session.
        '''

        prev_pop_at_least = estime2.options.pop.at_least
        estime2.options.pop.at_least = 2
        prev_comp_neg_death = estime2.options.comp_neg.death
        estime2.options.comp_neg.death = 'Deaths'

        estime2.reset_option('all')

        assert estime2.options.pop.at_least == prev_pop_at_least
        assert estime2.options.comp_neg.death == prev_comp_neg_death
    
    def test_reset_option_requires_more_chars(self):
        '''
        Test that `reset_option('x.yz')` requires 4 or more characters.
        '''

        with pytest.raises(ValueError) as more_char_error:
            estime2.reset_option('pop')
        msg =\
            "You must specify at least 4 characters when " +\
            "resetting multiple keys; use the special keyword " +\
            '"all" to reset all the options to their default value'

        assert str(more_char_error.value) == msg

    def test_reset_option_resets_multiple_ops(self):
        '''
        Test if `reset_option('x.y')` resets multiple options whenever
        those options match the pattern `'x.y'`.
        '''

        prev_pop_start = estime2.options.pop.start
        prev_pop_sex = estime2.options.pop.sex
        prev_pop_age = estime2.options.pop.age
        prev_pop_at_least = estime2.options.pop.at_least

        estime2.options.pop.start = 'Start-of-period population'
        estime2.options.pop.sex = 'sex'
        estime2.options.pop.age = 'age'
        estime2.options.pop.at_least = 2

        assert estime2.options.pop.start != prev_pop_start
        assert estime2.options.pop.sex != prev_pop_sex
        assert estime2.options.pop.age != prev_pop_age
        assert estime2.options.pop.at_least != prev_pop_at_least

        # Case 1: matches with pop.start and pop.sex
        estime2.reset_option('pop.s')

        assert estime2.options.pop.start == prev_pop_start
        assert estime2.options.pop.sex == prev_pop_sex
        assert estime2.options.pop.age != prev_pop_age
        assert estime2.options.pop.at_least != prev_pop_at_least

        estime2.options.pop.start = 'Start-of-period population'
        estime2.options.pop.sex = 'sex'

        # Case 2: matches with pop.s* and pop.a*
        estime2.reset_option('pop.s', 'pop.a')

        assert estime2.options.pop.start == prev_pop_start
        assert estime2.options.pop.sex == prev_pop_sex
        assert estime2.options.pop.age == prev_pop_age
        assert estime2.options.pop.at_least == prev_pop_at_least

        estime2.options.pop.start = 'Start-of-period population'
        estime2.options.pop.sex = 'sex'
        estime2.options.pop.age = 'age'
        estime2.options.pop.at_least = 2
        prev_pop_end = estime2.options.pop.end
        estime2.options.pop.end = 'End-of-period population'

        assert estime2.options.pop.end != prev_pop_end

        # Case 3: matches with pop.*
        estime2.reset_option('pop.')

        assert estime2.options.pop.start == prev_pop_start
        assert estime2.options.pop.sex == prev_pop_sex
        assert estime2.options.pop.age == prev_pop_age
        assert estime2.options.pop.at_least == prev_pop_at_least
        assert estime2.options.pop.end == prev_pop_end

    def test_reset_option_takes_multiple_args(self):
        '''
        Test that `reset_option()` takes multiple arguments so
        that, for instance, if `reset_option('x.y', 'z.w')` is executed,
        then both `options.x.y` and `options.z.w` reset to their factory
        settings.
        '''

        prev_age_max = estime2.options.age.max
        prev_pop_sex = estime2.options.pop.sex
        estime2.options.age.max = 89
        estime2.options.pop.sex = 'sex'
        
        assert estime2.options.age.max != prev_age_max
        assert estime2.options.pop.sex != prev_pop_sex

        estime2.reset_option('age.max', 'pop.sex')

        assert estime2.options.age.max == prev_age_max
        assert estime2.options.pop.sex == prev_pop_sex