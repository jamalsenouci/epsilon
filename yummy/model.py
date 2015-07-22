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
        self.sample = self.obs
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
        #set sample obs
        pass
    
    def fix(self, variables, values):
        """fix a variable coefficient to a specified number based on other information"""
        pass
    
    def group(self):
        """place variables_in into contribution groups"""
        #import pandas-qt
    
    def avm(self):
        """produce a line chart of actual data vs fitted data"""
        import yummy.plotting as plt
        from pandas import Series
        from pandas import concat
        
        obs = self.obs
        actual = self.depvar
        predict = self.fitdetail.predict()
        model = Series(predict, index=obs, name='Model')
        
        combined = concat([actual, model], axis=1)
        plt.line(combined)
    
    def con(self):
        """Produce a contribution chart. A stacked chart of all the components
        that make up the dependent variable"""
        from pandas import DataFrame
        import yummy.plotting as plt
        
        obs = self.obs
        actual = self.depvar
        exog = self.fitdetail.model.exog
        coeffs = self.fitdetail.params.values
        contribs = (exog*coeffs)
        
        contribs = DataFrame(contribs, index=obs, columns=self.fitdetail
                            .params.keys())
        plt.stackedBarAndLine(actual, contribs)

    def _update_variables(self):
        """internal function that updates the variables_out with new variables
        that have been added to the dataset"""
        from pandas import DataFrame
        allvars = self.data.columns.tolist()
        self.variables_out = set(allvars) - self.variables_in
        self.variables = DataFrame(allvars, columns=['Variable Name'])