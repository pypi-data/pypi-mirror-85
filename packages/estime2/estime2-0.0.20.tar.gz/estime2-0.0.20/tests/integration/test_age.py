
import estime2
import pandas as pd
import pytest



@pytest.fixture(scope = "module")
def test_tbl():
    # scope = "module" ensures test_tbl is called only once w/i the module,
    # not every time test_ method has `test_tbl` as an argument.
    test_dat = {
        'age': [94, 95, 96, 98, 99, 100, 101, 118, 119, 120, 121],
        'something': [i for i in range(11)]
    }
    tbl = pd.DataFrame(test_dat)
    tbl['age'] = tbl['age'].apply(estime2.Age)

    yield tbl
    # Additional action w/i this fixture done here
    # e.g. closing the connection



class TestAge:
    '''
    Tests for the `Age` class of estime2.
    '''
    
    @pytest.mark.parametrize(
        "lt_min, lt, eq, gt, inval",
        [
            ('-2.', '3', '99', '100', 'C++'),
            (-3, 3, 99, 100, [3, 4, 8]),
        ],
    )
    def test_age_convertible_to_int(
        self, lt_min, lt, eq, gt, inval,
        lower_max
    ):
        '''
        Test that: 
            1. `__init__` creates an instance of `Age` if an input is 
                convertible to `int`, and raises an error otherwise;
            2. `__init__` creates different instances of `Age` whenever 
                `estime2.options.age.max` gets different (it should). In 
                particular, `Age.has_plus()` should return different 
                boolean depending on that global option;
            3. `__str__` and `__repr__` are dynamic, i.e. their return
                values depend on the value of `estime2.options.age.max` 
                (they should).
        '''

        not_convertible_to_int =\
            '"{0}" is not convertible to `int`, ' +\
            "therefore not convertible to Age."            
        msg_less_than_one =\
            "`age` must be at least -1, but the current value is {0}." \
            if not isinstance(inval, str) else not_convertible_to_int
        msg_not_convbl =\
            '"{0}" in front of "+" cannot be converted to int.' \
            if isinstance(inval, str) else not_convertible_to_int

        with pytest.raises(Exception) as min_err:
            test = estime2.Age(lt_min)
        assert str(min_err.value) == msg_less_than_one.format(lt_min)

        assert estime2.options.age.max == 99
        age_3 = estime2.Age(lt) # less than age.max
        age_99 = estime2.Age(eq) # exactly age.max
        age_100 = estime2.Age(gt) # greater than age.max

        assert (str(age_99) == '99') and (not age_99.has_plus())
        assert not age_99.is_max()
        assert (str(age_100) == '100+') and (age_100.has_plus())
        assert age_100.is_max()
        assert age_99 != age_100

        # The following test implies that changing the global option 
        # DOES affect the pre-existing `Age`s.
        estime2.options.age.max = lower_max
        assert (str(age_99) == '95+') and (age_99.has_plus())
        assert age_99.is_max()
        assert (str(age_100) == '95+') and (age_100.has_plus())
        assert age_100.is_max()
        assert age_99 == age_100

        # The following test implies that creating an instance of `Age`
        # AFTER changing the global option ALSO DOES affect newly created 
        # `Age`s.
        age_99_new = estime2.Age(eq) # greater than new age.max
        assert (str(age_99_new) == '95+') and (age_99_new.has_plus())
        assert age_99_new.is_max()

        estime2.reset_option('age.max')

        with pytest.raises(ValueError) as invalid_err:
            test = estime2.Age(inval)
        in_0 = inval[:-1] if isinstance(inval, str) else inval
        assert str(invalid_err.value) == msg_not_convbl.format(in_0)

    @pytest.mark.parametrize(
        "oper, exp_i, exp_l, exp_u",
        [
            (
                '+', 
                [93,    99, '100+', '100+', '100+', '100+', '100+'],
                [93, '95+',  '95+',  '95+',  '95+',  '95+',  '95+'],
                [93,    99,    100, '100+', '101+',    116, '120+']
            ),
            (
                '-', 
                [91,    97,    98, '98+', '99+', '99+',  '99+'],
                [91, '94+', '94+', '94+', '94+', '94+',  '94+'],
                [91,    97,    98, '98+', '99+',   114, '119+']
            ),
        ],
    )
    def test_age_and_arithmetic_operators(
        self, oper, exp_i, exp_l, exp_u,
        lower_max, upper_max
    ):
        '''
        Test that `Age` works with arithmetic operators. In particular, 
        test that `Age` works with `+` and `-`. Test also that the return 
        value is dynamic, i.e. it depends on the value of `age.max`.
        '''

        assert estime2.options.age.max == 99

        a = [
            estime2.Age(92),
            estime2.Age(98),
            estime2.Age(99),
            estime2.Age('99+'),
            estime2.Age('100+'),
            estime2.Age(115),
            estime2.Age(120)
        ]

        for i in range(len(a)):
            assert eval(f"a[{i}] {oper} 1") == exp_i[i]

        estime2.options.age.max = lower_max
        for l in range(len(a)):
            assert eval(f"a[{l}] {oper} 1") == exp_l[l]

        estime2.options.age.max = upper_max
        for u in range(len(a)):
            assert eval(f"a[{u}] {oper} 1") == exp_u[u]

        estime2.reset_option('age.max')

    def test_age_and_comparison_operators(self, lower_max, upper_max):
        '''
        Test that `Age` works with comparison operators. In particular,
        test that `Age` works with `==`, `!=`, `>`, `>=`, `<`, and `<=`. 
        Test also that the return value is dynamic, i.e. it depends on the
        value of `estime2.options.age.max`.
        '''

        assert estime2.options.age.max == 99

        age_96 = estime2.Age(96)
        age_116 = estime2.Age(116)

        assert str(age_96) == '96'
        assert str(age_116) == '100+'
        assert age_96 != age_116
        assert age_96 < age_116
        assert age_96 <= age_116
        assert age_116 > age_96
        assert age_116 >= age_96

        estime2.options.age.max = lower_max
        assert str(age_96) == '95+'
        assert str(age_116) == '95+'
        assert age_96 == age_116

        estime2.options.age.max = upper_max
        assert str(age_96) == '96'
        assert str(age_116) == '116'
        assert age_96 != age_116
        assert age_96 < age_116
        assert age_96 <= age_116
        assert age_116 > age_96
        assert age_116 >= age_96

        estime2.reset_option('age.max')

    def test_age_is_displayed_dynamically_in_DataFrame(
        self, test_tbl, lower_max, upper_max
    ):
        '''
        Test if a data type of elements in Series is `Age`, then that 
        Series is shown (as str) differently whenever the `age.max` 
        is modified. 
        '''

        assert estime2.options.age.max == 99
        
        expected1 = '[94 95 96 98 99 100+ 100+ 100+ 100+ 100+ 100+]'
        assert str(test_tbl['age'].values) == expected1

        expected2 = '[94 95+ 95+ 95+ 95+ 95+ 95+ 95+ 95+ 95+ 95+]'
        estime2.options.age.max = lower_max
        assert str(test_tbl['age'].values) == expected2

        expected3 = '[94 95 96 98 99 100 101 118 119 120+ 120+]'
        estime2.options.age.max = upper_max
        assert str(test_tbl['age'].values) == expected3

        estime2.reset_option('age.max')

    def test_age_works_dynamically_with_DataFrame_groupby(
        self, test_tbl, lower_max, upper_max
    ):
        '''
        Test that `pandas.DataFrame.groupby()` is working properly with the
        `Age` class column. `__eq__()` and `__hash__()` are used in the
        process. This also tests whether the behaviour of `.groupby()`
        changes whenever `age.max` is different.
        '''

        assert estime2.options.age.max == 99

        def group(tbl):
            result = tbl\
                .groupby('age')\
                .agg(sum_s = ('something', 'sum'))\
                .reset_index()
            return result

        result1 = group(test_tbl)
        expected1_age = '[94 95 96 98 99 100+]'
        expected1_sum_s = '[ 0  1  2  3  4 45]'
        assert str(result1['age'].values) == expected1_age
        assert str(result1['sum_s'].values) == expected1_sum_s

        estime2.options.age.max = lower_max
        result2 = group(test_tbl)
        expected2_age = '[94 95+]'
        expected2_sum_s = '[ 0 55]'
        assert str(result2['age'].values) == expected2_age
        assert str(result2['sum_s'].values) == expected2_sum_s

        estime2.options.age.max = upper_max
        result3 = group(test_tbl)
        expected3_age = '[94 95 96 98 99 100 101 118 119 120+]'
        expected3_sum_s = '[ 0  1  2  3  4  5  6  7  8 19]'
        assert str(result3['age'].values) == expected3_age
        assert str(result3['sum_s'].values) == expected3_sum_s

        estime2.reset_option('age.max')
