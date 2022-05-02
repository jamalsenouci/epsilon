from numpy.testing import assert_array_almost_equal
from epsilon.core import EO
import pandas as pd
import numpy as np
import pytest


@pytest.fixture
def combined():
    ints = [[1, 2], [3, 4], [5, 6]]
    df = pd.DataFrame(ints,
                      index=["1999-01-01", "1999-01-02", "1999-01-03"],
                      columns=['Sales', 'Marketing Spend'])
    df.iloc[2, :] = np.nan
    eo = EO(df)
    eo.model.dep('sales')
    eo.model.ols()
    obs = eo.model.obs()
    actual = eo.model.depvar[eo.model.sample[0]]
    predict = eo.model.fitdetail.predict()
    model = pd.Series(predict, index=obs, name='Model')
    combined = pd.concat([actual, model], axis=1)
    return combined


def test_avm_shape(combined):
    if (combined.shape != (2, 2)):
        raise AssertionError


def test_avm_val(combined):
    print(combined.values)
    assert_array_almost_equal(combined.values, np.array([[1., 2.], [3., 2.]]))
