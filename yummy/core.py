class Yummy(object):
    """ Yummy class wraps up data, modelling and plotting functionality

    Parameters
    ----------
    dataframe : Pandas DataFrame

    Examples
    --------
    >>> from pandas import DataFrame
    >>> import numpy as np
    >>> df = DataFrame({'a': [True, False] * 3,
    ...                 'b': [1.0, 2.0] * 3})
    >>> yo = Yummy(df)
    >>> yo.data
           a  b
    0   True  1
    1  False  2
    2   True  1
    3  False  2
    4   True  1
    5  False  2
    
    
    See also
    --------
    yummy.load
    """
    def __init__(self, data):
        from yummy.model import Model
        from yummy.plotting import Plotting
        
        self.model = Model(data)
        self.data = self.model.data
        self.plotting = Plotting()
        #self.model.plot = self.plotting.plot