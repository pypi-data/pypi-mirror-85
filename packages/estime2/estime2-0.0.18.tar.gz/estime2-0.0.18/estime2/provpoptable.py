
from estime2.age import Age
from estime2.config import (
    get_option,
    set_option
)
from estime2.helper import (
    diff,
    is_subset,
    raise_if_not_subset,
    return_op_if_None
)
from estime2.provpoptable_resultswrapper import ProvPopTableResultsWrapper
from typing import Collection as Axes
from typing import (
    List,
    Optional,
    Union
)
import numpy as np
import pandas as pd
import warnings

# pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')
Dtype = Union[str, np.dtype, "ExtensionDtype"]



class ProvPopTable(pd.DataFrame):
    '''
    A table of populations and components at a provincial level.
    '''

    def __init__(
        self,
        data = None,
        index: Optional[Axes] = None,
        columns: Optional[Axes] = None,
        dtype: Optional[Dtype] = None,
        copy: bool = False,
        pop_sex: Optional[str] = None,
        pop_age: Optional[str] = None,
        pop_end: Optional[str] = None,
        pop_start: Optional[str] = None,
        pop_birth: Optional[str] = None,
        comp_neg_temp_out: Optional[str] = None,
        comp_neg_emi: Optional[str] = None,
        comp_neg_npr_out: Optional[str] = None,
        comp_neg_death: Optional[str] = None,
        comp_neg_interprov_out: Optional[str] = None,
        comp_neg_etc: Optional[List[str]] = None,
        comp_neg_put_etc_before: Optional[bool] = None,
        comp_pos_temp_in: Optional[str] = None,
        comp_pos_ret_emi: Optional[str] = None,
        comp_pos_npr_in: Optional[str] = None,
        comp_pos_immi: Optional[str] = None,
        comp_pos_interprov_in: Optional[str] = None,
        comp_pos_etc: Optional[List[str]] = None,
        comp_pos_put_etc_before: Optional[bool] = None,
        comp_end: Optional[List[str]] = None,
        reorder_cols: bool = True,
        show_pop_end: bool = False,
        flag: bool = True
    ):
        '''
        Create an instance of ProvPopTable. Note that every cell of the 
        table except for those in the end-of-period population column 
        should have non-negative values.

        Usage
        -----
        PopTable(
            data = None,
            index: Optional[Axes] = None,
            columns: Optional[Axes] = None,
            dtype: Optional[Dtype] = None,
            copy: bool = False,
            pop_sex: Optional[str] = None,
            pop_age: Optional[str] = None,
            pop_end: Optional[str] = None,
            pop_start: Optional[str] = None,
            pop_birth: Optional[str] = None,
            comp_neg_temp_out: Optional[str] = None,
            comp_neg_emi: Optional[str] = None,
            comp_neg_npr_out: Optional[str] = None,
            comp_neg_death: Optional[str] = None,
            comp_neg_interprov_out: Optional[str] = None,
            comp_neg_etc: Optional[List[str]] = None,
            comp_neg_put_etc_before: Optional[bool] = None,
            comp_pos_temp_in: Optional[str] = None,
            comp_pos_ret_emi: Optional[str] = None,
            comp_pos_npr_in: Optional[str] = None,
            comp_pos_immi: Optional[str] = None,
            comp_pos_interprov_in: Optional[str] = None,
            comp_pos_etc: Optional[List[str]] = None,
            comp_pos_put_etc_before: Optional[bool] = None,
            comp_end: Optional[List[str]] = None,
            reorder_cols: bool = True,
            show_pop_end: bool = False,
            flag: bool = True
        )

        Arguments
        ---------
        * `data`, `index`, `columns`, `dtype`, `copy`: inherited from 
            `pandas.DataFrame`
        * `pop_sex`: (`None` by default) a str; the name that denotes the 
            sex in the population table. If `None`, it first checks whether
            the global option value `pop.sex` is one of the column names 
            in the population table. If it is, the column having the same 
            name as `pop.sex` is selected as the sex column. If not, the 
            method assumes that records in the population table all have 
            the (unknown) same sex, creates the sex column with the
            `pop.sex` value as the name, and broadcasts `0` in the new
            column.
        * `pop_age`: (`None` by default) a str; the name that denotes the 
            age in the population table. If `None`, it first checks whether 
            the global option value `pop.age` is one of the column names
            in the population table. If it is, the column having the same
            name as `pop.age` is selected as the age column. If not, the
            method raises `AssertionError`, i.e. the age column must be
            initialized in the population table.
        * `pop_end`: (`None` by default) a str; the name that denotes 
            the end-of-period population in the population table. If 
            `None`, it uses the global option value `pop.end` as the name 
            of the end-of-period population column in the table. 
        * `pop_start`: (`None` by default) a str; the name that denotes 
            the start-of-period population in the population table. If 
            `None`, it first checks whether the global option value 
            `pop.start` is one of the column names in the population table.
            If it is, the column having the same name as `pop.start` is
            selected as the start-of-period population column. If not, the
            method raises `AssertionError`, i.e. the start-of-period
            population column must be initialized in the population table.
        * `pop_birth`: (`None` by default) a str; the name that denotes 
            the birth in the population table. If `None`, it first checks 
            whether the global option value `pop.birth` is one of the 
            column names in the population table. If it is, the column 
            having the same name as `pop.birth` is selected as the birth
            column. If not, the method raises `AssertionError`, i.e. the 
            birth column must be initialized in the population table.
        * `comp_neg_temp_out`: (`None` by default) a str; the name of
            the column corresponding to "Temporary emigrants OUT" in the
            population table. If `None`, it first checks whether the 
            global option value `comp_neg.temp_out` is also `None`. If it
            is also `None`, the "Temporary emigrants OUT" component is
            discarded from the population table (i.e. not shown and not 
            used). If it is not `None`, the method then checks whether the
            value `comp_neg.temp_out` is one of the column names in the 
            population table. If it is, the column having the same name as
            `comp_neg.temp_out` is selected as the 
            "Temporary emigrants OUT" column. If not, the method raises
            `AssertionError`.
        * `comp_neg_emi`: (`None` by default) a str; the name of
            the column corresponding to "Emigrants" in the
            population table. If `None`, it first checks whether the 
            global option value `comp_neg.emi` is also `None`. If it
            is also `None`, the "Emigrants" component is
            discarded from the population table (i.e. not shown and not 
            used). If it is not `None`, the method then checks whether the
            value `comp_neg.emi` is one of the column names in the 
            population table. If it is, the column having the same name as
            `comp_neg.emi` is selected as the 
            "Emigrants" column. If not, the method raises
            `AssertionError`.
        * `comp_neg_npr_out`: (`None` by default) a str; the name of
            the column corresponding to "Non-permanent residents OUT" in 
            the population table. If `None`, it first checks whether the 
            global option value `comp_neg.npr_out` is also `None`. If it
            is also `None`, the "Non-permanent residents OUT" component is
            discarded from the population table (i.e. not shown and not 
            used). If it is not `None`, the method then checks whether the
            value `comp_neg.npr_out` is one of the column names in the 
            population table. If it is, the column having the same name as
            `comp_neg.npr_out` is selected as the 
            "Non-permanent residents OUT" column. If not, the method raises
            `AssertionError`.
        * `comp_neg_death`: (`None` by default) a str; the name of
            the column corresponding to "Deaths" in the
            population table. If `None`, it first checks whether the 
            global option value `comp_neg.death` is also `None`. If it
            is also `None`, the "Deaths" component is
            discarded from the population table (i.e. not shown and not 
            used). If it is not `None`, the method then checks whether the
            value `comp_neg.death` is one of the column names in the 
            population table. If it is, the column having the same name as
            `comp_neg.death` is selected as the 
            "Deaths" column. If not, the method raises
            `AssertionError`.
        * `comp_neg_interprov_out`: (`None` by default) a str; the name of
            the column corresponding to "Interprovincial migrant OUT" in 
            the population table. If `None`, it first checks whether the 
            global option value `comp_neg.interprov_out` is also `None`. 
            If it is also `None`, the "Interprovincial migrant OUT" 
            component is discarded from the population table (i.e. not 
            shown and not used). If it is not `None`, the method then 
            checks whether the value `comp_neg.interprov_out` is one of the
            column names in the population table. If it is, the column 
            having the same name as `comp_neg.interprov_out` is selected as
            the "Interprovincial migrant OUT" column. If not, the method 
            raises `AssertionError`.
        * `comp_neg_etc`: (`None` by default) a list of str; the names of
            columns corresponding to the remaining negative components
            in the population table. If `None`, it first checks whether the
            global option value `comp_neg.etc` is `[]`, an empty list. If
            it is an empty list, then it assumes no extra negative 
            component is given in the table, and therefore not used. If it
            is not `None`, the method then checks whether the value of
            `comp_neg.etc` itself is a subset of all the column names in
            the population table. If it is, the column(s) in `comp_neg.etc`
            is used in the computation of end-of-period populations as well
            as in the correction process. If not, the method raises 
            `AssertionError`.
        * `comp_neg_put_etc_before`: (`None` by default) a bool; if `True`,
            then components in `comp_neg.etc` will precede 
            `comp_neg.interprov_out` and follow other conventional negative
            components. If `False`, components will follow 
            `comp_neg.interprov_out` instead. If `None`, then it uses a 
            global option value `estime2.options.comp_neg.put_etc_before` 
            (`False` by default).
        * `comp_pos_temp_in`: (`None` by default) a str; the name of
            the column corresponding to "Temporary emigrants IN" in the
            population table. If `None`, it first checks whether the 
            global option value `comp_pos.temp_in` is also `None`. If it
            is also `None`, the "Temporary emigrants IN" component is
            discarded from the population table (i.e. not shown and not 
            used). If it is not `None`, the method then checks whether the
            value `comp_pos.temp_in` is one of the column names in the 
            population table. If it is, the column having the same name as
            `comp_pos.temp_in` is selected as the 
            "Temporary emigrants IN" column. If not, the method raises
            `AssertionError`.
        * `comp_pos_ret_emi`: (`None` by default) a str; the name of the 
            column corresponding to "Returning emigrants" in the population
            table. If `None`, it first checks whether the global option 
            value `comp_pos.ret_emi` is also `None`. If it is also `None`, 
            the "Returning emigrants" component is discarded from the 
            population table (i.e. not shown and not used). If it is not 
            `None`, the method then checks whether the value 
            `comp_pos.ret_emi` is one of the column names in the population
            table. If it is, the column having the same name as 
            `comp_pos.ret_emi` is selected as the "Returning emigrants" 
            column. If not, the method raises `AssertionError`.
        * `comp_pos_npr_in`: (`None` by default) a str; the name of the 
            column corresponding to "Non-permanent residents IN" in the 
            population table. If `None`, it first checks whether the global
            option value `comp_pos.npr_in` is also `None`. If it is also 
            `None`, the "Non-permanent residents IN" component is discarded
            from the population table (i.e. not shown and not used). If it
            is not `None`, the method then checks whether the value 
            `comp_pos.npr_in` is one of the column names in the population
            table. If it is, the column having the same name as 
            `comp_pos.npr_in` is selected as the 
            "Non-permanent residents IN" column. If not, the method raises
            `AssertionError`.
        * `comp_pos_immi`: (`None` by default) a str; the name of the 
            column corresponding to "Immigrants" in the population table.
            If `None`, it first checks whether the global option value 
            `comp_pos.immi` is also `None`. If it is also `None`, the 
            "Immigrants" component is discarded from the population table 
            (i.e. not shown and not used). If it is not `None`, the method
            then checks whether the value `comp_pos.immi` is one of the 
            column names in the population table. If it is, the column 
            having the same name as `comp_pos.immi` is selected as the 
            "Immigrants" column. If not, the method raises 
            `AssertionError`.
        * `comp_pos_interprov_in`: (`None` by default) a str; the name of
            the column corresponding to "Interprovincial migrant IN" in the
            population table. If `None`, it first checks whether the global
            option value `comp_pos.interprov_in` is also `None`. If it is 
            also `None`, the "Interprovincial migrant IN" component is 
            discarded from the population table (i.e. not shown and not 
            used). If it is not `None`, the method then checks whether the
            value `comp_pos.interprov_in` is one of the column names in 
            the population table. If it is, the column having the same name
            as `comp_pos.interprov_in` is selected as the 
            "Interprovincial migrant IN" column. If not, the method raises
            `AssertionError`.
        * `comp_pos_etc`: (`None` by default) a list of str; the names of
            columns corresponding to the remaining positive components
            in the population table. If `None`, it first checks whether the
            global option value `comp_pos.etc` is `[]`, an empty list. If
            it is an empty list, then it assumes no extra positive 
            component is given in the table, and therefore not used. If it
            is not `None`, the method then checks whether the value of
            `comp_pos.etc` itself is a subset of all the column names in
            the population table. If it is, the column(s) in `comp_pos.etc`
            is used in the computation of end-of-period populations as well
            as in the correction process. If not, the method raises 
            `AssertionError`.
        * `comp_pos_put_etc_before`: (`None` by default) a bool; if `True`,
            then components in `comp_pos.etc` will precede 
            `comp_pos.interprov_in` and follow other conventional positive
            components. If `False`, components will follow 
            `comp_pos.interprov_in` instead. If `None`, then it uses a 
            global option value `estime2.options.comp_pos.put_etc_before` 
            (`False` by default).
        * `comp_end`: (`None` by default) a list of str; component(s) that
            is/are recorded at the end of the period. If `None`, then
            the global option value `comp.end` is used.
        * `reorder_cols`: (`True` by default) a boolean; if True, reorder 
            columns of ProvPopTable as specified by above arguments. See
            the item 8 in Details.
        * `show_pop_end`: (`False` by default) a boolean; if True, leave
            end-of-period population in a ProvPopTable, and discard it
            otherwise.
        * `flag`: (`True` by default) a boolean; leave this argument as
            `True`. This argument is for stopping the recursion in
            `ProvPopTable.__init__()`.
        
        Details
        -------
        1. `data`, `index`, `columns`, `dtype`, and `copy` are arguments to
            create an instance of `pandas.DataFrame`.
        2. A numeric values in any cell of the table should be nonnegative.
        3. Any missing value in `data` is filled with `0`.
        4. If `None` is supplied to the argument starting with either `pop`
            or `comp`, the global option value is used. For example, if
            `pop_sex = None`, then the corresponding global option 
            `estime2.options.pop.sex` is used, which is `'Sex'` by
            default.
        5. Any global option corresponding to the arguments with the 
            pattern `pop_*` cannot have `None` as its value. For example,
            `estime2.options.pop.age = None` raises an error.
        6. Any global option corresponding to the arguments with the
            pattern `comp_*` except `comp_end` and `comp_*.*etc*` may have
            `None` as its value. In case where both the argument and the 
            corresponding global option are `None`, the corresponding 
            column is discarded from the table (i.e. not shown and not 
            present in the table).
        7. Argument values have precedence over global option values. That
            is, if the argument value and the corresponding global option 
            value are different, this `__init__` method uses the argument 
            value.
        8. If `reorder_cols` is `True`, then the columns of `data` is
            reordered in the following order from the left. For a column
            corresponding to one of the `comp_*` arguments, it will be
            displayed in the table iff neither the argument nor the 
            corresponding global option is `None` or `[]`: 
                + `pop_sex`
                + `pop_age`
                + `pop_end` (if `show_pop_end` is True)
                + `pop_start`
                + `pop_birth`
                + `comp_neg_temp_out` 
                + `comp_neg_emi`
                + `comp_neg_npr_out`
                + `comp_neg_death`
                + `comp_neg_etc` (if given any & put_etc_before is True)
                + `comp_neg_interprov_out`
                + `comp_neg_etc` (if given any & put_etc_before is False)
                + `comp_pos_temp_in`
                + `comp_pos_ret_emi`
                + `comp_pos_npr_in`
                + `comp_pos_immi`
                + `comp_pos_etc` (if given any & put_etc_before is True)
                + `comp_pos_interprov_in`
                + `comp_pos_etc` (if given any & put_etc_before is False)
        9. Whether or not `reorder_cols` is `True`, the method looks for
            the component(s) responsible for the negative end-of-period
            population following the above order of `comp_*`'s.
        '''

        # Inherit from pandas.DataFrame
        super().__init__(data, index, columns, dtype, copy)
        self.fillna(0, inplace = True)

        opname_arg = {
            'pop.sex': pop_sex,
            'pop.age': pop_age,
            'pop.end': pop_end,
            'pop.start': pop_start,
            'pop.birth': pop_birth,
            'comp_neg.temp_out': comp_neg_temp_out, 
            'comp_neg.emi': comp_neg_emi, 
            'comp_neg.npr_out': comp_neg_npr_out,
            'comp_neg.death': comp_neg_death, 
            'comp_neg.interprov_out': comp_neg_interprov_out,
            'comp_neg.etc': comp_neg_etc,
            'comp_neg.put_etc_before': comp_neg_put_etc_before,
            'comp_pos.temp_in': comp_pos_temp_in, 
            'comp_pos.ret_emi': comp_pos_ret_emi, 
            'comp_pos.npr_in': comp_pos_npr_in,
            'comp_pos.immi': comp_pos_immi, 
            'comp_pos.interprov_in': comp_pos_interprov_in,
            'comp_pos.etc': comp_pos_etc,
            'comp_pos.put_etc_before': comp_pos_put_etc_before,
            'comp.end': comp_end
        }
        for opname, arg in opname_arg.copy().items():
            opname_arg[opname] = return_goption_if_None(opname, arg)

        for opname2 in opname_arg.keys():
            if opname2 != 'comp.end':
                prev_op = get_option(opname2)
                set_option(opname2, opname_arg[opname2])
                set_option(opname2, prev_op)
            else:
                raise_if_not_subset(
                    opname_arg[opname2],
                    [
                        opname_arg['comp_neg.temp_out'], 
                        opname_arg['comp_neg.emi'],
                        opname_arg['comp_neg.npr_out'],
                        opname_arg['comp_neg.death'],
                        opname_arg['comp_neg.interprov_out']
                    ] +\
                    opname_arg['comp_neg.etc'] +\
                    [
                        opname_arg['comp_pos.temp_in'],
                        opname_arg['comp_pos.ret_emi'],
                        opname_arg['comp_pos.npr_in'],
                        opname_arg['comp_pos.immi'],
                        opname_arg['comp_pos.interprov_in']
                    ] +\
                    opname_arg['comp_pos.etc'],
                    'comp_end',
                    'components'
                )

        all_cols = self.columns.tolist()
        all_name = 'self.columns'
        for opname3, arg3 in opname_arg.items():
            if opname3 == 'pop.sex':
                if is_subset([arg3], all_cols):
                    continue
                else:
                    self[arg3] = 0
            if opname3 == 'pop.end':
                continue
            if arg3 is not None:
                # Note: the only way arg3 is None at this point is when 
                # both the provided argument as well as the corresponding 
                # global option are None.
                # If the validator of the corresponding global option 
                # does NOT allow NoneType, then opname3 is checked for
                # whether it is a subset of all_cols.
                if opname3 in [
                    'comp_neg.put_etc_before',
                    'comp_pos.put_etc_before'
                ]:
                    continue
                elif opname3 not in [
                    'comp.end', 'comp_neg.etc', 'comp_pos.etc'
                ]:
                    raise_if_not_subset(
                        [arg3], all_cols, 
                        opname3.replace('.', '_'), all_name
                    )
                else:
                    raise_if_not_subset(
                        arg3, all_cols, 
                        opname3.replace('.', '_'), all_name
                    )
        if show_pop_end:
            raise_if_not_subset(
                [opname_arg['pop.end']], all_cols,
                'pop_end', all_name
            )

        reordered_cols1 = [opname_arg['pop.sex'], opname_arg['pop.age']]
        reordered_cols2 = []
        if show_pop_end:
            reordered_cols2.append(opname_arg['pop.end'])
        reordered_cols2.append(opname_arg['pop.start'])
        reordered_cols2.append(opname_arg['pop.birth'])

        comp_negs = [
            'comp_neg.temp_out', 'comp_neg.emi', 'comp_neg.npr_out',
            'comp_neg.death'
        ]
        if opname_arg['comp_neg.put_etc_before']:
            comp_negs.append('comp_neg.etc')
        comp_negs.append('comp_neg.interprov_out')
        if not opname_arg['comp_neg.put_etc_before']:
            comp_negs.append('comp_neg.etc')
        comp_poss = [
            'comp_pos.temp_in', 'comp_pos.ret_emi', 'comp_pos.npr_in',
            'comp_pos.immi'
        ]
        if opname_arg['comp_pos.put_etc_before']:
            comp_poss.append('comp_pos.etc')
        comp_poss.append('comp_pos.interprov_in')
        if not opname_arg['comp_pos.put_etc_before']:
            comp_poss.append('comp_pos.etc')
        comp_ordered = comp_negs + comp_poss

        for comp in comp_ordered:
            if opname_arg[comp] is not None:
                if isinstance(opname_arg[comp], list):
                    reordered_cols2.extend(opname_arg[comp])
                else:
                    reordered_cols2.append(opname_arg[comp])
        reordered_cols = reordered_cols1 + reordered_cols2

        self[opname_arg['pop.age']] =\
            self[opname_arg['pop.age']].apply(Age)
        agg_cols = {}
        for col in reordered_cols2:
            self[col] = self[col].apply(int)
            agg_cols[col] = 'sum'

        self.__pop_sex = opname_arg['pop.sex']
        self.__pop_age = opname_arg['pop.age']
        self.__pop_end = opname_arg['pop.end']
        self.__pop_start = opname_arg['pop.start']
        self.__pop_birth = opname_arg['pop.birth']
        self.__comp_neg_temp_out = opname_arg['comp_neg.temp_out']
        self.__comp_neg_emi = opname_arg['comp_neg.emi']
        self.__comp_neg_npr_out = opname_arg['comp_neg.npr_out']
        self.__comp_neg_death = opname_arg['comp_neg.death']
        self.__comp_neg_interprov_out = opname_arg['comp_neg.interprov_out']
        self.__comp_neg_etc = opname_arg['comp_neg.etc']
        self.__comp_neg_put_etc_before = opname_arg['comp_neg.put_etc_before']
        self.__comp_pos_temp_in = opname_arg['comp_pos.temp_in']
        self.__comp_pos_ret_emi = opname_arg['comp_pos.ret_emi']
        self.__comp_pos_npr_in = opname_arg['comp_pos.npr_in']
        self.__comp_pos_immi = opname_arg['comp_pos.immi']
        self.__comp_pos_interprov_in = opname_arg['comp_pos.interprov_in']
        self.__comp_pos_etc = opname_arg['comp_pos.etc']
        self.__comp_pos_put_etc_before = opname_arg['comp_pos.put_etc_before']
        self.__comp_end = opname_arg['comp.end']

        if reorder_cols:
            self.__init__(
                self.loc[:, reordered_cols]\
                    .groupby(reordered_cols1)\
                    .agg(agg_cols)\
                    .reset_index(),
                pop_sex = opname_arg['pop.sex'],
                pop_age = opname_arg['pop.age'],
                pop_end = opname_arg['pop.end'],
                pop_start = opname_arg['pop.start'],
                pop_birth = opname_arg['pop.birth'],
                comp_neg_temp_out = opname_arg['comp_neg.temp_out'],
                comp_neg_emi = opname_arg['comp_neg.emi'],
                comp_neg_npr_out = opname_arg['comp_neg.npr_out'],
                comp_neg_death = opname_arg['comp_neg.death'],
                comp_neg_interprov_out = opname_arg['comp_neg.interprov_out'],
                comp_neg_etc = opname_arg['comp_neg.etc'],
                comp_neg_put_etc_before = opname_arg['comp_neg.put_etc_before'],
                comp_pos_temp_in = opname_arg['comp_pos.temp_in'],
                comp_pos_ret_emi = opname_arg['comp_pos.ret_emi'],
                comp_pos_npr_in = opname_arg['comp_pos.npr_in'],
                comp_pos_immi = opname_arg['comp_pos.immi'],
                comp_pos_interprov_in = opname_arg['comp_pos.interprov_in'],
                comp_pos_etc = opname_arg['comp_pos.etc'],
                comp_pos_put_etc_before = opname_arg['comp_pos.put_etc_before'],
                comp_end = opname_arg['comp.end'],
                reorder_cols = False,
                show_pop_end = show_pop_end,
                flag = False
            )
            return None

        if flag:
            agg_cols2 = {}
            for orig_col in all_cols.copy():
                if orig_col not in reordered_cols:
                    all_cols.remove(orig_col)
                if orig_col in reordered_cols2:
                    agg_cols2[orig_col] = 'sum'

            self.__init__(
                self.loc[:, all_cols]\
                    .groupby(reordered_cols1)\
                    .agg(agg_cols2)\
                    .reset_index(),
                pop_sex = opname_arg['pop.sex'],
                pop_age = opname_arg['pop.age'],
                pop_end = opname_arg['pop.end'],
                pop_start = opname_arg['pop.start'],
                pop_birth = opname_arg['pop.birth'],
                comp_neg_temp_out = opname_arg['comp_neg.temp_out'],
                comp_neg_emi = opname_arg['comp_neg.emi'],
                comp_neg_npr_out = opname_arg['comp_neg.npr_out'],
                comp_neg_death = opname_arg['comp_neg.death'],
                comp_neg_interprov_out = opname_arg['comp_neg.interprov_out'],
                comp_neg_etc = opname_arg['comp_neg.etc'],
                comp_neg_put_etc_before = opname_arg['comp_neg.put_etc_before'],
                comp_pos_temp_in = opname_arg['comp_pos.temp_in'],
                comp_pos_ret_emi = opname_arg['comp_pos.ret_emi'],
                comp_pos_npr_in = opname_arg['comp_pos.npr_in'],
                comp_pos_immi = opname_arg['comp_pos.immi'],
                comp_pos_interprov_in = opname_arg['comp_pos.interprov_in'],
                comp_pos_etc = opname_arg['comp_pos.etc'],
                comp_pos_put_etc_before = opname_arg['comp_pos.put_etc_before'],
                comp_end = opname_arg['comp.end'],
                reorder_cols = False,
                show_pop_end = show_pop_end,
                flag = False
            )

    def __setattr__(self, name, value):
        '''
        Set an attribute of ProvPopTable. This method is defined to 
        override `pandas.DataFrame.__setattr__(name, value)` in 
        `ProvPopTable.__init__()`.

        Usage
        -----
        `ProvPopTable.name = value`

        Arguments
        ---------
        * self: a ProvPopTable
        * name: a string (when using setattr()) or an expression (when
            using PopTable.__setattr__())
        * value: any type
        '''

        allowed_attrs = [
            '_ProvPopTable__pop_sex',
            '_ProvPopTable__pop_age', 
            '_ProvPopTable__pop_end',
            '_ProvPopTable__pop_start',
            '_ProvPopTable__pop_birth',
            '_ProvPopTable__comp_neg_temp_out', 
            '_ProvPopTable__comp_neg_emi', 
            '_ProvPopTable__comp_neg_npr_out', 
            '_ProvPopTable__comp_neg_death', 
            '_ProvPopTable__comp_neg_interprov_out',
            '_ProvPopTable__comp_neg_etc', 
            '_ProvPopTable__comp_neg_put_etc_before',
            '_ProvPopTable__comp_pos_temp_in',
            '_ProvPopTable__comp_pos_ret_emi',
            '_ProvPopTable__comp_pos_npr_in',
            '_ProvPopTable__comp_pos_immi',
            '_ProvPopTable__comp_pos_interprov_in',
            '_ProvPopTable__comp_pos_etc',
            '_ProvPopTable__comp_pos_put_etc_before',
            '_ProvPopTable__comp_end'
        ]
        if name in allowed_attrs:
            self.__dict__[name] = value
        else:
            super().__setattr__(name, value)

    def calculate_pop(
        self,
        comp_neg: Optional[List[str]] = None,
        comp_pos: Optional[List[str]] = None,
        return_comps: bool = False
    ):
        '''
        Calculate the end-of-period population using the components
        specified in `comp_neg` and `comp_pos`. Let `return_comps` be 
        `True` if one wants to see the component values used.

        Usage
        -----
        `ProvPopTable.calculate_pop(comp_neg, comp_pos, return_comps)`

        Details
        -------
        Based on the component method, this computes the end-of-period
        population for each sex and age. For example, the end-of-period
        population of males aged 95 is computed using the components of
        the male record at age 94, NOT at age 95. The arguments except 
        `self` are used to compute the "intermediate" end-of-period 
        population to find the problematic component that causes a negative
        end-of-period population. If the user wants to pass no component,
        pass the empty list `[]` instead of `None` to the argument(s).

        Arguments
        ---------
        * `comp_neg`, `comp_pos`: (None by default) a list of
            str; a list of components to use to compute the end-of-period 
            population. `comp_neg` must be a subset of 
            `self.get_comp_neg()`, and `comp_pos` must be a subset of 
            `self.get_comp_pos()`. If None, it uses all the available 
            components in `self`. If both are `[]`, the method returns
            the sum of the start-of-period population and birth at each
            sex-age level.
        * `return_comps`: (False by default) a bool; if `True`, return the
            component values used to compute the end-of-period population.
        '''

        comp_neg = return_op_if_None(self.get_comp_neg(), comp_neg)
        comp_pos = return_op_if_None(self.get_comp_pos(), comp_pos)
        raise_if_not_subset(
            comp_neg, self.get_comp_neg(),
            'comp_neg', 'negative components'
        )
        raise_if_not_subset(
            comp_pos, self.get_comp_pos(),
            'comp_pos', 'positive components'
        )

        pop_end = self.__pop_end
        pop_groups = self.get_pop_groups()
        comps = comp_neg + comp_pos
        comp_end = self.__comp_end
        comp_not_end = []
        if comps != []:
            for comp in comps:
                if comp not in comp_end:
                    comp_not_end.append(comp)
        
        comp_aggs = {}
        comp_aggs[self.__pop_start] = 'sum'
        comp_aggs[self.__pop_birth] = 'sum'
        if comps != []:
            for comp2 in comp_not_end:
                comp_aggs[comp2] = 'sum' 

        result1 = self.loc[
            :, 
            pop_groups +\
                [self.__pop_start, self.__pop_birth] +\
                comp_not_end
        ]
        result1[self.__pop_age] += 1
        result1 = result1\
            .groupby(pop_groups)\
            .agg(comp_aggs)\
            .reset_index()
        if comps == []:
            result1[self.__pop_end] =\
                result1[self.__pop_start] + result1[self.__pop_birth]
            result = result1.loc[:, pop_groups + [self.__pop_end]]
            return result

        result2 = self.loc[:, pop_groups + comp_end]
        result2 = result2.loc[lambda df: df[self.__pop_age] != -1]

        result1[self.__pop_age] = result1[self.__pop_age].apply(str)
        result2[self.__pop_age] = result2[self.__pop_age].apply(str)
        result3 = result1\
            .merge(
                result2,
                how = 'left',
                on = pop_groups
            )
        result3[self.__pop_age] = result3[self.__pop_age].apply(Age)
        result3[pop_end] =\
            result3[self.__pop_start] + result3[self.__pop_birth]
        if comp_neg != []:
            for col_neg in comp_neg:
                result3[pop_end] -= result3[col_neg]
        if comp_pos != []:
            for col_pos in comp_pos:
                result3[pop_end] += result3[col_pos]

        cols_to_display = pop_groups + [pop_end]
        if return_comps:
            cols_to_display +=\
                [self.__pop_start, self.__pop_birth] +\
                comp_neg + comp_pos
        result = result3.loc[:, cols_to_display]

        return result

    def fix_issues(
        self, 
        method: Optional[str] = None, 
        return_all_mods: bool = False
    ):
        '''
        Apply modifications and counter-adjustments to `self` so that there
        are no negative end-of-period population. Figures for counter-
        adjustments in neighbouring ages are different based on `method`
        specified. Set `return_all_mods` to `True` to get all the 
        modifications and counter-adjustments made to `self`.

        Details
        -------
        For each problematic record, it modifies problematic record(s) and
        makes counter-adjustments to records of neighbouring ages within a 
        component according to the `method` specified. For each component, 
        the modification and counter-adjustments made to that component of 
        `self` will affect the end-of-period population. The process is 
        done until no new end-of-period population is negative.
        In case of "Interprovincial migration OUT" or "Interprovincial
        migration IN" is modified, this method records how much of
        modification and counter-adjustments are made so that the
        "counter-counter-adjustments" should be made to the other 
        provincial table(s).

        Usage
        -----
        `ProvPopTable.fix_issues(method, return_all_mods)`

        Argument
        --------
        * `method`: the same argument as in `self.get_K(comp, method, J)`.
        * `return_all_mods`: a bool (`False` by default); if `True`, this 
            will return all the modifications and counter-adjustments made
            to `self`.

        Returns
        -------
        If `return_all_mods` is `False`, then it returns a fixed version
        of `self`, the current `ProvPopTable`. 
        If `return_all_mods` is `True` and there are NO corrections made
        to the original table, then it returns `self`, the current 
        `ProvPopTable`.
        If `return_all_mods` is `True` and there are ANY corrections made
        to the original table, then it returns a 
        `ProvPopTableResultsWrapper`.
        '''

        args_in_self = {
            'pop.sex': self.__pop_sex,
            'pop.age': self.__pop_age,
            'pop.end': self.__pop_end,
            'pop.start': self.__pop_start,
            'pop.birth': self.__pop_birth,
            'comp_neg.temp_out': self.__comp_neg_temp_out,
            'comp_neg.emi': self.__comp_neg_emi,
            'comp_neg.npr_out': self.__comp_neg_npr_out,
            'comp_neg.death': self.__comp_neg_death,
            'comp_neg.interprov_out': self.__comp_neg_interprov_out,
            'comp_neg.etc': self.__comp_neg_etc,
            'comp_neg.put_etc_before': self.__comp_neg_put_etc_before,
            'comp_pos.temp_in': self.__comp_pos_temp_in,
            'comp_pos.ret_emi': self.__comp_pos_ret_emi,
            'comp_pos.npr_in': self.__comp_pos_npr_in,
            'comp_pos.immi': self.__comp_pos_immi,
            'comp_pos.interprov_in': self.__comp_pos_interprov_in,
            'comp_pos.etc': self.__comp_pos_etc,
            'comp_pos.put_etc_before': self.__comp_pos_put_etc_before,
            'comp.end': self.__comp_end,
        }
        prevs = {}
        for k, v in args_in_self.items():
            prevs[k] = get_option(k)
            set_option(k, v)

        comp_neg_to_use = self.get_comp_neg()
        comp_pos_to_use = self.get_comp_pos()
        comps = comp_neg_to_use + comp_pos_to_use

        pop_groups = self.get_pop_groups()
        all_cols = self.columns.tolist()
        show_pop_end = self.__pop_end in all_cols
        comps_modified = []
        sexes = np.unique(self[self.__pop_sex])
        self_copy = None
        method = return_goption_if_None('method', method)

        for sex in sexes:
            self_cp_sex =\
                self.copy().loc[lambda df: df[self.__pop_sex] == sex]
            self_cp_sex = ProvPopTable(
                self_cp_sex,
                reorder_cols = False, # since it is reordered already
                show_pop_end = show_pop_end,
                # since records are grouped + summarized by 
                # sex and age already
                flag = False
            )
            # `flag` is True iff `I` has at least one nonzero value
            flag = (sum(self_cp_sex.get_I()['I'].values != 0) != 0)
            i = 0
            num_zeros = sum(self_cp_sex.get_I()['I'].values == 0)
            while flag:
                comp = comps[i]
                comp_L = f"{comp}_L"
                L = self_cp_sex.get_L(comp, method)
                if return_all_mods:
                    if any(L[comp_L].values != 0):
                        comps_modified.append(L)
                L[self.__pop_age] =\
                    L[self.__pop_age].apply(str)
                self_cp_sex[self.__pop_age] =\
                    self_cp_sex[self.__pop_age].apply(str)
                self_cp_sex = self_cp_sex\
                    .merge(L, on = pop_groups, how = 'left')
                self_cp_sex.fillna(0, inplace = True)
                self_cp_sex[comp_L] = self_cp_sex[comp_L].apply(int)
                self_cp_sex[comp] += self_cp_sex[comp_L]
                del self_cp_sex[comp_L]

                self_cp_sex = ProvPopTable(
                    self_cp_sex,
                    reorder_cols = False, # since it is reordered already
                    show_pop_end = show_pop_end,
                    # since records are grouped + summarized by 
                    # sex and age already
                    flag = False                
                )

                I_vec = self_cp_sex.get_I()['I'].values
                new_num_zeros = sum(I_vec == 0)
                if all(I_vec == 0):
                    # all problematic records fixed
                    flag = False # stop the while-loop iteration
                elif num_zeros != new_num_zeros:
                    # one problematic record fixed
                    i = 0 # move to the next problematic record
                    num_zeros = new_num_zeros # assign a new number
                elif i != (len(comps) - 1): 
                    # correction in progress
                    i += 1
                else: 
                    # i.e. lack of values for corrections
                    # Correction could not be made to the problematic 
                    # record at the youngest age.
                    # If the youngest problematic record cannot be fixed, 
                    # then any older problematic records cannot be fixed 
                    # either.
                    # intraprov_in or intraprov_out should be modified 
                    # in SubProvPopTable
                    flag = False

            if self_copy is None:
                self_copy = self_cp_sex
            else:
                self_copy = self_copy\
                    .append(self_cp_sex, ignore_index = True)

        self_copy = ProvPopTable(
            self_copy.sort_values(pop_groups),
            reorder_cols = False, # since it is reordered already
            show_pop_end = show_pop_end,
            # since records are grouped + summarized by 
            # sex and age already
            flag = False            
        )

        for k2, v2 in prevs.items():
            set_option(k2, v2)

        if return_all_mods:
            if comps_modified == []:
                return self_copy
            result = ProvPopTableResultsWrapper(
                orig_table = self, 
                result_fix_issues = [self_copy] + comps_modified,
                method = method
            )
            return result
        else:
            return self_copy

    def get_comp_end(self):
        '''
        Get the component(s) recorded at the end of the period.

        Usage
        -----
        `ProvPopTable.get_comp_end()`
        '''

        return self.__comp_end

    def get_comp_neg(self):
        '''
        Get the negative components of self.

        Usage
        -----
        `ProvPopTable.get_comp_neg()`
        '''

        result = []
        result.append(self.__comp_neg_temp_out)
        result.append(self.__comp_neg_emi)
        result.append(self.__comp_neg_npr_out)
        result.append(self.__comp_neg_death)
        if self.__comp_neg_put_etc_before:
            result.extend(self.__comp_neg_etc)
        result.append(self.__comp_neg_interprov_out)
        if not self.__comp_neg_put_etc_before:
            result.extend(self.__comp_neg_etc)
        for comp in result.copy():
            if comp is None:
                result.remove(comp)
        
        return result

    def get_comp_pos(self):
        '''
        Get the positive components of self.

        Usage
        -----
        `ProvPopTable.get_comp_pos()`
        '''

        result = []
        result.append(self.__comp_pos_temp_in)
        result.append(self.__comp_pos_ret_emi)
        result.append(self.__comp_pos_npr_in)
        result.append(self.__comp_pos_immi)
        if self.__comp_pos_put_etc_before:
            result.extend(self.__comp_pos_etc)
        result.append(self.__comp_pos_interprov_in)
        if not self.__comp_pos_put_etc_before:
            result.extend(self.__comp_pos_etc)
        for comp in result.copy():
            if comp is None:
                result.remove(comp)

        return result

    def get_pop_end(self):
        '''
        Get self.__pop_end, the name of the end-of-period population.

        Usage
        -----
        `ProvPopTable.get_pop_end()`
        '''

        return self.__pop_end

    def get_pop_groups(self):
        '''
        Get self.__pop_sex and self.__pop_age, the names of sex and age
        columns.

        Usage
        -----
        `ProvPopTable.get_pop_groups()`
        '''

        return [self.__pop_sex, self.__pop_age]

    def set_comp_end(self, comps: List[str]):
        '''
        Specify the component(s) recorded at the end of the period.

        Usage
        -----
        `ProvPopTable.set_comp_end(comps)`

        Arguments
        ---------
        * `comps`: a list of str; name(s) of component(s) that is recorded
            at the end of the period in `self`. This setter raises an error
            if any of the component names in `comps` is not a subset of
            all the negative and positive components.

        Details
        -------
        To calculate the end-of-period population of age a + 1, the process
        requires component values at age a. For some components, however,
        it may require component values at age a + 1. This setter is to
        specify which components are the ones that require the
        end-of-period values. For example, the difference of NPR of age
        a is computed by subtracting the start-of-period NPR of age a
        from the end-of-period NPR of age a + 1.
        '''

        all_comps = self.get_comp_neg()
        all_comps.extend(self.get_comp_pos())
        raise_if_not_subset(comps, all_comps, 'comps', 'all components')
        self.__comp_end = comps

    def get_I(self):
        '''
        Get the vector I := |min(pop_end, 0)|. That is, get the amount of
        which each record requires so that the respective end-of-period
        population becomes nonnegative.

        Usage
        -----
        `ProvPopTable.get_I()`

        Details
        -------
        If a record has -3 as its end-of-period population, then this
        method will return 3; if a record has a nonnegative end-of-period
        population (e.g. 0, 1, or bigger), then the method returns 0.
        '''

        result = self.calculate_pop()
        I = result[self.__pop_end].apply(lambda x: abs(min(x, 0)))
        del result[self.__pop_end]
        result['I'] = I

        return result

    def get_J(self, comp: Optional[str] = None):
        '''
        Return how much modification and counter-adjustments the records of
        `self` can absorb in the `comp` component for the youngest 
        problematic record. In case where `self` doesn't need a correction,
        it throws an IndexError.

        Usage
        -----
        `ProvPopTable.get_J(comp)`

        Details
        -------
        For all the problematic records of `self`, i.e. records having a
        negative end-of-period population, the method searches for the 
        record that has the youngest age among them. For that particular
        problematic record, it computes the maximum counter-adjustments
        applicable to the `comp` component of neighbouring-age records. 
        For example, if there are two records of end-of-period population
        in `self`, one at age 94 and the other at age 97, the method 
        searches for the possible counter-adjustments for the problematic
        record at age 94. After all the modification and counter-
        adjustments are applied to the record of age 94, the process will
        do the same for the problematic record at age 97.

        Arguments
        ---------
        * `comp`: a str; the name of component in `self` that will be
            modified and adjusted. Although it does not have a default
            argument, it must be specified.
        '''

        # Get basic options
        comp_neg = self.get_comp_neg()
        comp_pos = self.get_comp_pos()
        comps = comp_neg + comp_pos
        raise_if_not_subset([comp], comps, 'comp', 'components of self')
        at_least = get_option('pop.at_least')
        pop_groups = self.get_pop_groups()
        cols_required = pop_groups.copy()
        cols_required.append(comp)

        # Get properties of the youngest problematic record
        ## .sort_values() will be deprecated in later versions of pandas
        I = self.get_I()
        I = I.query('I != 0').sort_values(pop_groups)
        problematic = I.iloc[0, :] # choose the youngest
        problematic_sex = problematic[self.__pop_sex]
        problematic_age = problematic[self.__pop_age]
        problematic_val = problematic['I']
        calculated_pop = self.calculate_pop()
        comp_in_neg = comp in comp_neg # comp is in comp_pos otherwise
        comp_in_comp_end = comp in self.__comp_end
        age_is_max = problematic_age.is_max()

        # Get the corresponding age(s) of comp to modify & counter-adjust
        ages = calculate_ages_to_modify_and_counter(
            problematic_age, 
            comp_in_comp_end
        )
        to_modify_age = ages['age.to_modify']
        to_counter_age = ages['age.to_counter']

        # Get the maximum amounts modifiable & counter-adjustable
        correctable_in_pop_end = calculated_pop.copy()\
            .loc[lambda df: df[self.__pop_sex] == problematic_sex]
        correctable_in_comp = self\
            .loc[lambda df: df[self.__pop_sex] == problematic_sex]\
            [cols_required]
        to_modify_records = calculate_modifiable_in_comp(
            df_pop_end = correctable_in_pop_end,
            df_comp = correctable_in_comp,
            pop_age = self.__pop_age,
            pop_end = self.__pop_end,
            comp = comp,
            problematic_age = problematic_age,
            to_modify_age = to_modify_age,
            comp_in_neg = comp_in_neg
        )
        to_counter_records = calculate_counter_adjustable_in_comp(
            df_pop_end = correctable_in_pop_end,
            df_comp = correctable_in_comp,
            pop_age = self.__pop_age,
            pop_end = self.__pop_end,
            comp = comp,
            to_counter_age = to_counter_age,
            comp_in_comp_end = comp_in_comp_end,
            comp_in_neg = comp_in_neg
        )
        result = {
            'records.to_modify': to_modify_records,
            'records.to_counter': to_counter_records
        }

        return result

    def get_K(
        self, 
        comp: Optional[str] = None, 
        method: Optional[str] = None,
        J: Optional[dict] = None
    ):
        '''
        Compute the actual amount of counter-adjustments to be applied to 
        the `comp` of `self` based on different `method`s. Specify `J` for
        a faster computation. Specifying the `method_use.second_pass` 
        option will further determine how the amount of counter-adjustments
        will be distributed when using the one-distribution method.

        Usage
        -----
        `ProvPopTable.get_K(comp, method, J)`

        Arguments
        ---------
        * `comp`: a str; the same argument as `self.get_J(comp)`.
        * `method`: a str; either '1dist', 'filler', or 'prop'. If `None`, 
            then the global option value `estime2.options.method` is used. 
            See Details below.
        * `J`: a dict of "str: pd.DataFrame"; a return value of 
            `self.get_J(comp)`. If `None`, then `self.get_J(comp)` is
            evaluated.

        Details
        -------
        Based on the results of `self.get_J(comp)`, this method computes
        the actual amount to be either added or subtracted to the `comp`
        values of `self`. Depending on the `method` argument, the way in
        which those corrections are calculated gets different.

        Suppose that neighbouring ages are from 56 to 95 and the total 
        value to be modified is 4. Suppose also that, from the result of 
        `self.get_J(comp)`, the maximum counter-adjustable value for ages 
        91, 92, 93, 94, and 95 are computed as 1, 1, 2, 1, and 0 
        respectively.

        1. If `method = '1dist'`, then `self.get_K()` distributes 1 to the
            counter-adjustable component values starting from the maximum
            counter-adjustable age so that the modifiable component value 
            is balanced out. For the above scenario, '1dist' starts to put 
            1 to the `comp` of age 94 since the `comp` at age 95 is not 
            correctable, 1 to age 93, 1 to age 92, and finally 1 to age 91.
        2. If `method = 'filler'`, then `self.get_K()` distributes the 
            maximum correctable amount starting from the maximum 
            counter-adjustable age so that the modifiable component value 
            is balanced out. For the above scenario, it puts 1 to the age 
            94, 2 to the age 93 since that is the maximum correctable 
            amount, and finally 1 to the age 92.
        3. If `method = 'prop'`, then `self.get_K()` computes the 
            proportions of end-of-period populations in a given period,
            usually in a length of 5 years (which can be changed via 
            `estime2.options.age.prop_size`), compare them with the maximum
            correctable values at each record's component, and take the
            minimum of the two. In each counter-adjustment, this method
            checks whether the entire value of modification is distributed
            within the component of 5-year period. If yes, terminate the
            process; otherwise, the remaining modification value is
            distributed to the record of the highest proportions as much as
            possible. In case of tie proportions, take the oldest
            neighbouring-age record within the period. The process 
            continues until all the modification value is distributed.

        This method tries to balance out the modification value in the 
        problematic component as much as possible. In case where it is too 
        big to be completely balanced out within the component, the method 
        either: 
        
        a. stops the iteration (and move on to the next problematic
            component to fix the remaining negative value), or;
        b. runs the correction method once again in the same component

        If the `method` argument/option is 'filler', 'prop', or '1dist'
        with the `method_use.second_pass` (global) option being `False`, 
        then the choice is always "a". If `method` is '1dist' and
        `method_use.second_pass` is `True`, then the one-distribution is 
        applied once again in the same problematic component.
        '''

        method = return_goption_if_None('method', method)
        prev_method = get_option('method')
        set_option('method', method)
        set_option('method', prev_method)
        
        comp_in_comp_end = comp in self.__comp_end
        pop_groups = [self.__pop_sex, self.__pop_age]
        comp_J = "{0}_J".format(comp)
        dfs_comp = None
        if J is None:
            dfs_comp = self.get_J(comp) # sanity check of comp done here
        else:
            dfs_comp = J # assuming sanity check is already done for comp
        df_comp_modifiable = dfs_comp['records.to_modify']
        df_comp_counter_adjust = dfs_comp['records.to_counter']
        df_comp_counter_adjust_reversed = df_comp_counter_adjust\
            .sort_values(pop_groups, ascending = [True, False])
        to_modify_val_total = df_comp_modifiable[comp_J].sum()

        comp_K = "{0}_K".format(comp)
        result = []
        max_correctables =\
            df_comp_counter_adjust_reversed.iloc[:, -1].values.copy()

        if method == '1dist':
            for index, row in df_comp_counter_adjust_reversed.iterrows():
                if row[comp_J] > 0 and to_modify_val_total != 0:
                    result.append(1)
                    to_modify_val_total -= 1
                else:
                    result.append(0)
            use_2nd_pass = get_option('method_use.second_pass')
            if to_modify_val_total != 0 and use_2nd_pass:
                # The first pass wasn't enough so that to_modify_val_total
                # didn't come down to 0.
                # Apply the second pass only if the option says so.
                max_correctables -= np.array(result)
                for i, item in enumerate(max_correctables):
                    if item > 0 and to_modify_val_total != 0:
                        result[i] += 1
                        to_modify_val_total -= 1
        elif method == 'filler':
            for index, row in df_comp_counter_adjust_reversed.iterrows():
                if row[comp_J] > 0 and to_modify_val_total != 0:
                    min_comp_J_val = min(row[comp_J], to_modify_val_total)
                    result.append(min_comp_J_val)
                    to_modify_val_total -= min_comp_J_val
                else:
                    result.append(0)
        elif method == 'prop':
            problematic_sex = df_comp_modifiable[self.__pop_sex].values[0]
            prop_max_age = df_comp_counter_adjust_reversed\
                .iloc[0, :]\
                [self.__pop_age]
            prop_min_age = df_comp_counter_adjust_reversed\
                .iloc[-1, :]\
                [self.__pop_age]
            if not comp_in_comp_end:
                prop_max_age += 1
                prop_min_age += 1
            calculated_pop = self.calculate_pop()
            pop_end_to_compare_reversed = calculated_pop.copy()\
                .loc[lambda df: df[self.__pop_sex] == problematic_sex]\
                .loc[lambda df: df[self.__pop_age] <= prop_max_age]\
                .loc[lambda df: df[self.__pop_age] >= prop_min_age]\
                .sort_values(pop_groups, ascending = [True, False])
            
            prop_size = get_option('age.prop_size')
            pop_end_for_prop =\
                pop_end_to_compare_reversed.iloc[:, -1].values
            pop_end_len = len(pop_end_for_prop)
            # Note: len(pop_end_for_prop) == len(max_correctables)
            for i in np.arange(pop_end_len, step = prop_size):
                # min(...) is required to define `period` in case where 
                # pop_end_len is not a multiple of prop_size
                period = [i, min(i + prop_size, pop_end_len)]
                props_numer = pop_end_for_prop[period[0]:period[1]]
                props_denom = sum(props_numer)
                props = props_numer / props_denom
                props_x_m = np.array(
                    list(map(int, np.round(to_modify_val_total * props)))
                )
                max_correct_for_each =\
                    max_correctables[period[0]:period[1]]
                min_from_each = np.minimum(props_x_m, max_correct_for_each)
                # The last `[0]` in `loc_max_prop` is an application of
                # the principle to take the oldest neighbouring-age record 
                # within the period in case where the record of highest 
                # proportion is not unique.
                loc_max_prop = np.where(props == max(props))[0][0]
                sum_min_from_each = sum(min_from_each)
                to_modify_val_total -= sum_min_from_each
                plmp = props_x_m[loc_max_prop]
                mclmp = max_correct_for_each[loc_max_prop]
                if plmp <= mclmp:
                    more_possible_correction = mclmp - plmp
                    min_mod_cor = min(
                        to_modify_val_total,
                        more_possible_correction
                    )
                    min_from_each[loc_max_prop] += min_mod_cor
                    to_modify_val_total -= min_mod_cor
                    result.extend(min_from_each)
                else:
                    result.extend(min_from_each)
        else:
            raise NotImplementedError

        df_comp_counter_adjust_reversed[comp_K] = result
        del df_comp_counter_adjust_reversed[comp_J]
        df_comp_counter_adjust_reversed\
            .sort_values(
                pop_groups, 
                ascending = [True, True], 
                inplace = True
            )

        return df_comp_counter_adjust_reversed

    def get_L(
        self,
        comp: Optional[str] = None,
        method: Optional[str] = None
    ):
        '''
        Bind rows of `self.get_J(comp)['records.to_modify']` and 
        `self.get_K(comp, method)`.
        
        Details
        -------
        This method binds two `pandas.DataFrame`s by row, where the top
        is the records of neighbouring ages and correction figures computed
        from `self.get_K(comp, method)`, and the bottom is the record(s) of
        modification to be made to `comp`, which is coming from 
        `self.get_J(comp)['records.to_modify']`.
        If the `comp` is a negative component, put the minus sign in front 
        of `self.get_J(comp)['records.to_modify']` and the plus sign in 
        front of `self.get_K(comp, method)`.
        If the `comp` is a positive component, put the plus sign in front
        of `self.get_J(comp)['records.to_modify']` and the minus sign in
        front of `self.get_K(comp, method)`.

        Usage
        -----
        `ProvPopTable.get_L(comp, method)`
        '''

        comp_neg = self.get_comp_neg()
        comp_in_neg = comp in comp_neg
        comp_J = f'{comp}_J'
        comp_K = f'{comp}_K'
        comp_L = f'{comp}_L'
        
        J_all = self.get_J(comp)
        K = self.get_K(comp, method, J_all)
        J = J_all['records.to_modify']

        sum_mod_val = J[comp_J].sum()
        p_sex = J[self.__pop_sex].values[0]
        p_age = J[self.__pop_age].values
        sum_counter_adjust = K[comp_K].sum()
        assert sum_mod_val == sum_counter_adjust, \
            f"The total modification value, {sum_mod_val}, " +\
            f"at sex {p_sex} age(s) {p_age} and " +\
            f"component {comp} is not equal to the sum of " +\
            f"counter-adjustments, {sum_counter_adjust}."

        if comp_in_neg:
            J[comp_L] = -J[comp_J]
            del J[comp_J]
            K[comp_L] = K[comp_K]
            del K[comp_K]
        else: # i.e. comp is positive
            J[comp_L] = J[comp_J]
            del J[comp_J]
            K[comp_L] = -K[comp_K]
            del K[comp_K]

        L = K.append(J, ignore_index = True)

        return L

def calculate_ages_to_modify_and_counter(
    problematic_age: Age,
    comp_in_comp_end: bool
):
    '''
    Return the age(s) of components to modify, as well as ages to make 
    counter-adjustments.

    Details
    -------
    This is a function to be used within the `ProvPopTable.get_J(comp)`
    method. It computes the age(s) of records to be modified. For example,
    if the negative end-of-period population is detected at age 97, and
    the component is NOT one of the end-of-period components, then the 
    method will select the age 96 

    Arguments
    ---------
    * `problematic_age`: an Age whose end-of-period population is negative.
    * `comp_in_comp_end`: a bool; is the `comp` in `self.get_J(comp)` the
        end-of-period component, i.e. `comp in self.__comp_end`?

    Examples
    --------
    >>> # age.down_to == 40
    >>> # age.max == 99
    >>> age1 = Age(97)
    >>> age2 = Age('100+') # maximum age
    >>> set_option('age.floor', 65)
    >>> result1 = calculate_ages_to_modify_and_counter(
    ...     age1, 
    ...     comp_in_comp_end = False
    ... )
    >>> result1 == {
    ...     'age.to_modify': 96, 
    ...     'age.to_counter': [56, 95]
    ... }
    True
    >>> result2 = calculate_ages_to_modify_and_counter(
    ...     age1, 
    ...     comp_in_comp_end = True
    ... )
    >>> result2 == {
    ...     'age.to_modify': 97, 
    ...     'age.to_counter': [57, 96]
    ... }
    True
    >>> result3 = calculate_ages_to_modify_and_counter(
    ...     age2, 
    ...     comp_in_comp_end = False
    ... )
    >>> result3 == {
    ...     'age.to_modify': [99, 100], 
    ...     'age.to_counter': [59, 98]
    ... }
    True
    >>> result4 = calculate_ages_to_modify_and_counter(
    ...     age2, 
    ...     comp_in_comp_end = True
    ... )
    >>> result4 == {
    ...     'age.to_modify': 100, 
    ...     'age.to_counter': [60, 99]
    ... }
    True
    >>> set_option('age.floor', 50)
    >>> result5 = calculate_ages_to_modify_and_counter(
    ...     age1, 
    ...     comp_in_comp_end = False
    ... )
    >>> result5 == {
    ...     'age.to_modify': 96, 
    ...     'age.to_counter': [50, 95]
    ... }
    True
    >>> result6 = calculate_ages_to_modify_and_counter(
    ...     age1, 
    ...     comp_in_comp_end = True
    ... )
    >>> result6 == {
    ...     'age.to_modify': 97, 
    ...     'age.to_counter': [50, 96]
    ... }
    True
    '''

    age_down_to = get_option('age.down_to')
    age_floor = get_option('age.floor')
    age_is_max = problematic_age.is_max()
    to_modify_age_str = str(problematic_age.get_showing_age())
    to_modify_age_int = int(to_modify_age_str) - 1
    if comp_in_comp_end:
        to_modify_age_int += 1
    to_counter_age_max = to_modify_age_int - 1
    to_counter_age_min = min(
        age_floor, 
        max(-1, to_modify_age_int - age_down_to)
    )
    to_modify_age_int_lst = None
    result = {}
    if age_is_max and not comp_in_comp_end:
        to_modify_age_int_lst = [to_modify_age_int, to_modify_age_int + 1]
        result['age.to_modify'] = to_modify_age_int_lst
        result['age.to_counter'] = [to_counter_age_min, to_counter_age_max]
    else:
        result['age.to_modify'] = to_modify_age_int
        result['age.to_counter'] = [to_counter_age_min, to_counter_age_max]

    return result

def calculate_counter_adjustable_in_comp(
    df_pop_end: pd.DataFrame,
    df_comp: pd.DataFrame,
    pop_age: str,
    pop_end: str,
    comp: str,
    to_counter_age: List[int],
    comp_in_comp_end: bool,
    comp_in_neg: bool
):
    '''
    Compute the maximum amount that is counter-adjustable in `comp` of
    `df_comp` based on `pop_end` in `df_pop_end`, the information regarding
    the `to_counter_age`, `comp_in_comp_end`, and `comp_in_neg`. `pop_age`
    is the name of the age column for both `df_pop_end` and `df_comp`.
    '''

    at_least = get_option('pop.at_least')
    to_counter_age_min = to_counter_age[0]
    to_counter_age_max = to_counter_age[1]
    df_pop_end_compare = None
    if comp_in_comp_end:
        df_pop_end_compare = df_pop_end\
            .loc[lambda df: df[pop_age] >= to_counter_age_min]\
            .loc[lambda df: df[pop_age] <= to_counter_age_max]
    else:
        df_pop_end_compare = df_pop_end\
            .loc[lambda df: df[pop_age] >= to_counter_age_min + 1]\
            .loc[lambda df: df[pop_age] <= to_counter_age_max + 1]
    df_pop_end_compare[pop_end] -= at_least
    df_comp_counter_adjust = df_comp\
        .loc[lambda df: df[pop_age] >= to_counter_age_min]\
        .loc[lambda df: df[pop_age] <= to_counter_age_max]

    pop_end_values = df_pop_end_compare[pop_end].values
    comp_values = df_comp_counter_adjust[comp].values
    counter_adjustable = []
    to_append = None
    if len(comp_values) != len(pop_end_values):
        # This will never happen since to_counter_age_min is always 
        # at least -1.
        raise NotImplementedError
    for pop_end_val, comp_val in zip(pop_end_values, comp_values):
        if pop_end_val <= 0:
            # If "end-of-period pop - 1" <= 0 (where 1 == pop.at_least),
            # then that neighbouring age record can't absorb any correction
            to_append = 0
        elif comp_in_neg:
            # If "end-of-period pop - 1" > 0, i.e. it is correctable,
            # then see if the component is negative.
            # If it is, then the maximum correction (i.e. increase in the
            # component value of the record, like increasing the death from
            # 2 to 3) of this record must be the "end-of-period pop of that 
            # record - 1" because if the negative component increases more
            # than that, then the "end-of-period population - 1" of the 
            # neighbouring age record will go below 1.
            to_append = pop_end_val
        else:
            # If "end-of-period pop - 1" > 0, i.e. it is correctable,
            # and the component is positive, then the maximum correction 
            # (i.e. "decrease" in the component value of the record, like
            # decreasing the immigration from 5 to 4) of this record must
            # be the minimum of "end-of-period pop - 1" and the component 
            # value. This is because, in the positive component, the 
            # component value has to decrease (not increase) in 
            # neighbouring ages in order to balance out the
            # modification at the problematic record. If the 
            # counter-adjustment goes below this minimum value, then either
            # the end-of-period population or the component value will 
            # become negative.
            to_append = min(pop_end_val, comp_values)
        counter_adjustable.append(to_append)

    df_comp_counter_adjust[f"{comp}_J"] = counter_adjustable
    del df_comp_counter_adjust[comp]

    return df_comp_counter_adjust

def calculate_modifiable_in_comp(
    df_pop_end: pd.DataFrame,
    df_comp: pd.DataFrame,
    pop_age: str,
    pop_end: str,
    comp: str,
    problematic_age: Age,
    to_modify_age: Union[int, List[int]],
    comp_in_neg: bool
):
    '''
    Compute the maximum modifiable value of `comp` in `df_comp` based on 
    `pop_end` in `df_pop_end`, the information regarding the 
    `problematic_age`, `to_modify_age`, and `comp_in_neg`. `pop_age` is the
    name of the age column for both `df_pop_end` and `df_comp`.
    '''

    at_least = get_option('pop.at_least')
    age_is_max = problematic_age.is_max()
    pop_end_query = None
    if age_is_max:
        pop_end_query = f"{pop_age} > {get_option('age.max')}"
    else:
        pop_end_query = f"{pop_age} == {problematic_age}"
    df_pop_end_problematic = df_pop_end.query(pop_end_query)
    df_comp_modifiable = None
    if isinstance(to_modify_age, int):
        df_comp_modifiable = df_comp\
            .loc[lambda df: df[pop_age] == to_modify_age]
    elif isinstance(to_modify_age, list):
        df_comp_modifiable = df_comp\
            .loc[lambda df: df[pop_age] <= to_modify_age[1]]\
            .loc[lambda df: df[pop_age] >= to_modify_age[0]]
    else:
        raise NotImplementedError

    modifiable_val_in_pop_end = df_pop_end_problematic[pop_end].values[0]
    abs_modifiable_val_in_pop_end = abs(modifiable_val_in_pop_end)
    modifiable = None
    if isinstance(to_modify_age, int):
        modifiable_val_in_comp = df_comp_modifiable[comp].values[0]
        if comp_in_neg:
            # `modifiable` also has to consider the sum of the
            # counter-adjustable values in `min`, but it is not done here
            # since it is deemed to be always greater than these two 
            # numbers in the following min function.
            modifiable = min(
                abs_modifiable_val_in_pop_end,
                modifiable_val_in_comp
            )
        else:
            modifiable = abs_modifiable_val_in_pop_end
    elif isinstance(to_modify_age, list):
        modifiable_val_in_comp = df_comp_modifiable[comp]
        modifiable_val_in_comp_0 = modifiable_val_in_comp.values[0]
        modifiable_val_in_comp_1 = modifiable_val_in_comp.values[1]
        modifiable_0 = None
        modifiable_1 = None
        if comp_in_neg:
            modifiable_1 = min(
                abs_modifiable_val_in_pop_end, 
                modifiable_val_in_comp_1
            )
            modifiable_0 = None
            leftover = None
            if modifiable_1 == abs_modifiable_val_in_pop_end:
                modifiable_0 = 0
            else:
                leftover = abs_modifiable_val_in_pop_end -\
                    modifiable_val_in_comp_1
                modifiable_0 = min(leftover, modifiable_val_in_comp_0)
        else:
            modifiable_0 =\
                (abs_modifiable_val_in_pop_end // 2)
            modifiable_1 =\
                abs_modifiable_val_in_pop_end - modifiable_0
        modifiable = [modifiable_0, modifiable_1]
    else:
        raise NotImplementedError

    df_comp_modifiable[f"{comp}_J"] = modifiable
    del df_comp_modifiable[comp]

    return df_comp_modifiable

def return_goption_if_None(opname: str, argument):
    '''
    Return the global option value of `opname` if `argument` is None,
    and return `argument` if it is not None.

    Usage
    -----
    `return_goption_if_None(opname, argument)`
    '''

    return return_op_if_None(get_option(opname), argument)



if __name__ == '__main__':
    import doctest
    doctest.testmod()