
from estime2.metric import (
    get_agediff_range,
    get_agediff_sparsity,
    get_correction_magni,
    get_correction_sd,
    get_num_cells
)
from estime2.vis import (
    plot_pop,
    plot_correction
)
from typing import (
    List,
    Optional
)
import matplotlib.pyplot as plt
import numpy as np



class ProvPopTableResultsWrapper():
    '''
    A result of `ProvPopTable.fix_issues()` wrapped in the object.
    '''

    def __init__(
        self, 
        orig_table, 
        result_fix_issues: List,
        method: str
    ):
        '''
        Create an instance of `ProvPopTableResultsWrapper`.

        Arguments
        ---------
        * `orig_table`: a `ProvPopTable` that creates `result_fix_issues`.
        * `result_fix_issues`: a list of `ProvPopTable` and 
            `pandas.DataFrame`; the return value of 
            `orig_table.fix_issues(return_all_mods = True)`.
        * `method`: a str; a method used to fix the original table.
        '''

        self.__orig_table = orig_table
        self.__fixed_table = result_fix_issues[0]
        self.__corrections = result_fix_issues[1:]
        self.__method = method

    def get_corrections(self):
        '''
        Return all the corrections applied to the original table which
        has created the fixed table.

        Usage
        -----
        `self.get_corrections(self)`

        Returns
        -------
        A list of `pandas.DataFrame` if there is at least one correction.
        `None` otherwise.
        '''

        return self.__corrections

    def get_fixed_table(self):
        '''
        Return the `ProvPopTable` after correction.

        Usage
        -----
        `self.get_fixed_table()`
        '''

        return self.__fixed_table

    def get_metric_all(self, include_zeros: bool = False):
        '''
        Get the following metrics at each correction all at once:
            + range
            + average sparsity
            + average magnitude
            + standard deviation

        Usage
        -----
        `self.get_metric_all(include_zeros)`

        Arguments
        ---------
        * `include_zeros`: a bool, `False` by default; if `True`, then any
            corrections with a value 0 in the correction DataFrame will be
            included in the computation of evaluation metric.
        '''

        join_on = self.__fixed_table.get_pop_groups()
        join_on += ['Component']
        summary_metrics =\
            self.get_metric_range()\
            .merge(
                self.get_metric_sparsity(),
                on = join_on,
                how = 'inner'
            )\
            .merge(
                self.get_metric_magni(include_zeros),
                on = join_on,
                how = 'inner'
            )\
            .merge(
                self.get_metric_sd(include_zeros),
                on = join_on,
                how = 'inner'
            )
        
        return summary_metrics

    def get_metric_magni(self, include_zeros: bool = False):
        '''
        Get the magnitude of changes made due to corrections in
        `self.__corrections`. The smaller, the better.

        Details
        -------
        Define the magnitude of correction as the mean of absolute values 
        of each correction. That is, for example, the mean of the 
        correction (-4, 1, 1, 1) should be:
        
        (|-4| + |1| + |1| + |1|) / 4 = 1.75
        
        If `include_zeros` is `True` (`False` by default), it counts 
        corrections with a value 0 in the computation of magnitude.

        Usage
        -----
        `self.get_metric_magni(include_zeros)`

        Arguments
        ---------
        * `include_zeros`: a bool, `False` by default; if `True`, then any
            corrections with a value 0 in the correction DataFrame will be
            included in the magnitude computation.
        '''

        result_fix_issues = self.get_result_fix_issues()
        return get_correction_magni(result_fix_issues)        

    def get_metric_num_cells(self, include_zeros: bool = False):
        '''
        Get the number of modified cells in `self.__fixed_table`. Include
        the components with zero changes by setting `include_zeros` to be
        `True` (`False` by default). The smaller, the better.

        Details
        -------
        This function compares two tables: `self.__orig_table` and
        `self.__fixed_table`. It checks which cells have become different
        from `self.__orig_table` as a result of corrections in 
        `self.__corrections`, and calculates the total number of cells that
        have changed. The following information is checked:
        
            + The number of different cells in 
                `self.__orig_table.calculate_pop()` and
                `self.__fixed_table.calculate_pop()`
            + The number of different cells in corrected negative 
                components between `self.__orig_table` and 
                `self.__fixed_table`
            + The number of different cells in corrected positive 
                components between `self.__orig_table` and 
                `self.__fixed_table`
        
        Include the components with zero changes by setting `include_zeros`
        to be `True`.

        Usage
        -----
        `self.get_metric_num_cells(include_zeros)`

        Arguments
        ---------
        * `include_zeros`: a bool, `False` by default; if `True`, then all
            the components, including those with zero changes, are included
            in the returning `dict` of this function.
        
        Returns
        -------
        A `dict` with keys `col` (a str), where `col` is either the name of
        the end-of-period population or the name of the corrected 
        component, and `num_cell`, a nonnegative `int`.
        '''

        result = get_num_cells(
            poptbl = self.__orig_table, 
            result_fix_issues = self.get_result_fix_issues(),
            include_zeros = include_zeros
        )
        return result

    def get_metric_range(self):
        '''
        Get the difference in the modification age and the minimum 
        counter-adjusted age in each correction. The smaller, the better.

        Details
        -------
        This method measures how far the correction spans out within the 
        correction. For example, if the component modification is made at 
        age 96, and counter-adjustments are made to ages 95, 93, 91, 90, 
        then this function returns 6 because 96 - 90 = 6.

        Usage
        -----
        `self.get_metric_range()`
        '''

        result_fix_issues = self.get_result_fix_issues()
        return get_agediff_range(result_fix_issues)

    def get_metric_sd(self, include_zeros: bool = False):
        '''
        Compute the standard deviations of corrections applied to
        `self.__orig_table`. Let `include_zeros` be `True` if the user 
        wants to count zeros as a part of standard deviation computation. 
        The smaller, the better.

        Details
        -------
        This method is to compute the standard deviation of each 
        correction in `self.__corrections`. If `include_zeros` is `True`
        (`False` by default), it counts corrections with a value 0 in the 
        computation of standard deviation.

        Usage
        -----
        `self.get_metric_sd(include_zeros)`

        Arguments
        ---------
        * `include_zeros`: a bool, `False` by default; if `True`, then any
            corrections with a value 0 in the correction DataFrame will be
            included in the standard deviation computation.
        '''

        result_fix_issues = self.get_result_fix_issues()
        return get_correction_sd(result_fix_issues)

    def get_metric_sparsity(self):
        '''
        Get the mean value of how further away each corected record is
        located from one another in each correction. The smaller, the
        better.

        Details
        -------
        This method measures the mean age difference between corrected 
        records according to `self.__corrections`. For example, if the 
        component modification is made at age 96, and counter-adjustments 
        are made to ages 95, 93, 91, 90, then this function returns 1.5 
        because:

        (|96 - 95| + |95 - 93| + |93 - 91| + |91 - 90|) / 4 == 1.5

        Usage
        -----
        `self.get_metric_sparsity()`
        '''

        result_fix_issues = self.get_result_fix_issues()
        return get_agediff_sparsity(result_fix_issues)

    def get_orig_table(self):
        '''
        Return the `ProvPopTable` before correction.

        Usage
        -----
        `self.get_orig_table()`
        '''

        return self.__orig_table

    def get_result_fix_issues(self):
        '''
        Get the list where the first element is `self.__fixed_table` and
        from the second and last element are `self.__corrections`.

        Usage
        -----
        `self.get_result_fix_issues()`
        '''

        return [self.__fixed_table] + self.__corrections

    def plot_correction(
        self, 
        num: Optional[int] = None,
        age_range: Optional[List[int]] = None,
        alpha: float = .5
    ):
        '''
        Get the barplot of ages vs. `num`-th correction made in 
        `self.__orig_table` filtered by `age_range`. Set `alpha` for 
        transparency.

        Usage
        -----
        `self.plot_correction(num[, age_range, alpha])`

        Argument
        --------
        * `num`: an int, `None` by default; the order number of the 
            correction made. For example, `num = 3` means the function will
            display the 3rd correction applied to the table. If left 
            `None`, then the error is raised.
        * `age_range`: a list of two ints, `None` by default; only the 
            records of the correction having Ages within the closed 
            interval defined by this argument are used. If `None`, then all
            the Ages greater than or equal to the minimum age of nonzero 
            correction up to and including the modification age are used in
            the plot.
        * `alpha`: a float, .5 by default; the argument to control 
            transparency of a plot
        '''

        result_fix_issues = self.get_result_fix_issues()
        plot_correction(
            result_fix_issues = result_fix_issues, 
            num = num,
            age_range = age_range,
            alpha = alpha
        )
        plt.show()

    def plot_pop(
        self, 
        sex = None,
        of: str = 'both',
        age_range: Optional[List[int]] = None,
        alpha: float = .5
    ):
        '''
        Plot the barplot of ages vs. end-of-period populations of the
        `of` population table, where ages are filtered by `sex` and 
        `age_range`. Set `alpha` for transparency.

        Usage
        -----
        `self.plot_pop([sex, of, age_range, alpha])`

        Arguments
        ---------
        * `sex`: an object, `None` by default; use only records having the
            same `sex` in table(s) of `self`. If `None`, then the function
            checks if the table has an unique `sex`. If it does, it uses 
            that `sex`; otherwise, it raises an error.
        * `of`: a str, 'both' by default; depending on what population 
            table the user wants to use to draw a plot, either specify
            it as 'orig', 'fixed', or 'both'. Any other string will raise 
            an error.
        * `age_range`: a list of two ints, `None` by default; only the
            records of `of` table having Ages within the closed interval
            defined by this argument are used. If `None`, then all Ages are
            used in the plot.
        * `alpha`: a float, .5 by default; the argument to control the
            transparency of the plot
        '''

        pop_groups = self.__orig_table.get_pop_groups()
        pop_sex = pop_groups[0]
        pop_age = pop_groups[1]
        pop_end = self.__orig_table.get_pop_end()
        if sex is None:
            test_uniqueness = np.unique(self.__orig_table[pop_sex])
            assert len(test_uniqueness) == 1, \
                "There are more than one sex in tables of `self`. " +\
                "Specification of `sex` argument is required."
            sex = test_uniqueness[0]

        if of == 'orig':
            plot_pop(
                poptbl = self.__orig_table, 
                sex = sex,
                age_range = age_range, 
                alpha = alpha
            )
        elif of == 'fixed':
            plot_pop(
                poptbl = self.__fixed_table, 
                sex = sex,
                age_range = age_range, 
                alpha = alpha
            )
        elif of == 'both':
            plot_pop(
                poptbl = self.__orig_table, 
                sex = sex,
                age_range = age_range, 
                alpha = alpha
            )
            plot_pop(
                poptbl = self.__fixed_table, 
                sex = sex,
                age_range = age_range, 
                alpha = alpha
            )
            plt.legend(
                labels = ['Before corrections', 'After corrections'],
                loc = 'upper right'
            )
        else:
            raise NotImplementedError
        plt.title(f"End-of-period population of sex {sex}")
        plt.xlabel(pop_age)
        plt.ylabel(pop_end)
        plt.show()

    def summary(self, include_zeros: bool = False):
        '''
        Get the following information:
            + method used
            + total number of cells changed
            + number of cells changed at each affected column
            + average magnitude of each correction
            + range of each correction
            + standard deviation of each correction
            + average sparsity of each correction
        
        Usage
        -----
        `self.summary(include_zeros)`

        Arguments
        ---------
        * `include_zeros`: a bool, `False` by default; if `True`, then any
            corrections with a value 0 in the correction DataFrame will be
            included in the computation of evaluation metric. 

        Returns
        -------
        A str.
        '''

        summary = ''
        num_cells = self.get_metric_num_cells()
        summary +=\
            f"Method used: {self.__method}\n" +\
            f"Total cells changed: {sum(num_cells.values())}\n"
        
        for k, v in num_cells.items():
            summary += f"    {k}: {v}\n"

        summary +=\
            "Metrics at each correction:\n" +\
            str(self.get_metric_all(include_zeros))

        return summary
