import epsilon._parser
import os
import shutil
import numpy as np
import pandas as pd
import pytest

@pytest.fixture(scope='module')
def df():
    ints = np.random.randint(1, 10, size=(3, 2))
    df = pd.DataFrame(ints,
                      index=["1999-01-01", "1999-01-02", "1999-01-03"],
                      columns=['Sales', 'Marketing Spend'])
    df.iloc[2, :] = np.nan
    return df


def test_read(df):
    eo = epsilon._parser.read(df)
