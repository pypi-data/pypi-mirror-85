
from estime2.config import (
    get_option
)
from typing import (
    Union
)



class Age():
    '''
    Age column of a PopTable.
    '''

    def __init__(
        self, 
        age: Union[int, str]
    ):
        '''
        Initialize the Age.

        Details
        -------
        Age is similar to type `int` except that it has lower and upper 
        bounds. The upper bound is of the form `000+` (meaning "000 or 
        over"), where the last letter is `+` and the rest is numeric. The 
        upper bound is set by the global option `estime2.options.age.max`, 
        and the lower bound is always `-1`.

        Usage
        -----
        `Age(age)`

        Arguments
        ---------
        * `age`: `int`, `str`, or `Age` itself. If `int`, it should fall in
            `[-1, 000+]`, where `000` in `000+` is set by 
            `estime2.options.age.max` (`99` by default), and `000+` means 
            "000 or over". For example, `-2` will return an error; both 
            `100` and `101` will return `100+`. If `str`, one can type 
            either an int like `'94'` (which will be initialized as the age
            `94`), or `'99+'` where it is then defined as the age `99+`. In
            case of it is `Age`, then it is converted back to `str` and is
            initialized again.
        '''

        age_min = -1
        has_plus = False
        msg_less_than_one =\
            "`age` must be at least -1, but the current value is {0}."
        if isinstance(age, str):
            if age[-1] == '+':
                has_plus = True
                try:
                    age = int(age[:-1])
                except:
                    raise ValueError(
                        f'"{age[:-1]}" in front of "+" cannot be '
                        'converted to int.'
                    )
                assert age >= age_min, msg_less_than_one.format(age)
            else:
                try:
                    age = int(age)
                except:
                    raise ValueError(
                        f'"{age}" is not convertible to `int`, '
                        'therefore not convertible to Age.'
                    )
                assert age >= age_min, msg_less_than_one.format(age)
        else:
            self.__init__(str(age))

        self.__age = age
        self.__plus = has_plus

    def __add__(self, other):
        '''
        Return the value of self + other.

        Argument
        --------
        * `other`: either `Age`, `int`, or `str`.

        Usage
        -----
        `self + other`

        Examples
        --------
        >>> # age.max = 99
        >>> Age(97) + 1
        98
        >>> Age(98) + 1
        99
        >>> Age(99) + 1
        100+
        >>> Age('98+') + 1
        99+
        >>> Age('99+') + 1
        100+
        >>> Age('100+') + 1
        100+
        '''

        if not isinstance(other, Age):
            try:
                other = Age(other)
                return self + other
            except:
                raise NotImplementedError
        if self.has_plus(): # e.g. 99+, 100+
            return Age(str(self.get_showing_age() + other.__age) + '+')
        if self.__age < get_option('age.max'):
            return Age(self.__age + other.__age)
        else: # i.e. self.__age >= age.max, regardless of other
            return Age(get_option('age.max') + 1)  

    def __eq__(self, other):
        '''
        Return True iff `self` is equal to `other`.

        Details
        -------
        1. If the showing age of `self` and `other` are equal, they are
            considered equal. 
        2. If one contains the other individual age conceptually 
            (e.g. `99+` contains `99`), then it is also considered equal. 
        3. If `other` can be initialized as `Age`, then it is converted to
            Age and then the method is applied.

        Argument
        --------
        * `other`: either `Age`, `int`, or `str`. 

        Usage
        -----
        `self == other`

        Examples
        --------
        >>> # age.max == 99
        >>> eg1 = Age(94); eg2 = Age(95)
        >>> eg1 == eg2
        False
        >>> eg3 = Age('99'); eg4 = Age('99+')
        >>> eg3 == eg4
        True
        >>> eg5 = Age(100)
        >>> eg4 == eg5 # False because 99 belongs to 99+ but not to 100+
        False
        >>> eg6 = Age(101)
        >>> eg5 == eg6 # True because both are initialized as '100+'
        True
        >>> eg7 = Age('120+')
        >>> eg5 == eg7 # True because '120+' is initialized as '100+'
        True
        '''

        if not isinstance(other, Age):
            try:
                other = Age(other)
                return self == other
            except:
                raise NotImplementedError
        return self.get_showing_age() == other.get_showing_age()

    def __ge__(self, other):
        '''
        Return True iff self >= other.

        Details
        -------
        1. If the showing age of `self` is greater than or equal to 
            `other`, the method returns True.
        2. If one contains the other individual age conceptually 
            (e.g. `99+` contains `99`), then it is considered equal, and
            thus returns True.
        3. If `other` can be initialized as `Age`, then it is converted to
            Age and then the method is applied.

        Argument
        --------
        * `other`: either `Age`, `int`, or `str`. 

        Usage
        -----
        `self >= other`

        Examples
        --------
        >>> # age.max == 99
        >>> eg1 = Age(94); eg2 = Age(95)
        >>> eg1 >= eg2
        False
        >>> eg3 = Age('99'); eg4 = Age('99+')
        >>> eg3 >= eg4 # True because "99 == 99+"
        True
        >>> eg5 = Age(100); eg6 = Age(101)
        >>> eg5 >= eg6 # True because both are initialized as "100+"
        True
        >>> eg7 = Age('120+')
        >>> eg5 >= eg7 # True because '120+' is initialized as '100+'
        True
        '''

        if not isinstance(other, Age):
            try:
                other = Age(other)
                return self >= other
            except:
                raise NotImplementedError
        return self.get_showing_age() >= other.get_showing_age()        

    def __gt__(self, other):
        '''
        Return True iff self > other.

        Details
        -------
        1. If the showing age of `self` is greater than `other`, the method
            returns True.
        2. If one contains the other individual age conceptually 
            (e.g. `99+` contains `99`), then it is considered equal, and
            thus one is NOT greater than the other; it returns False.
        3. If `other` can be initialized as `Age`, then it is converted to
            Age and then the method is applied.

        Argument
        --------
        * `other`: either `Age`, `int`, or `str`. 

        Usage
        -----
        `self > other`

        Examples
        --------
        >>> # age.max == 99
        >>> eg1 = Age(95); eg2 = Age(94)
        >>> eg1 > eg2
        True
        >>> eg3 = Age('99'); eg4 = Age('99+')
        >>> eg3 > eg4 # False because "99 == 99+"
        False
        >>> eg5 = Age(100); eg6 = Age(101)
        >>> eg5 > eg6 # False because both are initialized as "100+"
        False
        >>> eg7 = Age('120+')
        >>> eg5 > eg7 # False because '120+' is initialized as '100+'
        False
        '''

        if not isinstance(other, Age):
            try:
                other = Age(other)
                return self > other
            except:
                raise NotImplementedError
        return self.get_showing_age() > other.get_showing_age()

    def __hash__(self):
        return hash((self.get_showing_age(), ))

    def __le__(self, other):
        '''
        Return True iff self <= other.

        Details
        -------
        1. If the showing age of `self` is less than or equal to `other`, 
            the method returns True.
        2. If one contains the other individual age conceptually 
            (e.g. `99+` contains `99`), then it is considered equal, and
            thus returns True.
        3. If `other` can be initialized as `Age`, then it is converted to
            Age and then the method is applied.

        Argument
        --------
        * `other`: either `Age`, `int`, or `str`. 

        Usage
        -----
        `self < other`

        Examples
        --------
        >>> # age.max == 99
        >>> eg1 = Age(95); eg2 = Age(94)
        >>> eg1 <= eg2
        False
        >>> eg3 = Age('99'); eg4 = Age('99+')
        >>> eg3 <= eg4 # True because "99 == 99+"
        True
        >>> eg5 = Age(100); eg6 = Age(101)
        >>> eg5 <= eg6 # True because both are initialized as "100+"
        True
        >>> eg7 = Age('120+')
        >>> eg5 <= eg7 # True because '120+' is initialized as '100+'
        True
        '''

        if not isinstance(other, Age):
            try:
                other = Age(other)
                return self <= other
            except:
                raise NotImplementedError
        return self.get_showing_age() <= other.get_showing_age()

    def __lt__(self, other):
        '''
        Return True iff self < other.

        Details
        -------
        1. If the showing age of `self` is less than `other`, the method
            returns True.
        2. If one contains the other individual age conceptually 
            (e.g. `99+` contains `99`), then it is considered equal, and
            thus one is NOT less than the other; it returns False.
        3. If `other` can be initialized as `Age`, then it is converted to
            Age and then the method is applied.

        Argument
        --------
        * `other`: either `Age`, `int`, or `str`. 

        Usage
        -----
        `self < other`

        Examples
        --------
        >>> # age.max == 99
        >>> eg1 = Age(94); eg2 = Age(95)
        >>> eg1 < eg2
        True
        >>> eg3 = Age('99'); eg4 = Age('99+')
        >>> eg3 < eg4 # False because "99 == 99+"
        False
        >>> eg5 = Age(100); eg6 = Age(101)
        >>> eg5 < eg6 # False because both are initialized as "100+"
        False
        >>> eg7 = Age('120+')
        >>> eg5 < eg7 # False because '120+' is initialized as '100+'
        False
        '''

        if not isinstance(other, Age):
            try:
                other = Age(other)
                return self < other
            except:
                raise NotImplementedError
        return self.get_showing_age() < other.get_showing_age()

    def __repr__(self):
        '''
        Return the Age representation of self.

        Examples
        --------
        >>> Age(94)     # <= age.max, does not have '+'
        94
        >>> Age('99+')  # <= age.max, does have '+'
        99+
        >>> Age(100)    #  > age.max, does not have '+' case 1
        100+
        >>> Age(101)    #  > age.max, does not have '+' case 2
        100+
        >>> Age('120+') #  > age.max, does have '+'
        100+
        '''

        return str(self)

    def __str__(self):
        '''
        Return the string representation of self.

        Examples
        --------
        >>> str(Age(94))     # <= age.max, does not have '+'
        '94'
        >>> str(Age('99+'))  # <= age.max, does have '+'
        '99+'
        >>> str(Age(100))    #  > age.max, does not have '+' case 1
        '100+'
        >>> str(Age(101))    #  > age.max, does not have '+' case 2
        '100+'
        >>> str(Age('120+')) #  > age.max, does have '+'
        '100+'
        '''

        showing_age = self.get_showing_age()
        last = '+' if self.has_plus() else ''

        return str(showing_age) + last

    def __sub__(self, other):
        '''
        Return the value of self - other.

        Argument
        --------
        * `other`: either `Age`, `int`, or `str`.

        Usage
        -----
        `self - other`

        Examples
        --------
        >>> # age.max = 99
        >>> Age(97) - 1
        96
        >>> Age(98) - 1
        97
        >>> Age(99) - 1
        98
        >>> Age('98+') - 1
        97+
        >>> Age('99+') - 1
        98+
        >>> Age('100+') - 1
        99+
        >>> Age('120+') - 1
        99+
        '''

        if not isinstance(other, Age):
            try:
                other = Age(other)
                return self - other
            except:
                raise NotImplementedError
        if self.has_plus(): # e.g. 99+, 100+
            return Age(str(self.get_showing_age() - other.__age) + '+')
        if self.__age <= get_option('age.max'):
            return Age(self.__age - other.__age)
        else: # i.e. self.__age > age.max, regardless of other
            return Age(str(get_option('age.max')) + '+')

    def get_showing_age(self):
        '''
        Return the age on display.

        Details
        -------
        1. Any individual age less than or equal to `age.max` will return 
            the int. 
        2. Any individual age greater than `age.max` will return `age.max`
            plus 1. 
        3. If the `self` has plus at the end (such as `99+` or `100+`),
            then it will return the int before `+`.

        Usage
        -----
        `self.get_showing_age()`

        Examples
        --------
        >>> eg1 = Age(94)
        >>> eg1.get_showing_age()
        94
        >>> eg2 = Age('99+')
        >>> eg2.get_showing_age()
        99
        >>> eg3 = Age(100)
        >>> eg3.get_showing_age()
        100
        >>> eg4 = Age(101)
        >>> eg4.get_showing_age()
        100
        >>> eg5 = Age('120+')
        >>> eg5.get_showing_age()
        100
        '''

        showing_age = self.__age
        if self.__age > get_option('age.max'):
            showing_age = get_option('age.max') + 1
        
        return showing_age

    def has_plus(self):
        '''
        Return True iff `self` has a plus sign at the end.

        Details
        -------
        Whenever the initial `age` argument of `self` is less than or
        equal to `age.max`, this method will return False. Otherwise,
        it returns True because any `age` greater than `age.max` will be
        initialized as `000+`, where `000` is `age.max` plus 1.

        Usage
        -----
        `self.has_plus()`

        Examples
        --------
        >>> # age.max == 99
        >>> eg1 = Age(94)
        >>> eg1.has_plus()
        False
        >>> eg2 = Age('99+')
        >>> eg2.has_plus()
        True
        >>> eg3 = Age(100)
        >>> eg3.has_plus() # True, since eg3 is initialized as '100+'
        True
        >>> eg4 = Age(101)
        >>> eg4.has_plus() # True, since eg4 is initialized as '100+'
        True
        >>> eg5 = Age('120+')
        >>> eg5.has_plus()
        True
        '''

        return self.__age > get_option('age.max') or self.__plus

    def is_max(self):
        '''
        Return `True` iff `self` is the maximum.

        Details
        -------
        The method checks whether `self` is shown in the form of maximum
        given the global option value `age.max`. For example, if `age.max`
        is `99`, then the maximum possible form of `self` is `100+`. This
        will return `True` if `self` is in such a form.

        Usage
        -----
        `self.is_max()`

        Examples
        --------
        >>> # age.max == 99
        >>> eg1 = Age(94)
        >>> eg1.is_max()
        False
        >>> eg2 = Age('99+')
        >>> eg2.is_max()
        False
        >>> eg3 = Age(100)
        >>> eg3.is_max() # True, since eg3 is initialized as '100+'
        True
        >>> eg4 = Age(101)
        >>> eg4.is_max() # True, since eg4 is initialized as '100+'
        True
        >>> eg5 = Age('120+')
        >>> eg5.is_max()
        True
        '''

        check1 = self.get_showing_age() == get_option('age.max') + 1
        check2 = self.has_plus()

        return check1 and check2

if __name__ == '__main__':
    import doctest
    doctest.testmod()
