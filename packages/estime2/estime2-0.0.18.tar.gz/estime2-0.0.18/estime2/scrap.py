
# from age import Age
# from config import (
#     get_option
# )
# from provpoptable import (
#     ProvPopTable,
#     calculate_ages_to_modify_and_counter
# )
from estime2 import (
    Age,
    get_option,
    options,
    set_option,
    ProvPopTable
)
from estime2.provpoptable import calculate_ages_to_modify_and_counter
from pprint import pprint
import estime2
import numpy as np
import os
import pandas as pd
pd.options.display.min_rows = 15

RegionSAD = ['RegionCode', 'Sex', 'Age', 'RefDate']
RegionSA = RegionSAD[0:3]
RegionSD = list(np.array(RegionSAD)[[0,1,3]])
RegionS = RegionSA[0:2]
    
def arrange_by_lvl(df, levels, value_name):
    age_cols = [col for col in df if col.startswith('A_')]
    result =\
        pd.melt(
            df[levels + age_cols],
            id_vars = levels,
            value_vars = age_cols,
            var_name = 'Age',
            value_name = value_name
        )\
        .assign(
            Age = lambda df: \
                df.Age.apply(lambda x: int(x[(x.index('A_') + 2):]))
        )
    return result

def call_tbl():
    tbl_name = [x for x in os.listdir('..') if x[0] == 'G'][0]
    tbl = pd.read_excel('../' + tbl_name, sheet_name = 1)
    poptbl = ProvPopTable(tbl)
    return poptbl

def call_tbl2():
    files_above = os.listdir('..')
    starts_with_10 = list(map(lambda x: x[0:2] == '10', files_above))
    tbl_name = np.array(files_above)[starts_with_10][0]

    with pd.ExcelFile('../' + tbl_name) as tbl:
        pop_2001 = pd.read_excel(tbl, sheet_name = 0)
        bth = pd.read_excel(tbl, sheet_name = 1)
        dth_d01 = pd.read_excel(tbl, sheet_name = 2)
        dth_d02 = pd.read_excel(tbl, sheet_name = 3)
        imm = pd.read_excel(tbl, sheet_name = 4)
        emi = pd.read_excel(tbl, sheet_name = 5)
        rem = pd.read_excel(tbl, sheet_name = 6)
        nte = pd.read_excel(tbl, sheet_name = 7)
        mip = pd.read_excel(tbl, sheet_name = 8)
        mit = pd.read_excel(tbl, sheet_name = 9)
        npr = pd.read_excel(tbl, sheet_name = 10)
        pop_2002_orig = pd.read_excel(tbl, sheet_name = 11, skiprows = 2)
        pop_2002_corrected = pd.read_excel(tbl, sheet_name = 12)

    return {
        'pop_2001': pop_2001, 
        'bth': bth,
        'dth_d01': dth_d01,
        'dth_d02': dth_d02,
        'imm': imm,
        'emi': emi,
        'rem': rem,
        'nte': nte,
        'mip': mip,
        'mit': mit,
        'npr': npr,
        'pop_2002_orig': pop_2002_orig,
        'pop_2002_corrected': pop_2002_corrected
    }

def run():
    poptbl = call_tbl()

    pop_age = 'Age'
    pop_end = 'Postcensal Population'
    comp = 'DTH'

    # Get basic options
    comp_neg = poptbl.get_comp_neg()
    comp_pos = poptbl.get_comp_pos()
    comps = comp_neg + comp_pos
    at_least = get_option('pop.at_least')
    pop_groups = ['Sex', 'Age']
    cols_required = pop_groups.copy()
    cols_required.append(comp)

    # Get properties of the youngest problematic record
    I = poptbl.get_I()
    I = I.query('I != 0').sort_values(pop_groups)
    problematic = I.iloc[0, :]
    problematic_sex = problematic['Sex']
    problematic_age = problematic['Age']
    problematic_val = problematic['I']
    calculated_pop = poptbl.calculate_pop()
    comp_in_neg = comp in comp_neg
    comp_in_comp_end = False
    age_is_max = problematic_age.is_max()
    
    # Get the corresponding age(s) of comp to modify & counter-adjust
    ages = calculate_ages_to_modify_and_counter(
        problematic_age,
        comp_in_comp_end
    )    
    to_modify_age = ages['age.to_modify']
    to_counter_age = ages['age.to_counter']

    # Get the maximum amounts modifiable & counter-adjustable
    correctable_in_comp = poptbl\
        .loc[lambda df: df['Sex'] == problematic_sex]\
        [cols_required]
    correctable_in_pop_end = calculated_pop.copy()\
        .loc[lambda df: df['Sex'] == problematic_sex]

    df_comp = correctable_in_comp.copy()
    df_pop_end = correctable_in_pop_end.copy()

    # calculate_modifiable_in_comp
    pop_end_query = None
    if age_is_max:
        pop_end_query = "{0} > {1}".format(pop_age, get_option('age.max'))
    else:
        pop_end_query = "{0} == {1}".format(pop_age, problematic_age)
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

    # print('Problematic record:')
    # print(df_pop_end_problematic)
    # print('')
    # print('Component value to modify:')
    # print(df_comp_modifiable)

    modifiable_val_in_pop_end = df_pop_end_problematic[pop_end].values[0]
    abs_modifiable_val_in_pop_end = abs(modifiable_val_in_pop_end)
    modifiable = None
    if isinstance(to_modify_age, int):
        modifiable_val_in_comp = df_comp_modifiable[comp].values[0]
        if comp_in_neg:
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
            modifiable_0 = abs_modifiable_val_in_pop_end // 2
            modifiable_1 = abs_modifiable_val_in_pop_end - modifiable_0
        modifiable = [modifiable_0, modifiable_1]
    else:
        raise NotImplementedError
    
    df_comp_modifiable["{0}_J".format(comp)] = modifiable
    del df_comp_modifiable[comp]

    # print('Component value modifiable:')
    # print(df_comp_modifiable)

    # calculate_counter_adjustable_in_comp
    modifiable_in_comp = df_comp_modifiable.copy()
    to_counter_age_min = to_counter_age[0]
    to_counter_age_max = to_counter_age[1]

    df_comp_counter_adjust = df_comp\
        .loc[lambda df: df[pop_age] >= to_counter_age_min]\
        .loc[lambda df: df[pop_age] <= to_counter_age_max]
    if comp_in_comp_end:
        df_pop_end_compare = df_pop_end\
            .loc[lambda df: df[pop_age] >= to_counter_age_min]\
            .loc[lambda df: df[pop_age] <= to_counter_age_max]
    else:
        df_pop_end_compare = df_pop_end\
            .loc[lambda df: df[pop_age] >= to_counter_age_min + 1]\
            .loc[lambda df: df[pop_age] <= to_counter_age_max + 1]
    df_pop_end_compare[pop_end] -= at_least

    pop_end_values = df_pop_end_compare[pop_end].values
    comp_values = df_comp_counter_adjust[comp].values
    counter_adjustable = []
    to_append = None

    for val in zip(pop_end_values, comp_values):
        if val[0] <= 0:
            to_append = 0
        elif comp_in_neg:
            to_append = val[0]
        else:
            to_append = val[1]
        counter_adjustable.append(to_append)

    df_comp_counter_adjust["{0}_J".format(comp)] = counter_adjustable
    del df_comp_counter_adjust[comp]

    # print("Component values counter-adjustable:")
    # print(df_comp_counter_adjust)
    df_comp_counter_adjust_reversed = df_comp_counter_adjust\
        .sort_values(pop_groups, ascending = [True, False])

    comp_J = "{0}_J".format(comp)
    comp_K = "{0}_K".format(comp)
    to_modify_val_total = df_comp_modifiable[comp_J].sum()
    # print('Total value to be modified:')
    # print(to_modify_val_total)

    result = []
    method = get_option('method')
    # print('Counter-adjustable records:')
    if method == '1dist':
        for index, row in df_comp_counter_adjust_reversed.iterrows():
            if row[comp_J] > 0 and to_modify_val_total != 0:
                result.append(1)
                to_modify_val_total -= 1
            else:
                result.append(0)
    else: # i.e. prop
        for index, row in df_comp_counter_adjust_reversed.iterrows():
            if row[comp_J] > 0 and to_modify_val_total != 0:
                min_comp_J_val = min(row[comp_J], to_modify_val_total)
                result.append(min_comp_J_val)
                to_modify_val_total -= min_comp_J_val
            else:
                result.append(0)

    df_comp_counter_adjust_reversed[comp_K] = result
    del df_comp_counter_adjust_reversed[comp_J]
    df_comp_counter_adjust_reversed\
        .sort_values(
            pop_groups, 
            ascending = [True, True], 
            inplace = True
        )

    comp_L = '{0}_L'.format(comp)
    J = df_comp_modifiable
    K = df_comp_counter_adjust_reversed

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

    self_copy = poptbl.copy()
    self_copy = self_copy.merge(L, on = pop_groups, how = 'left')
    self_copy.fillna(0, inplace = True)
    self_copy[comp_L] = self_copy[comp_L].apply(int)
    self_copy[comp] += self_copy[comp_L]
    del self_copy[comp_L]

    self_copy = ProvPopTable(
        self_copy,
        pop_sex = 'Sex', # self.__pop_sex,
        pop_age = 'Age', # self.__pop_age,
        pop_end = 'Postcensal Population', # self.__pop_end,
        pop_start = 'Initial Population', # self.__pop_start,
        pop_birth = 'BTH', # self.__pop_birth,
        comp_neg_temp_out = get_option('comp_neg.temp_out'), # self.__comp_neg_temp_out,
        comp_neg_emi = get_option('comp_neg.emi'),
        comp_neg_npr_out = get_option('comp_neg.npr_out'),
        comp_neg_death = get_option('comp_neg.death'),
        comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
        comp_pos_temp_in = get_option('comp_pos.temp_in'),
        comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
        comp_pos_npr_in = get_option('comp_pos.npr_in'),
        comp_pos_immi = get_option('comp_pos.immi'),
        comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
        comp_end = get_option('comp.end'),
        reorder_cols = False,
        show_pop_end = pop_end in poptbl.columns.tolist(), # self.columns.tolist(),
        flag = False        
    )

    print("self:")
    print(poptbl)
    print("self.calculate_pop():")
    self_calculate_pop = poptbl.calculate_pop()
    print(self_calculate_pop)
    print("Total end-of-period pop of self:")
    print(self_calculate_pop[pop_end].sum())
    print("self_copy after applying comp_L:")
    print(self_copy)
    print("self_copy.calculate_pop():")
    self_copy_calculate_pop = self_copy.calculate_pop()
    print(self_copy_calculate_pop)
    print("self_copy.get_I():")
    print(all(self_copy.get_I()['I'].values == 0))
    print("Total end-of-period pop of self_copy:")
    print(self_copy_calculate_pop[pop_end].sum())

    print('poptbl.fix_issues():')
    result = poptbl.fix_issues()
    print(result.calculate_pop())

    # test = Age('99+')
    # print(str(test)[-1] == '+')
    # print(Age(102).get_showing_age())

    # pop_groups = ['Sex', 'Age']
    # pop_end = 'Postcensal Population'
    # pop_start = 'Initial Population'
    # pop_birth = 'BTH'
    # comp_neg = ['TEM', 'EMI', 'NPR, 2018-07-01', 'DTH', 'IOM']
    # comp_pos = ['RE', 'NPR, 2019-07-01' ,'IMM', 'IIM']
    # comps = comp_neg + comp_pos
    # comp_end = ['NPR, 2019-07-01']
    # comp_not_end = []
    # for comp in comps:
    #     if comp not in comp_end:
    #         comp_not_end.append(comp)
    # comp_aggs = {}
    # comp_aggs[pop_start] = 'sum'
    # comp_aggs[pop_birth] = 'sum'
    # for comp2 in comp_not_end:
    #     comp_aggs[comp2] = 'sum'

    # result1 = poptbl.loc[
    #     :, 
    #     pop_groups + [pop_start, pop_birth] + comp_not_end
    # ]
    # result1['Age'] += 1
    # result1 = result1\
    #     .groupby(pop_groups)\
    #     .agg(comp_aggs)\
    #     .reset_index()

    # result2 = poptbl.loc[:, pop_groups + comp_end]
    # result2 = result2.loc[lambda df: df['Age'] != -1]

    # result3 = result1\
    #     .merge(
    #         result2, 
    #         how = 'left', 
    #         on = ['Sex', 'Age']
    #     )
    
    # result3[pop_end] = result3[pop_start] + result3[pop_birth]
    # if comp_neg != []:
    #     for col_neg in comp_neg:
    #         result3[pop_end] -= result3[col_neg]
    # if comp_pos != []:
    #     for col_pos in comp_pos:
    #         result3[pop_end] += result3[col_pos]

    # result = result3.loc[:, pop_groups + [pop_end]]

    # pop_end =\
    #     poptbl['Initial Population'] + poptbl['BTH']\
    #         - poptbl['TEM'] - poptbl['EMI'] - poptbl['NPR, 2018-07-01']\
    #         - poptbl['DTH'] - poptbl['IOM'] - poptbl['RAO']\
    #         + poptbl['RE'] + poptbl['NPR, 2019-07-01'] + poptbl['IMM']\
    #         + poptbl['IIM'] + poptbl['RAI']
    # pop_grp = poptbl.loc[:, ['Sex', 'Age']]
    # pop_grp['Age'] += 1
    # pop_grp['End-of-period population'] = pop_end
    # result = poptbl\
    #     .groupby(['Sex', 'Age'])\
    #     .agg({
    #         'Initial Population': 'sum',
    #         'BTH': 'sum',
    #         'TEM': 'sum',
    #         'EMI': 'sum',
    #         'NPR, 2018-07-01': 'sum',
    #         'DTH': 'sum',
    #         'IOM': 'sum',
    #         'RAO': 'sum',
    #         'RE': 'sum',
    #         'NPR, 2019-07-01': 'sum',
    #         'IMM': 'sum',
    #         'IIM': 'sum',
    #         'RAI': 'sum'
    #     })\
    #     .reset_index()
    # print(pop_grp)
    # print(result)
    # print(poptbl.calculate_pop())
    # print(poptbl.loc[lambda df: df['Age'] >= '99+'])
    # template =\
    #     '* `{arg_name}`: (`None` by default) a str; the name of ' +\
    #     'the column corresponding to "{real_name}" in the ' +\
    #     'population table. If `None`, it first checks whether the ' +\
    #     'global option value `{glob_name}` is also `None`. If it ' +\
    #     'is also `None`, the "{real_name}" component is ' +\
    #     'discarded from the population table (i.e. not shown and not ' +\
    #     'used). If it is not `None`, the method then checks whether the ' +\
    #     'value `{glob_name}` is one of the column names in the ' +\
    #     'population table. If it is, the column having the same name as ' +\
    #     '`{glob_name}` is selected as the ' +\
    #     '"{real_name}" column. If not, the method raises ' +\
    #     '`AssertionError`.'
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_npr_in',
    #         real_name = 'Non-permanent residents IN',
    #         glob_name = 'comp_pos.npr_in'
    #     )
    # )
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_immi',
    #         real_name = 'Immigrants',
    #         glob_name = 'comp_pos.immi'
    #     )
    # )
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_interprov_in',
    #         real_name = 'Interprovincial migrant IN',
    #         glob_name = 'comp_pos.interprov_in'
    #     )
    # )

def run2():

    method = get_option('method')

    self = call_tbl()

    comp_neg_to_use = self.get_comp_neg()
    comp_pos_to_use = self.get_comp_pos()
    comp_neg_to_use.remove(get_option('comp_neg.interprov_out'))
    comp_pos_to_use.remove(get_option('comp_pos.interprov_in'))
    comps = comp_neg_to_use + comp_pos_to_use

    pop_groups = [get_option('pop.sex'), get_option('pop.age')]
    all_cols = self.columns.tolist()
    show_pop_end = get_option('pop.end') in all_cols
    self_copy = self.copy()

    not_fixed = True
    i = 0
    while not_fixed:
        comp = comps[i]; print(comp)
        i += 1

        comp_L = '{0}_L'.format(comp)
        if i == 1:
            self_copy = ProvPopTable(
                self_copy,
                pop_sex = 'Sex', 
                pop_age = 'Age',
                pop_end = 'Postcensal Population',
                pop_start = 'Initial Population',
                pop_birth = 'BTH',
                comp_neg_temp_out = get_option('comp_neg.temp_out'),
                comp_neg_emi = get_option('comp_neg.emi'),
                comp_neg_npr_out = get_option('comp_neg.npr_out'),
                comp_neg_death = get_option('comp_neg.death'),
                comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
                comp_pos_temp_in = get_option('comp_pos.temp_in'),
                comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
                comp_pos_npr_in = get_option('comp_pos.npr_in'),
                comp_pos_immi = get_option('comp_pos.immi'),
                comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
                comp_end = get_option('comp.end'),
                reorder_cols = False,
                show_pop_end = show_pop_end,
                flag = False  
            )
        L = self_copy.get_L(comp, method); 
        L['Age'] = L['Age'].apply(str); print(L)
        self_copy['Age'] = self_copy['Age'].apply(str)
        self_copy = self_copy.merge(L, on = pop_groups, how = 'left')
        self_copy.fillna(0, inplace = True)
        self_copy[comp_L] = self_copy[comp_L].apply(int)

        print('Before adding:')
        print(self_copy)
        
        self_copy[comp] += self_copy[comp_L]

        print('After adding, before deleting comp_L:')
        print(self_copy)
        
        del self_copy[comp_L]

        print('After adding, after deleting comp_L:')
        print(self_copy)

        self_copy = ProvPopTable(
            self_copy,
            pop_sex = 'Sex', 
            pop_age = 'Age',
            pop_end = 'Postcensal Population',
            pop_start = 'Initial Population',
            pop_birth = 'BTH',
            comp_neg_temp_out = get_option('comp_neg.temp_out'),
            comp_neg_emi = get_option('comp_neg.emi'),
            comp_neg_npr_out = get_option('comp_neg.npr_out'),
            comp_neg_death = get_option('comp_neg.death'),
            comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
            comp_pos_temp_in = get_option('comp_pos.temp_in'),
            comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
            comp_pos_npr_in = get_option('comp_pos.npr_in'),
            comp_pos_immi = get_option('comp_pos.immi'),
            comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
            comp_end = get_option('comp.end'),
            reorder_cols = False,
            show_pop_end = show_pop_end,
            flag = False  
        )

        not_fixed = not (all(self_copy.get_I()['I'].values == 0) or i == len(comps))


    print(self_copy)

def run3():
    poptbl = call_tbl()
    print(poptbl)
    print(poptbl.calculate_pop())

    result = poptbl.fix_issues(return_all_mods = True)

    pprint(result)
    try:
        print(result.calculate_pop())
    except:
        print(result[0].calculate_pop())
    
    return result

def run4():

    self = call_tbl()
    comp = 'DTH'
    comp_in_comp_end = False
    method = '1dist'
    pop_sex = 'Sex'
    pop_age = 'Age'
    pop_end = 'Postcensal Population'
    problematic_sex = 1

    pop_groups = self.get_pop_groups()
    comp_J = f"{comp}_J"
    dfs_comp = self.get_J(comp)
    df_comp_modifiable = dfs_comp['records.to_modify']
    df_comp_counter_adjust = dfs_comp['records.to_counter']
    df_comp_counter_adjust_reversed = df_comp_counter_adjust\
        .sort_values(pop_groups, ascending = [True, False])
    to_modify_val_total = df_comp_modifiable[comp_J].sum()

    print("df_comp_modifiable:")
    print(df_comp_modifiable)
    print("df_comp_counter_adjust_reversed:")
    print(df_comp_counter_adjust_reversed)

    comp_K = f"{comp}_K"
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
        print("result so far:")
        print(result)
        use_2nd_pass = get_option('method_use.second_pass')
        if to_modify_val_total != 0 and use_2nd_pass:
            # The first pass wasn't enough so that to_modify_val_total
            # didn't come down to 0.
            # Apply the second pass only if the option says so
            print("The second pass has started.")
            max_correctables -= np.array(result)
            print("df_comp_counter_adjust_reversed:")
            print(df_comp_counter_adjust_reversed)
            print("New max_correctables:")
            print(max_correctables)
            for i, item in enumerate(max_correctables):
                if item > 0 and to_modify_val_total != 0:
                    result[i] += 1
                    to_modify_val_total -= 1
                print("to_modify_val_total:")
                print(to_modify_val_total)
                print("result:")
                print(result)

    elif method == 'filler':
        for index, row in df_comp_counter_adjust_reversed.iterrows():
            if row[comp_J] > 0 and to_modify_val_total != 0:
                min_comp_J_val = min(row[comp_J], to_modify_val_total)
                result.append(min_comp_J_val)
                to_modify_val_total -= min_comp_J_val
            else:
                result.append(0)
    else: # proportional method
        problematic_sex = df_comp_modifiable[pop_sex].values[0]
        prop_max_age = df_comp_counter_adjust_reversed\
            .iloc[0, :]\
            [pop_age]
        prop_min_age = df_comp_counter_adjust_reversed\
            .iloc[-1, :]\
            [pop_age]
        if not comp_in_comp_end:
            prop_max_age += 1
            prop_min_age += 1
        calculated_pop = self.calculate_pop()
        pop_end_to_compare_reversed = calculated_pop.copy()\
            .loc[lambda df: df[pop_sex] == problematic_sex]\
            .loc[lambda df: df[pop_age] <= prop_max_age]\
            .loc[lambda df: df[pop_age] >= prop_min_age]\
            .sort_values(pop_groups, ascending = [True, False])
        print("pop_end_to_compare_reversed:")
        print(pop_end_to_compare_reversed)

        prop_size = get_option('age.prop_size')
        pop_end_for_prop =\
            pop_end_to_compare_reversed.iloc[:, -1].values
        if comp_in_comp_end:
            pop_end_for_prop[0] = 0
        
        print("pop_end_for_prop:")
        print(pop_end_for_prop)
        print("max_correctables:")
        print(max_correctables)
        
        pop_end_len = len(pop_end_for_prop)
        for i in np.arange(pop_end_len, step = prop_size):
            period = [i, min(i + prop_size, pop_end_len)]
            props_numer = pop_end_for_prop[period[0]:period[1]]
            props_denom = sum(props_numer)
            props = props_numer / props_denom
            print("to_modify_val_total before:")
            print(to_modify_val_total)
            print("props:")
            print(props)
            props_x_m = np.array(
                list(map(int, np.round(to_modify_val_total * props)))
            )
            print("props_x_m:")
            print(props_x_m)
            max_correct_for_each =\
                max_correctables[period[0]:period[1]]
            print("max_correct_for_each:")
            print(max_correct_for_each)
            min_from_each = np.minimum(props_x_m, max_correct_for_each)
            print("min_from_each:")
            print(min_from_each)
            loc_max_prop = np.where(props == max(props))[0][0]
            print("loc_max_prop:")
            print(loc_max_prop)
            sum_min_from_each = sum(min_from_each)
            to_modify_val_total -= sum_min_from_each
            print("to_modify_val_total after:")
            print(to_modify_val_total)
            if props_x_m[loc_max_prop] <= max_correct_for_each[loc_max_prop]:
                more_possible_correction =\
                    max_correct_for_each[loc_max_prop] -\
                    props_x_m[loc_max_prop]
                print("more_possible_correction:")
                print(more_possible_correction)
                min_mod_cor = min(
                    to_modify_val_total,
                    more_possible_correction
                )
                min_from_each[loc_max_prop] += min_mod_cor
                to_modify_val_total -= min_mod_cor
                print("min_from_each further:")
                print(min_from_each)
                print("to_modify_val_total after further:")
                print(to_modify_val_total)
                result.extend(min_from_each)
            else:
                result.extend(min_from_each)
            print("result:")
            print(result)
            print(len(result))
            print("")

    df_comp_counter_adjust_reversed[comp_K] = result
    del df_comp_counter_adjust_reversed[comp_J]
    df_comp_counter_adjust_reversed\
        .sort_values(
            pop_groups, 
            ascending = [True, True], 
            inplace = True
        )
    
    return df_comp_counter_adjust_reversed

def run5():
    result = call_tbl2()

    pop_2001 = result['pop_2001']
    bth = result['bth']
    dth_d01 = result['dth_d01']
    dth_d02 = result['dth_d02']
    imm = result['imm']
    emi = result['emi']
    rem = result['rem']
    nte = result['nte']
    mip = result['mip']
    mit = result['mit']
    npr = result['npr']
    pop_2002_orig = result['pop_2002_orig']
    pop_2002_corrected = result['pop_2002_corrected']
    
    nprs = arrange_by_lvl(npr, RegionSD, 'NPR')
    tbl =\
        arrange_by_lvl(pop_2001, RegionS, 'InitialPopulation')\
        .merge(
            bth[RegionS + ['Total']]\
                .assign(Age = -1)\
                .rename(columns = {'Total': 'BTH'})\
                [RegionSA + ['BTH']],
            on = RegionSA,
            how = 'outer'
        )\
        .sort_values(RegionSA)\
        .fillna(0)\
        .assign(
            InitialPopulation = lambda df: df.InitialPopulation.apply(int),
            BTH = lambda df: df.BTH.apply(int)
        )\
        .rename(
            columns = {'InitialPopulation': 'POP_2001'}
        )\
        .merge(
            arrange_by_lvl(dth_d01, RegionS, 'DTH_D01'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(imm, RegionS, 'IMM'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(emi, RegionS, 'EMI'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(rem, RegionS, 'REM'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(nte, RegionS, 'NTE'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(mip, RegionS, 'MIP'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(mit, RegionS, 'MIT'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            nprs.loc[
                lambda df: df['RefDate'] < np.datetime64('2002-01-01')
            ]\
            [RegionSA + ['NPR']]\
            .rename(columns = {'NPR': 'NPR_out'}),
            on = RegionSA,
            how = 'outer'
        )\
        .merge(
            nprs.loc[
                lambda df: df['RefDate'] > np.datetime64('2002-01-01')
            ]\
            [RegionSA + ['NPR']]\
            .rename(columns = {'NPR': 'NPR_in'}),
            on = RegionSA,
            how = 'outer'
        )\
        .fillna(0)\
        .assign(
            NPR_out = lambda df: df.NPR_out.apply(int),
            NPR_in = lambda df: df.NPR_in.apply(int)
        )\
        .assign(
            MIP_out = lambda df: df.MIP.apply(lambda x: abs(min(x, 0))),
            MIP_in = lambda df: df.MIP.apply(lambda x: max(x, 0)),
            MIT_out = lambda df: df.MIT.apply(lambda x: abs(min(x, 0))),    
            MIT_in = lambda df: df.MIT.apply(lambda x: max(x, 0))
        )
    selected_cols = tbl.columns.tolist()
    selected_cols.remove('MIP')
    selected_cols.remove('MIT')
    tbl = tbl[selected_cols]
    
    all_RegionC = np.unique(tbl[RegionSAD[0]])
    poptbl_regions = {}
    for region in all_RegionC:
        tbl_region =\
            tbl\
            .query(f"{RegionSAD[0]} == {region}")\
            [selected_cols[1:]]
        with estime2.option_context(
            'pop.sex', 'Sex',
            'pop.age', 'Age',
            'pop.end', 'POP_2002',
            'pop.start', 'POP_2001',
            'pop.birth', 'BTH',
            'comp_neg.temp_out', 'NTE',
            'comp_neg.emi', 'EMI',
            'comp_neg.npr_out', 'NPR_out',
            'comp_neg.death', 'DTH_D01',
            'comp_neg.interprov_out', 'MIP_out',
            'comp_neg.etc', ['MIT_out'],
            'comp_pos.ret_emi', 'REM',
            'comp_pos.npr_in', 'NPR_in',
            'comp_pos.immi', 'IMM',
            'comp_pos.interprov_in', 'MIP_in',
            'comp_pos.etc', ['MIT_in'],
            'comp.end', ['NPR_in']
        ):
            poptbl_regions[region] = estime2.ProvPopTable(tbl_region)
    
    return poptbl_regions

def run6():
    poptbl_regions = run5()
    poptbl_1001 = poptbl_regions[1001]
    poptbl_1010 = poptbl_regions[1010]
    estime2.options.method = '1dist'
    poptbl_1001_fixed_onedist =\
        poptbl_1001.fix_issues(return_all_mods = True)
    poptbl_1010_fixed_onedist =\
        poptbl_1010.fix_issues(return_all_mods = True)
    
    print(poptbl_1001_fixed_onedist.summary())
    print('')
    print(poptbl_1010_fixed_onedist.summary())
    print('')

    estime2.options.method = 'filler'
    poptbl_1001_fixed_filler =\
        poptbl_1001.fix_issues(return_all_mods = True)
    poptbl_1010_fixed_filler =\
        poptbl_1010.fix_issues(return_all_mods = True)
    
    print(poptbl_1001_fixed_filler.summary())
    print('')
    print(poptbl_1010_fixed_filler.summary())
    print('')

    estime2.options.method = 'prop'
    poptbl_1001_fixed_prop =\
        poptbl_1001.fix_issues(return_all_mods = True)
    poptbl_1010_fixed_prop =\
        poptbl_1010.fix_issues(return_all_mods = True)

    print(poptbl_1001_fixed_prop.summary())
    print('')
    print(poptbl_1010_fixed_prop.summary())
    print('')
