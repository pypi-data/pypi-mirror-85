
from estime2.age import Age
from typing import List
import numpy as np
import pandas as pd



def compute_correction_evaluated_at_func( 
    func, 
    colname: str,
    result_fix_issues: List,
    include_zeros: bool = False,
    *args, 
    **kwargs
):
    '''
    Compute the value of each applied correction in `result_fix_issues`
    evaluated at `func`. Name this quantity as `colname`. Specify 
    positional arguments and keyword arguments of `func` if necessary.

    Details
    -------
    The following for each correction is computed using this function:

        + `func(correction, *args, **kwargs)`
    
    If `include_zeros` is `True` (`False` by default), then zero values
    are included in the correction.
    
    Usage
    -----
    `compute_correction_evaluated_at_func(
        func, 
        colname,
        result_fix_issues, 
        include_zeros, 
        *args, 
        **kwargs
    )`

    Arguments
    ---------
    * `func`: a function that takes `pandas.Series`, and returns a number 
        like `float` and `int`.
    * `colname`: a str; the name of value 
        `func(correction, *args, **kwargs)`.
    * `result_fix_issues`: a list; return value of 
        `ProvPopTable.fix_issues(return_all_mods = True)`.
    * `include_zeros`: a bool, `False` by default; if `True`, then any
        corrections with the value 0 in the correction `Series` will be
        included in the quantity computation.
    * `*args`: positional arguments of `func`
    * `**kwargs`: keyword arguments of `func`

    Returns
    -------
    A `pandas.DataFrame` with columns `sex`, `age`, `comp`, and `colname`,
    where `sex` is a collection of problematic sexes, `age` is a collection
    of problematic ages, `comp` is a collection of names of problematic 
    components, and `colname` a collection of quantitative metrics computed
    at each correction.
    '''

    pop_sex_age = result_fix_issues[0].get_pop_groups()
    get_L_values = None
    if include_zeros:
        get_L_values = lambda sr: sr.iloc[:, -1]
    else:
        get_L_values = lambda sr: sr.iloc[:, -1].loc[lambda x: x != 0]
    
    dat = {}
    dat[pop_sex_age[0]] = []
    dat[pop_sex_age[1]] = []
    dat['Component'] = []
    dat[colname] = []
    for i in range(1, len(result_fix_issues)):
        problematic_sex_age = result_fix_issues[i]\
            .iloc[-1, :]\
            [pop_sex_age]\
            .values
        p_sex = problematic_sex_age[0]
        comp_L_values = get_L_values(result_fix_issues[i])
        p_comp = comp_L_values.name[:-2]
        comp_in_comp_end = p_comp in result_fix_issues[0].get_comp_end()
        modification_age = problematic_sex_age[1]
        m_age_is_max = Age(modification_age).is_max()
        p_age = None
        if (not m_age_is_max) and (not comp_in_comp_end):
            p_age = str(Age(modification_age) + 1)
        else:
            p_age = modification_age
        quant = func(comp_L_values, *args, **kwargs)
        dat[pop_sex_age[0]].append(p_sex)
        dat[pop_sex_age[1]].append(p_age)
        dat['Component'].append(p_comp)
        dat[colname].append(quant)

    return pd.DataFrame(dat)

def get_agediff_range(result_fix_issues: List):
    '''
    Get the difference in the modification age and the minimum 
    counter-adjusted age in each correction of `result_fix_issues`. The 
    smaller, the better.

    Details
    -------
    This function measures how far the correction spans out within the 
    correction.

    Usage
    -----
    `get_agediff_range(result_fix_issues)`

    Argument
    --------
    * `result_fix_issues`: a list; return value of 
        `ProvPopTable.fix_issues(return_all_mods = True)`.
    
    Returns
    -------
    A `pandas.DataFrame` with columns `sex`, `age`, `comp`, and `range`,
    where `sex` is a collection of problematic sexes, `age` is a collection
    of problematic ages, `comp` is a collection of names of problematic 
    components, and `range` a collection of ranges computed at each 
    correction.
    '''

    result = compute_correction_evaluated_at_func(
        func = lambda sr: sr.index.max() - sr.index.min(),
        colname = 'range',
        result_fix_issues = result_fix_issues,
        include_zeros = False
    )

    return result

def get_agediff_sparsity(result_fix_issues: List):
    '''
    Get the mean value of how further away each corrected record is located
    from one another in `result_fix_issues`. The smaller, the better.

    Details
    -------
    This function measures the mean age difference between corrected 
    records according to `result_fix_issues`. For example, if the component
    modification is made at age 96, and counter-adjustments are made to
    ages 95, 93, 91, 90, then this function returns 1.5 because:

    (|96 - 95| + |95 - 93| + |93 - 91| + |91 - 90|) / 4 == 1.5

    Usage
    -----
    `get_agediff_sparsity(result_fix_issues)`

    Argument
    --------
    * `result_fix_issues`: a list; return value of 
        `ProvPopTable.fix_issues(return_all_mods = True)`.
    
    Returns
    -------
    A `pandas.DataFrame` with columns `sex`, `age`, `comp`, and `sparsity`,
    where `sex` is a collection of problematic sexes, `age` is a collection
    of problematic ages, `comp` is a collection of names of problematic 
    components, and `sparsity` a collection of sparsities computed at each 
    correction.
    '''

    result = compute_correction_evaluated_at_func(
        func = lambda sr: np.mean(np.diff(sr.index)),
        colname = 'sparsity',
        result_fix_issues = result_fix_issues,
        include_zeros = False
    )

    return result

def get_correction_magni(
    result_fix_issues: List, 
    include_zeros: bool = False
):
    '''
    Get the magnitude of changes made due to corrections in
    `result_fix_issues`. The smaller, the better.

    Details
    -------
    For each correction applied to a problematic record, the user is able
    to get the log of all corrections applied to `ProvPopTable` via its
    `.fix_issues(return_all_mods = True)` method. Note that the argument
    `return_all_mods` is `True`; it MUST BE.

    Define the magnitude of correction as the mean of absolute values of 
    each correction. That is, for example, the mean of the correction
    (-4, 1, 1, 1) should be (|-4| + |1| + |1| + |1|) / 4 = 1.75. If 
    `include_zeros` is `True` (`False` by default), it counts corrections 
    with a value 0 in the computation of magnitude.

    Usage
    -----
    `get_correction_magni(result_fix_issues, include_zeros)`

    Arguments
    ---------
    * `result_fix_issues`: a list; return value of 
        `ProvPopTable.fix_issues(return_all_mods = True)`.
    * `include_zeros`: a bool, False by default; if `True`, then any
        corrections with a value 0 in the correction DataFrame will be
        included in the magnitude computation.
    
    Returns
    -------
    A `pandas.DataFrame` with columns `sex`, `age`, `comp`, and 
    `magnitude`, where `sex` is a collection of problematic sexes, `age` is
    a collection of problematic ages, `comp` is a collection of names of 
    problematic components, and `magnitude` a collection of magnitudes 
    computed at each correction.
    '''

    result = compute_correction_evaluated_at_func(
        func = lambda sr: np.mean(np.abs(sr)),
        colname = 'magnitude',
        result_fix_issues = result_fix_issues,
        include_zeros = include_zeros
    )

    return result

def get_correction_sd(
    result_fix_issues: List, 
    include_zeros: bool = False
):
    '''
    Compute the standard deviations of corrections applied to
    `result_fix_issues`, a return value of `ProvPopTable.fix_issues()`.
    Let `include_zeros` be `True` if the user wants to count zeros as
    a part of standard deviation computation. The smaller, the better.

    Details
    -------
    For each correction applied to a problematic record, the user is able
    to get the log of all corrections applied to `ProvPopTable` via its
    `.fix_issues(return_all_mods = True)` method. Note that the argument
    `return_all_mods` is `True`; it MUST BE. This function is to compute 
    the standard deviation of each correction. If `include_zeros` is `True`
    (`False` by default), it counts corrections with a value 0 in the 
    computation of standard deviation.

    Usage
    -----
    `get_correction_sd(result_fix_issues, include_zeros)`

    Arguments
    ---------
    * `result_fix_issues`: a list; return value of 
        `ProvPopTable.fix_issues(return_all_mods = True)`.
    * `include_zeros`: a bool, `False` by default; if `True`, then any
        corrections with a value 0 in the correction DataFrame will be
        included in the standard deviation computation.

    Returns
    -------
    A `pandas.DataFrame` with columns `sex`, `age`, `comp`, and `sd`, 
    where `sex` is a collection of problematic sexes, `age` is a 
    collection of problematic ages, `comp` is a collection of names of 
    problematic components, and `sd` a collection of standard deviations 
    computed at each correction.
    '''

    result = compute_correction_evaluated_at_func(
        func = np.std,
        colname = 'sd',
        result_fix_issues = result_fix_issues,
        include_zeros = include_zeros,
        ddof = 1
    )

    return result

def get_num_cells(
    poptbl, 
    result_fix_issues: List, 
    include_zeros: bool = False
):
    '''
    Get the number of modified cells in the table of `result_fix_issues`,
    a return value of `poptbl.fix_issues()`. Include the components with
    zero changes by setting `include_zeros` to be `True`. The smaller, the
    better.

    Details
    -------
    This function compares two tables: `poptbl` and the first item of 
    `poptbl.result_fix_issues(return_all_mods = True)`. It checks which 
    cells have become different from `poptbl` as a result of correction, 
    and calculates the total number of cells that have changed. The
    following information is checked:
    
        + The number of different cells in `poptbl.calculate_pop()` and
            `result_fix_issues[0].calculate_pop()`
        + The number of different cells in corrected negative components
            between `poptbl` and `result_fix_issues[0]`
        + The number of different cells in corrected positive components
            between `poptbl` and `result_fix_issues[0]`
    
    Include the components with zero changes by setting `include_zeros` 
    to be `True`.

    Usage
    -----
    `get_num_cells(poptbl, result_fix_issues, include_zeros)`

    Arguments
    ---------
    * `poptbl`: a `ProvPopTable`
    * `result_fix_issues`: a list; return value of 
        `poptbl.fix_issues(return_all_mods = True)`.
    * `include_zeros`: a bool, `False` by default; if `True`, then all the
        components, including those with zero changes, are included in the
        returning `dict` of this function.
    
    Returns
    -------
    A `dict` with keys `col` (a str), where `col` is either the name of
    the end-of-period population or the name of the corrected component, 
    and `num_cell`, a nonnegative `int`.
    '''

    result = {}

    pop_end = poptbl.get_pop_end()
    poptbl_fixed = result_fix_issues[0]
    pop_end_orig = poptbl.calculate_pop()
    pop_end_fixed = poptbl_fixed.calculate_pop()
    delta_pop_end =\
        (pop_end_orig[pop_end].values != pop_end_fixed[pop_end].values)\
        .sum()
    result[pop_end] = delta_pop_end
    
    all_comps = poptbl.get_comp_neg()
    all_comps.extend(poptbl.get_comp_pos())
    for comp in all_comps:
        before = poptbl[comp].values
        after = poptbl_fixed[comp].values
        delta_comp = (before != after).sum()
        result[comp] = delta_comp

    if not include_zeros:
        for k, v in result.copy().items():
            if v == 0:
                result.pop(k)
    
    return result
