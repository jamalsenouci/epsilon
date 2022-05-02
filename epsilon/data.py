import numpy as np
import pandas as pd


class Data(pd.DataFrame):
    """
    Wrapper around a Pandas DataFrame providing data
    transformation methods specific to marketing modelling

    Parameters
    ----------
    dataframe : Pandas DataFrame

    Examples
    --------
    >>> from pandas import DataFrame
    >>> import numpy as np
    >>> df = DataFrame(data = {'a': [True, False] * 3,
    ...                 'b': [1.0, 2.0] * 3}, index=[0,1,2,3,4,5])
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
    epsilon.load

    """

    def __init__(self, data=None, index=None, columns=None, dtype=None,
                 copy=False):
        super(Data, self).__init__(data, index, columns, dtype, copy)
        from epsilon._utils import has_variation, convert_categoricals
        from warnings import warn
        from textwrap import dedent
        convert_categoricals(data)
        model_data = has_variation(data)
        num_omitted_vars = len(data.columns) - len(model_data.columns)
        omitted_vars = set(data.columns).difference(set(model_data.columns))
        if num_omitted_vars > 0:
            warn(
                dedent("""
                    {x} variables have been removed as they have no
                    variation across the dataset {vars}""").format(
                    x=str(num_omitted_vars), vars=omitted_vars)
            )
        columns = self.columns.str.lower()
        columns = columns.str.strip(" ")
        columns = columns.str.replace(" ", "_")
        self.columns = columns
        self.index = self.index.to_datetime()

    def handle_duplicate(self):
        """to deal with import of duplicate data"""
        raise NotImplementedError()

    @staticmethod
    def _check_duplicates_names(df):
        seen = set()
        dup = []
        for col in df.columns:
            if col not in seen:
                seen.add(col)
            else:
                dup.append(col)
        return dup

    def pow(self, var, power, inplace=True):
        """
        Create new variable that is a specified
        variable raised to a given power

        Also works on multiple variables.
        """
        subset = self[var].fillna(0)
        powered = subset.pow(power)
        powered = self._df_rename(powered, "**", power)
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def _df_rename(self, df, suffix, param):
        """
        internal function to rename variables that have been transformed
        """
        if isinstance(df, pd.core.series.Series):
            df.name = str(df.name)+suffix+str(param)
            if df.name in self.columns:
                df = None
        else:
            df.columns = df.columns.map(lambda x: str(x)+suffix+str(param))
            unique_df = df[df.columns.difference(self.columns)]
            # TODO print warning if variables already exist df.columns is different from new_df.columns
        return unique_df

    def lag(self, var, lag, val, inplace=True):
        """
        Create a new variable that is a lag or lead of a specified variable.

        Also works on multiple variables.
        """
        subset = self[var].fillna(0)
        if lag == 0:
            raise ValueError("A lag of zero is pointless!")
        lagged = subset.shift(lag)
        if lag > 0:
            lagged.iloc[:lag] = val
        else:
            lagged.iloc[lag:] = val
        lagged = self._df_rename(lagged, "_lag", lag)
        result = pd.concat([self, lagged], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def atan(self, var, alphas, inplace=True):
        """
        Create a new variable that is an atan transformation of a specified
        variable. Used to model diminishing returns, creates a concave
        transformation

        Also works on multiple variables.
        """
        subset = self[var].fillna(0)
        std = subset.div(subset.max())
        if not isinstance(alphas, list):
            alphas = [alphas]
        total = []
        for alpha in alphas:
            atan = (np.arctan(std/alpha))/(np.pi/2)
            atan = self._df_rename(atan, "_atan", alpha)
            total.append(atan)
        total = pd.concat(total, axis=1)
        result = pd.concat([self, total], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def atansq(self, var, alphas, inplace=True):
        """
        Create a new variable that is a squared atan transformation of a
        specified variable. Used to model either diminishing and increasing
        returns, creates an s-shaped transformation

        Also works on multiple variables.
        """
        subset = self[var].fillna(0)
        std = subset.div(subset.max())
        if not isinstance(alphas, list):
            alphas = [alphas]
        total = []
        for alpha in alphas:
            atansq = (np.arctan(std/alpha)**2)/(np.pi/2)
            atansq = self._df_rename(atansq, "_atansq", alpha)
            total.append(atansq)
        total = pd.concat(total, axis=1)
        result = pd.concat([self, total], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def adstock(self, var, adstocks, inplace=True):
        """
        Create adstock(s) of a variable(s)
        Used to model advertising carryover into the next period.
        Also works on multiple variables.

        Example
        -------
            ym.data.adstock(["Mother's Day Media Spend",
                             "Suncare Media Spend"],
                             adstocks=[0.9,0.8])``

        Attributes
        ----------
        var: list or string
        decays: list or float
        inplace: boolean
        """
        if isinstance(adstocks, float):
            adstocks = [adstocks]
        decays = [1-adstock for adstock in adstocks]
        subset = self[var]
        subset = subset.fillna(0)

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
            applied = self._df_rename(applied, "_adstock", dec)
            total.append(applied)
        total = pd.concat(total, axis=1)
        result = pd.concat([self, total], axis=1)
        # import pdb; pdb.set_trace()
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def decay(self, var, decays, inplace=True):
        """
        Create a new variable that decays away over time
        Used to model advertising carryover into the next period.
        Also works on multiple variables.
        decays a variable

        Example
        -------
            ym.data.decay(["Mother's Day Media Spend","Suncare Media Spend"],
                          [0.9,0.8])``

        Attributes
        ----------
        var: list or string
        decays: list or float
        inplace: boolean
        """

        subset = self[var]
        subset = subset.fillna(0)

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
            applied = self._df_rename(applied, "_dec", dec)
            total.append(applied)
        total = pd.concat(total, axis=1)
        result = pd.concat([self, total], axis=1)
        # import pdb; pdb.set_trace()
        if inplace:
            self._update_inplace(result)
        else:
            return result

    def mult(self, var, newname=None, inplace=True):
        """
        Create a new variable that is a multiplicative combination of two
        variables. Used to model interaction between two variables.
        e.g. Promotion and Media

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

    def to_frame(self):
        """convert epsilon Data object to pandas DataFrame"""
        from pandas import DataFrame
        return DataFrame(self)

    def line(self, var):
        """Convenience method to chart variables together"""
        import epsilon.plotting as plt
        subset = self[var]
        subset = pd.DataFrame(subset)

        if self._check_duplicates_names(subset) != []:
            raise NameError('variables with duplicate names selected')

        obs = subset.index
        plt.line(subset)
