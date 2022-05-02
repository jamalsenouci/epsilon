from numpy.testing import assert_array_equal
from epsilon.core import EO
import pandas as pd
import numpy as np
import pytest


@pytest.fixture(scope='module')
def df():
    ints = np.random.randint(1, 10, size=(3, 2))
    df = pd.DataFrame(ints,
                      index=["1999-01-01", "1999-01-02", "1999-01-03"],
                      columns=['Sales', 'Marketing Spend'])
    df.iloc[2, :] = np.nan
    return df


@pytest.fixture(scope='function')
def eo():
    ints = np.random.randint(1, 10, size=(3, 2))
    df = pd.DataFrame(ints,
                      index=["1999-01-01", "1999-01-02", "1999-01-03"],
                      columns=['Sales', 'Marketing Spend'])
    df.iloc[2, :] = np.nan
    eo = EO(df)
    eo.model.dep('sales')
    return eo


# test that depvar values are equal to the dataframe values
def test_dep_values(df):
    eo = EO(df)
    eo.model.dep('sales')
    assert_array_equal(eo.model.depvar.values, df.Sales.values)


# test that depvar is equal to chosen column
def test_dep_name(eo):
    if (eo.model.depvar.name != 'sales'):
        raise AssertionError


# test that depvar has been removed from the model if already an exogenous var
def test_dep_not_in(eo):
    eo.model.add('marketing_spend')
    eo.model.dep('marketing_spend')
    if ('marketing_spend' in eo.model.variables_in):
        raise AssertionError


# test that depvar is not available as an exogenous variable
def test_dep_not_out(eo):
    if ('sales' in eo.model.variables_out):
        raise AssertionError


# test that sample is as expected
def test_dep_sample(eo):
    assert_array_equal(eo.model.sample[0], [True, True, False])
    assert_array_equal(eo.model.sample[1], ['sales', 'marketing_spend'])


# test that model observations are the right length
def test_obs_len(eo):
    if (len(eo.model.obs()) != 2):
        raise AssertionError


# test that model observations are the right values
def test_obs_vals(eo):
    assert_array_equal(eo.model.obs(),
                       pd.date_range(start="1999-01-01",
                                     end="1999-01-02"))
