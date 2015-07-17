class Model(object):
    """ The modelling component of the yummy package keeps track of the 
    endogenous and exogenous variables that are entered. fits the model and 
    captures the stats 
    
    """
    def __init__(self, data):
        from yummy.data import Data
        from pandas import DataFrame
        self.data = Data(data)
        self.variables_in = set()
        self._update_variables()
        self.depvar = None
        self.obs = self.data.index
        self.actual = None
        self.model = None
        self.res = None
        self.period = None
        self.fitdetail = None
        
    def add(self, variables):
        """add variables to the model, variables will be placed into the variables_in method"""
        #ensure latest variables are in the variable list 
        self._update_variables()
        
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
        """remove variables from the model, variables will be placed back into the variables_out method"""
        #ensure latest variables are in the variable list 
        _update_variables()
        
        if isinstance(variables, str):
            variables = [variables]
        for var in variables:
            if var in self.variables_in:
                self.variables_in.remove(var)
                self.variables_out.add(var)
            else:
                print(var + " not in model")
    
    def dep(self, name):
        """set the dependent variable, can be a single name for a simple linear 
        regression. Panel regression not yet implemented.
        """
        if name in self.variables_in:
            self.variables_in.remove(name)
            print('Dependent Variable removed from variables in to prevent the \
            model from being suspiciously too good')
        if name in self.variables_out:
            self.variables_out.remove(name)
            self.depvar = self.data[name]
        else:
            print(name + " not in data")
    
    def ols(self):
        """fits the specified endogenous and exogenous variables with an OLS
        estimation"""
        import statsmodels.api as sm
        modeltype = sm.OLS
        return self._fit(modeltype)
        
    def _fit(self, modeltype):
        """generic statsmodels fit function that takes any statsmodels 
        estimation method"""
        import statsmodels.api as sm
        Y = self.depvar
        x = self.data[list(self.variables_in)]
        x = sm.add_constant(x)
        modelspec = modeltype(Y,x)
        fit = modelspec.fit()
        self.fitdetail = fit
        return fit.summary()

    def sample(self, period):
        """restrict the modelling period to a sample of the total dataset"""
        pass
    
    def fix(self, variables, values):
        pass
    
    def avm(self):
        """produce a line chart of actual data vs fitted data"""
        from pandas import Series
        
        predict = self.fitdetail.predict()
        obs = self.obs
        obs = obs.map(lambda x: x.strftime('%d-%b-%y')).tolist()
        model = Series(predict, index=obs, name='Model')
        actual = self.depvar
        
        plot = bk.Figure(plot_width=900, plot_height=500, x_range=obs)
        plot.xaxis.major_label_orientation = np.pi/3
        plot.left[0].formatter.use_scientific = False 
        plot.line(obs,model, legend='Model')
        plot.line(obs,actual, legend='Actual')
        return bk.show(plot)
    
    def con(self):
        """Produce a contribution chart. A stacked chart of all the components
        that make up the dependent variable"""
        from pandas import DataFrame
        obs = self.obs
        obs = obs.map(lambda x: x.strftime('%d-%b-%y')).tolist()
        actual = self.depvar
        exog = self.fitdetail.model.exog
        coeffs = self.fitdetail.params.values
        contribs = (exog*coeffs)
        contribs = DataFrame(contribs, index=obs, columns=self.fitdetail
                            .params.keys())
        plot = bk.figure(plot_width=900, plot_height=500, x_range=obs, 
                        x_axis_type=None)
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
                plot.rect(x=obs, y=pos_sum+contrib/2, width=1, height=contrib, 
                          color=colors[i], alpha=0.6, legend=name)
                pos_sum += contrib
            else:
                plot.rect(x=obs, y=neg_sum+contrib/2, width=1, height=contrib, 
                          color=colors[i], alpha=0.6)
                neg_sum += contrib
                actual -= contrib
        plot.line(x=obs, y=actual, line_dash=[4, 4], color='#000000', 
                  legend='Sales')
        return bk.show(plot)
    
    def _update_variables(self):
        """internal function that updates the variables_out with new variables
        that have been added to the dataset"""
        from pandas import DataFrame
        allvars = self.data.columns.tolist()
        self.variables_out = set(allvars) - self.variables_in
        self.variables = DataFrame(allvars, columns=['Variable Name'])