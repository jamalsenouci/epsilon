class Yummy(object):
    """ Yummy class wraps up data, modelling and plotting functionality

    Parameters
    ----------
    dataframe : Pandas DataFrame

    Examples
    --------
    >>> d = {'col1': ts1, 'col2': ts2}
    >>> df = DataFrame(data=d, index=index)
    >>> Yummy(df)

    See also
    --------
    yummy.load
    """
    from yummy.model import Model
    from yummy.data import Data
    from yummy.plotting import Plotting
    
    def __init__(self, data):
        self.model = Model(data)
        self.data = self.model.data
        self.plotting = Plotting()
        self.model.plot = self.plotting.plot