
<!-- README.md is generated from README.Rmd. Please edit that file -->

# `estime2`

[![pipeline
status](https://gitlab.com/joon3216/estime2/badges/master/pipeline.svg)](https://gitlab.com/joon3216/estime2/-/commits/master)
[![coverage
report](https://gitlab.com/joon3216/estime2/badges/master/coverage.svg)](https://gitlab.com/joon3216/estime2/-/commits/master)

[![PyPI version
shields.io](https://img.shields.io/pypi/v/estime2.svg)](https://pypi.python.org/pypi/estime2/)

This is a Python package to manipulate and make corrections on the
end-of-period population of a given table based on the component method.
The program aims to “distribute” values of components to other records
so that no end-of-period population estimates are negative. Moreover, it
incorporates sum constraints across regional levels, provincial and
subprovincial, so that the total end-of-period population is the same as
the original population table after it goes through the process.

Public version: <https://gitlab.com/joon3216/estime2> (private
repository)  
StatCan version: <https://f3eaipitcap01.statcan.ca/junkpar/estime2> (not
available to public)

Refer to
[documentations](https://gitlab.com/joon3216/estime2/-/tree/master/docs)
for details.

## Installation

In the command line, simply type:

``` bash
pip install estime2
```

To update to the latest version, type:

``` bash
pip install estime2 --upgrade
```

To install from source, first download the whole repository using a
proper `git clone` command. Then, move your working directory to that
repository, and type:

``` bash
python setup.py install --user
```

## Example

Suppose `tbl` is a `pandas.DataFrame` that qualifies to become a
`estime2.ProvPopTable`. Creating an instance of `ProvPopTable` is done
as follows:

``` python
import estime2
poptbl = estime2.ProvPopTable(tbl)
print(poptbl)
#>      Sex   Age  Initial Population  BTH  ...  NPR, 2019-07-01  IMM  IIM  RAI
#> 0      1    -1                   0  473  ...                0    0    5    2
#> 1      1     0                 455    0  ...                0    0   12    2
#> 2      1     1                 449    0  ...                0    0   10    2
#> 3      1     2                 446    0  ...                0    0   10    2
#> 4      1     3                 435    0  ...                0    0   11    2
#> ..   ...   ...                 ...  ...  ...              ...  ...  ...  ...
#> 97     1    96                   0    0  ...                0    0    0    1
#> 98     1    97                   0    0  ...                0    0    0    2
#> 99     1    98                   1    0  ...                0    0    0    2
#> 100    1    99                   0    0  ...                0    0    0    2
#> 101    1  100+                   1    0  ...                0    0    0    2
#> 
#> [102 rows x 15 columns]
```

See the source code for more information about the arguments of
`ProvPopTable`.

`ProvPopTable.calculate_pop()` is the method that computes the
end-of-period population:

``` python
calculated_poptbl = poptbl.calculate_pop()
print(calculated_poptbl)
#>      Sex   Age  Postcensal Population
#> 0      1     0                    461
#> 1      1     1                    449
#> 2      1     2                    446
#> 3      1     3                    442
#> 4      1     4                    435
#> ..   ...   ...                    ...
#> 96     1    96                      1
#> 97     1    97                     -4
#> 98     1    98                      1
#> 99     1    99                      2
#> 100    1  100+                      2
#> 
#> [101 rows x 3 columns]
```

Note that the total end-of-period population of `poptbl` before applying
the corrections is:

``` python
print(calculated_poptbl[estime2.options.pop.end].sum())
#> 20023
```

`estime2.options` has many global options available for the package to
work. See the source codes for details.

`ProvPopTable.fix_issues()` *returns* the fixed version of the original
`ProvPopTable` where there are no negative end-of-period population(s):

``` python
poptbl_fixed_tbl = poptbl.fix_issues()
print(poptbl_fixed_tbl)
#>      Sex   Age  Initial Population  BTH  ...  NPR, 2019-07-01  IMM  IIM  RAI
#> 0      1    -1                   0  473  ...                0    0    5    2
#> 1      1     0                 455    0  ...                0    0   12    2
#> 2      1     1                 449    0  ...                0    0   10    2
#> 3      1     2                 446    0  ...                0    0   10    2
#> 4      1     3                 435    0  ...                0    0   11    2
#> ..   ...   ...                 ...  ...  ...              ...  ...  ...  ...
#> 97     1    96                   0    0  ...                0    0    0    1
#> 98     1    97                   0    0  ...                0    0    0    2
#> 99     1    98                   1    0  ...                0    0    0    2
#> 100    1    99                   0    0  ...                0    0    0    2
#> 101    1  100+                   1    0  ...                0    0    0    2
#> 
#> [102 rows x 15 columns]
```

Any negative end-of-period is brought up to 0, and the
counter-modifications are applied to records of neighbouring ages:

``` python
calculated_poptbl_fixed = poptbl_fixed_tbl.calculate_pop()
print(calculated_poptbl_fixed)
#>      Sex   Age  Postcensal Population
#> 0      1     0                    461
#> 1      1     1                    449
#> 2      1     2                    446
#> 3      1     3                    442
#> 4      1     4                    435
#> ..   ...   ...                    ...
#> 96     1    96                      1
#> 97     1    97                      0
#> 98     1    98                      1
#> 99     1    99                      2
#> 100    1  100+                      2
#> 
#> [101 rows x 3 columns]
```

`ProvPopTable.fix_issues()` preserves the total end-of-period population
of the original table:

``` python
print(calculated_poptbl_fixed[estime2.options.pop.end].sum())
#> 20023
```

If you let `return_all_mods` to be `True` in
`ProvPopTable.fix_issues()`, you get the wrapper object which allows you
to compute relevant metrics:

``` python
poptbl_fixed = poptbl.fix_issues(return_all_mods = True)
```

For example, you may compute the standard deviation of all the
corrections applied to `poptbl` as follows:

``` python
poptbl_sd = poptbl_fixed.get_metric_sd()
print(poptbl_sd)
#>    Sex Age Component        sd
#> 0    1  97       DTH  2.236068
```

The wrapper object also comes with some visualization tools. For
example, you can visualize pre- and post-correction end-of-period
populations as follows:

``` python
poptbl_fixed.plot_pop(age_range = [87, 97])
```

<img src="./man/figures/README-intro11-1.png" width="100%" />
