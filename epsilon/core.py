class EO:
    """ epsilon class wraps up data, modelling and plotting functionality.

    Parameters
    ----------
    dataframe : Pandas DataFrame

    Examples
    --------
    >>> from pandas import DataFrame
    >>> import numpy as np
    >>> df = DataFrame({'a': [True, False] * 3,
    ...                 'b': [1.0, 2.0] * 3})
    >>> eo = EO(df)
    >>> eo.data
           a  b
    0   True  1
    1  False  2
    2   True  1
    3  False  2
    4   True  1
    5  False  2


    See also
    --------
    epsilon.load
    """

    def __init__(self, data):
        from epsilon.model import Model
        self.model = Model(data)
        self.data = self.model.data

    def reset(self):
        """
        Function to reset data back to original dataset.

        useful when you overwrite variable, doesn't require network access

        """
        from epsilon.model import Model
        import pyarrow.parquet as pq
        table = pq.read_table("data/rawdata.parquet")
        rawdata = table.to_pandas()
        self.model = Model(rawdata)
        self.data = rawdata


def help():
    """function forwards user to documentation."""
    import webbrowser
    webbrowser.open_new_tab('http://localhost:6757')
