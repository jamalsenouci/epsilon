import pandas as pd
import numpy as np
class Data(pd.DataFrame):
    """ Wrapper around a Pandas DataFrame providing convenience methods specific to modelling
    
    Parameters
    ----------
    dataframe : Pandas DataFrame

    Examples
    --------
    >>> d = {'col1': ts1, 'col2': ts2}
    >>> df = DataFrame(data=d, index=index)
    >>> Data(df)

    See also
    --------
    yummy.load
    """
    
    def __init__(self, data=None, index=None, columns=None, dtype=None,copy=False):
        super(Data, self).__init__(data, index, columns, dtype, copy)
    
    def pow(self, var, power, inplace=True):
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

    def decay(self, var, decays=None,inplace=True):
        """
        decays a variable
        
        
        Example
        -------
            ``ym.data.decay(["Mother's Day Media Spend","Suncare Media Spend"], [0.9,0.8], inplace=True)``
        
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
            for i in range(1,N):
                cur = df[i]
                decayed = ((alpha * decayed) + cur)
                output[i] = decayed
            return output
        if isinstance(decays, float):
            decays = [decays]
        total = []
        for dec in decays:
            decays = subset.apply(lambda x: _decay(x,dec))
            if isinstance(decays, pd.core.series.Series):
                decays.name = str(decays.name)+' Dec'+str(dec)
            else:
                decays.columns = decays.columns.map(lambda x: str(x)+' Dec'+str(dec))
            total.append(decays)
        total = pd.concat(total, axis=1)
        result = pd.concat([self, total], axis=1)
        if inplace:
            self._update_inplace(result)
        else:
            return result
        
    
    def mult(self, var, newname=None, inplace=True):
        if not len(var)==2:
            raise ValueError("must pass of list of exactly two variable names to multiply")
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

class Model(object):
    
    def __init__(self, data):
        self.data = Data(data)
        self.variables_in = set()
        self.variables_out = set(self.data.columns.tolist())
        self.variables = pd.DataFrame(self.data.columns.tolist(), columns=['Variable Name'])
        self.depvar = None
        self.obs = self.data.index
        self.actual = None
        self.model = None
        self.res = None
        self.fitdetail = None
        
    def add(self, variables):
        if isinstance(variables, str):
            variables = [variables]
        for var in variables:
            if var in self.variables_in:
                print(var + " already in model")
            elif var in self.variables_out:
                self.variables_in.add(var)
                self.variables_out.remove(var)
            else:
                raise ValueError(var+" not in dataset")
    
    def rem(self, variables):
        if isinstance(variables, str):
            variables = [variables]
        for var in variables:
            if var in self.variables_in:
                self.variables_in.remove(var)
                self.variables_out.add(var)
            else:
                print(var + " not in model")
    
    def dep(self, name):
        if name in self.variables_in:
            self.variables_in.remove(name)
            print('Dependent Variable removed from variables in to prevent the model from being suspiciously too good')
        if name in self.variables_out:
            self.variables_out.remove(name)
            self.depvar = self.data[name]
        else:
            print(name + " not in data")
    
    def fit(self):
        Y = self.depvar
        x = self.data[self.variables_in]
        x = sm.add_constant(x)
        model = sm.OLS(Y,x)
        fit = model.fit()
        self.fitdetail = fit
        return fit.summary()

    def period(self, period):
        pass
    
    def fix(self, variables, values):
        pass
    
    def avm(self):
        predict = self.fitdetail.predict()
        obs = self.obs
        obs = obs.map(lambda x: x.strftime('%d-%b-%y')).tolist()
        model = pd.Series(predict, index=obs, name='Model')
        actual = self.depvar
        plot = bk.Figure(plot_width=900, plot_height=500, x_range=obs)
        plot.xaxis.major_label_orientation = np.pi/3
        plot.left[0].formatter.use_scientific = False 
        plot.line(obs,model, legend='Model')
        plot.line(obs,actual, legend='Actual')
        return bk.show(plot)
    
    def con(self):
        obs = self.obs
        obs = obs.map(lambda x: x.strftime('%d-%b-%y')).tolist()
        actual = self.depvar
        exog = self.fitdetail.model.exog
        coeffs = self.fitdetail.params.values
        contribs = (exog*coeffs)
        contribs = pd.DataFrame(contribs, index=obs, columns=self.fitdetail.params.keys())
        plot = bk.figure(plot_width=900, plot_height=500, x_range=obs, x_axis_type=None)
        plot.left[0].formatter.use_scientific = False 
        plot.grid.grid_line_color = None
        plot.axis.major_tick_line_color = None
        plot.xaxis.major_label_orientation = np.pi/3
        #ticker = bokeh.models.formatters.DatetimeTickFormatter()
        #xaxis = bokeh.models.DatetimeAxis(num_labels=10)
        #plot.add_layout(xaxis, 'below')
        colors = ['#1f77b4',
                  '#ff7f0e',
                  '#2ca02c',
                  '#d62728',
                  '#9467bd',
                  '#8c564b',
                  '#e377c2',
                  '#7f7f7f',
                  '#bcbd22',
                  '#17becf',
                  '#e377c2',
                  '#7f7f7f',
                  '#bcbd22',
                  '#aec7e8',
                  '#ffbb78',
                  '#98df8a',
                  '#ff9896']
        pos_sum = 0
        neg_sum = 0
        for i, contrib in enumerate(contribs):
            name = contrib
            contrib = contribs[contrib]
            if contrib.max() > 0:
                plot.rect(x=obs, y=pos_sum+contrib/2, width=1, height=contrib, color=colors[i], alpha=0.6, legend=name)
                pos_sum += contrib
            else:
                plot.rect(x=obs, y=neg_sum+contrib/2, width=1, height=contrib, color=colors[i], alpha=0.6)
                neg_sum += contrib
                actual -= contrib
        plot.line(x=obs, y=actual, line_dash=[4, 4], color='#000000', legend='Sales')
        return bk.show(plot)
    
    def _update_model_series(self):
        predict = fit.predict()
        self.model = pd.Series(predict, index=obs, name='Model')
        self.actual = df['Value Sales']
        self.res = fit.resid
        self.avm = pd.concat([actual,model], axis=1)
    
    def _update_variables(self):
        self.variables_out = set(self.data.columns.tolist()) - self.variables_in
        self.variables = pd.DataFrame(self.variables_out, columns=['Variable Name'])
        

class Plotting(object):
    
    import bokeh.plotting as bk
    import bokeh
    bokeh.plotting.output_notebook()
    def __init__(self):
        pass
    
    def plot(data,x,y):
        plot = bk.Figure()
        x = data[x]
        y = data[y]
        plot.line(x=x,y=y)
        return bk.show(plot)
        
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
    
    def __init__(self, data):
        self.model = Model(data)
        self.data = self.model.data
        self.plotting = Plotting()
        self.model.plot = self.plotting.plot