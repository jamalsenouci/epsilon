import pandas as pd
import numpy as np
class Data(pd.DataFrame):
    """ Wrapper around a Pandas DataFrame providing convenience methods specific to modelling
    
    Parameters
    ----------
    dataframe : Pandas DataFrame

    Examples
    --------
    >>> from pandas import DataFrame
    >>> import numpy as np
    >>> df = DataFrame({'a': [True, False] * 3,
    ...                 'b': [1.0, 2.0] * 3})
    >>> data = Data(df)
    >>> data
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
    
    def __init__(self, data=None, index=None, columns=None, dtype=None,copy=False):
        super(Data, self).__init__(data, index, columns, dtype, copy)
    
    def pow(self, var, power, inplace=True):
        """
        Create new variable that is a specified variable raised to a given power
        
        Also works on multiple variables.
        """
        subset = self[var]
        powered = subset.pow(power)
        if isinstance(powered, pd.core.series.Series):
            powered.name = str(powered.name)+'**'+str(power)
        else:
            powered.columns = powered.columns.map(lambda x: str(x)+'**'+str(power))
        result = pd.concat([self, powered], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result
        
    def lag(self, var, lag, val, inplace=True):
        """
        Create a new variable that is a lag or lead of a specified variable.
        
        Also works on multiple variables.
        """
        subset = self[var]
        if lag == 0:
            raise ValueError("A lag of zero is pointless!")
        lagged = subset.shift(lag)
        if lag > 0:
            lagged.iloc[:lag] = val
        else:
            lagged.iloc[-lag+1:] = val
        if isinstance(lagged, pd.core.series.Series):
            lagged.name = str(lagged.name)+' lag'+str(lag)
        else:
            lagged.columns = lagged.columns.map(lambda x: str(x)+' Lag'+str(lag))
        result = pd.concat([self, lagged], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def atan(self, var, alphas,inplace=True):
        """
        Create a new variable that is an atan transformation of a specified variable.
        Used to model diminishing returns, creates a concave transformation
        
        Also works on multiple variables.
        """
        subset = self[var]
        std = subset.div(subset.max())
        if not isinstance(alphas, list):
            alphas = [alphas]
        total = []
        for alpha in alphas:
            atan = (np.arctan(std/alpha))/(np.pi/2)
            if isinstance(atan, pd.core.series.Series):
                atan.name = str(atan.name)+' Atan'+str(alpha)
            else:
                atan.columns = atan.columns.map(lambda x: str(x)+' Atan'+str(alpha))
            total.append(atan)
        total = pd.concat(total, axis=1)
        result = pd.concat([self, atan], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result
    
    def atansq(self, var, alphas, inplace=True):
        """
        Create a new variable that is a squared atan transformation of a specified variable.
        Used to model either diminishing and increasing returns, creates an s-shaped transformation
        
        Also works on multiple variables.
        """
        subset = self[var]
        std = subset.div(subset.max())
        if not isinstance(alphas, list):
            alphas = [alphas]
        total = []
        for alpha in alphas:
            atansq = (np.arctan(std/alpha)**2)/(np.pi/2)
            if isinstance(atansq, pd.core.series.Series):
                atansq.name = str(atansq.name)+' AtanSq'+str(alpha)
            else:
                atansq.columns = atansq.columns.map(lambda x: str(x)+' AtanSq'+str(alpha))
            total.append(atansq)
        total = pd.concat(total, axis=1)
        result = pd.concat([self, total], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def decay(self, var, decays=None, inplace=True):
        """
        Create a new variable that decays away over time
        Used to model advertising carryover into the next period.
        Also works on multiple variables.
        decays a variable

        Example
        -------
            ym.data.decay(["Mother's Day Media Spend","Suncare Media Spend"], [0.9,0.8], inplace=True)``

        Attributes
        ----------
        var: list or string
        decays: list or float
        inplace: boolean            
        """

        subset = self[var]
        def _decay(df, dec):
            alpha = 1 - dec
            N = len(df)
            output = np.array(np.empty(N, dtype=float))
            decayed = df[0]
            output[0] = decayed
            for i in range(1, N):
                cur = df[i]
                decayed = ((alpha * decayed) + cur)
                output[i] = decayed
            return output
        if isinstance(decays, float):
            decays = [decays]
        total = []
        for dec in decays:
            applied = subset.apply(lambda x: _decay(x, dec))
            if isinstance(applied, pd.core.series.Series):
                applied.name = str(applied.name) + ' Dec'+str(dec)
            else:
                applied.columns = applied.columns + ' Dec'+str(dec)
            total.append(applied)
        total = pd.concat(total, axis=1)
        result = pd.concat([self, total], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def mult(self, var, newname=None, inplace=True):
        """
        Create a new variable that is a multiplicative combination of two variables.
        Used to model interaction between two variables. e.g. Promotion and Media
        
        Also works on multiple variables.
        decays a variable
        """
        if not len(var) == 2:
            raise ValueError("must pass of list of exactly two \
                variable names to multiply")
        multiplied = self[var[0]].mul(self[var[1]])
        if newname is None:
            name = var[0]+'*'+var[1]
        else:
            name = newname
        multiplied.name = name
        result = pd.concat([self, multiplied], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result
