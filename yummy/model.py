class Model(object):
    """ The modelling component of the yummy package keeps track of the 
    endogenous and exogenous variables that are entered. fits the model and 
    captures the stats 
    
    """
    def __init__(self, data):
        from yummy.data import Data
        from pandas import DataFrame
        import numpy as np
        
        self.data = Data(data)
        self.rawdata = data
        self.variables_in = set()
        self.variables_out = None
        self.depvar = None
        self._update_variables()
        self.sample = DataFrame(np.ones(len(self.data.index)), index=self.data.index, columns=["Sample"])
        self.fitdetail = None
        
    def obs(self):
        obs = self.sample[self.sample == 1].index
        return obs

    def add(self, variables):
        """
        add variables to the model, variables will be placed into the 
        variables_in method
        
        Parameters
        ----------
        variables: list or string
                variable or list of variables to remove,
        """
        #TODO: add contribution groups
        #ensure latest variables are in the variable list 
        self._update_variables()
        
        if isinstance(variables, str):
            variables = [variables]
        for var in variables:
            if var in self.variables_out:
                self.variables_in.add(var)
                self.variables_out.remove(var)
            elif var not in self.variables_in:
                raise ValueError(var+" not in dataset")
    
    def rem(self, variables='all'):
        """
        remove variables from the model, variables will be placed back into 
        the variables_out method

        Parameters
        ----------
        variables: list or string, default 'all'
                variable or list of variables to remove,

        """
        #ensure latest variables are in the variable list 
        self._update_variables()

        if self.variables_in == set():
            return

        if variables == 'all':
            variables = list(self.variables_in)
        
        if isinstance(variables, str):
            variables = [variables]
        for var in variables:
            if var in self.variables_in:
                self.variables_in.remove(var)
                self.variables_out.add(var)
    
    def dep(self, name):
        """
        set the dependent variable, can be a single name for a simple linear 
        regression. Panel regression not yet implemented.
        
        Parameters
        ----------
        name : string
                the name of the dependent variable

        """
        if name in self.variables_in:
            self.variables_in.remove(name)
            print('Dependent Variable removed from variables in to prevent the \
            model from being suspiciously too good')
        if name in self.variables_out:
            self.variables_out.remove(name)
            depvar = self.data[name]
            #depvar = depvar.dropna(how="all", axis=0)            
            self.depvar = depvar
            #create sample based on dep var
            self.sample = self.data[depvar]/self.data[depvar]
        else:
            print(name + " not in data")
    
    def _get_exog(self):
        """function to prepare dataset for modelling"""
        df = self.data
        df = df[self.sample == 1]
        df = df.dropna(how="all", subset=[self.depvar.name], axis=0)
        df = df.fillna(0)
        df = df[list(self.variables_in)]
        return df

    def ols(self, constant=True):
        """
        fits the specified endogenous and exogenous variables with an OLS
        estimation

        Parameters
        ----------
        constant : Boolean, default True
                estimate the model with a constant
        """
        import statsmodels.api as sm
        
        x = self._get_exog()
        Y = self.depvar[self.sample == 1]
        if constant == True:
            x = sm.add_constant(x)
        modelspec = sm.OLS(Y,x)
        return self._fit(modelspec)

    def gls(self, constant=True, sigma=None):
        """fits the specified endogenous and exogenous variables with an OLS
        estimation"""
        import statsmodels.api as sm
        
        x = self._get_exog()
        Y = self.depvar[self.sample == 1]
        if constant == True:
            x = sm.add_constant(x)
        modelspec = sm.OLS(Y,x)
        return self._fit(modelspec)

    def rlm(self, constant=True, **kwargs):
        """fits the specified endogenous and exogenous variables with as a 
        robust linear model estimation"""
        import statsmodels.api as sm
        
        x = self._get_exog()
        Y = self.depvar[self.sample == 1]
        if constant == True:
            x = sm.add_constant(x)
        modelspec = sm.RLM(Y,x, **kwargs)
        return self._fit(modelspec)

    def var(self, lag='auto'):
        """needs to generalise fit function"""
        import statsmodels.api as sm

        if lag == 'auto':
            params = {'maxlags':15, 'ic':'aic'}
        else:
            params = {'maxlag':lag}
        variables = list(self.variables_in)
        variables.append(self.depvar.name)
        data = self.data(variables)
        modelspec = sm.tsa.VAR(data)
        
        return self._fit(modelspec, params)

        
    def _fit(self, modelspec, **kwargs):
        """generic statsmodels fit function that takes any statsmodels 
        estimation method"""
        import statsmodels.api as sm
        fit = modelspec.fit()
        self.fitdetail = fit
        return fit.summary()

    def sample(self, period):
        """restrict the modelling period to a sample of the total dataset"""
        #set sample obs handsontable widget
        pass
    
    def fix(self, variables, values):
        """fix a variable coefficient to a specified number based on other 
        information"""
        pass
    
    def ttest(self, subset="all", method='ols'):
        """
        view statistics for variables outside of the model if they were 
        entered into the model

        Parameters
        ----------
        subset : list or string
                variable or list of variables to test
        method : string, default ols
                estimation method to use
        """
        from yummy.display import grid_display
        from pandas import DataFrame

        if subset == "all":
            self._update_variables()
            subset = self.variables_out
        elif type(subset) == str:
            import re
            match = [re.match(subset, x) for x in self.data.columns]
            match = [x.string for x in match if x is not None]
            subset = match 
        params = []
        for var in subset:
            self.add(var)
            self.ols()
            params.append({"Variable Name":var, "coefficient":self.fitdetail.params[var], "t-stat":self.fitdetail.tvalues[var], "PValue":self.fitdetail.pvalues[var], "Adjusted Rsquared":self.fitdetail.rsquared_adj})
            self.rem(var)
        self.ols()
        params = DataFrame(params)
        params = params[params["coefficient"] != 0]
        params = params.set_index("Variable Name")
        return grid_display(params)

    def forecast(self, sample):
        pass
    
    def group(self):
        """place variables_in into contribution groups"""
        pass

    def export(self, path):
        """export model to csv"""
        pass
    
    def avm(self):
        """produce a line chart of actual data vs fitted data"""
        import yummy.plotting as plt
        from pandas import Series
        from pandas import concat
        
        obs = self.obs()
        actual = self.depvar[self.sample == 1]
        predict = self.fitdetail.predict()
        model = Series(predict, index=obs, name='Model')
        
        combined = concat([actual, model], axis=1)
        plt.line(combined)
    
    def con(self):
        """Produce a contribution chart. A stacked chart of all the components
        that make up the dependent variable"""
        from pandas import DataFrame
        import yummy.plotting as plt
        obs = self.obs()
        actual = self.depvar[self.sample == 1]
        exog = self.fitdetail.model.exog
        coeffs = self.fitdetail.params.values
        contribs = (exog*coeffs)
        
        contribs = DataFrame(contribs, index=obs, columns=self.fitdetail
                            .params.keys())
        plt.stackedBarAndLine2(actual, contribs)

    def res(self, percent=True):
        """
        produce a residual chart

        Parameters
        ----------
        percent : Boolean
                display in percentage terms
        """

        import yummy.plotting as plt
        obs = self.obs()
        resid = self.fitdetail.resid
        resid.name = "Residuals"
        if percent == True:
            resid = self.fitdetail.resid / self.fitdetail.model.endog
        plt.line(resid)

    def plot(self, subset, dep=False, sample=True):
        """
        produce a plot of the variable

        Parameters
        ----------
        subset : list or string
                variable or list of variables to plot
        dep : Boolean, default False
                plot variable against the dependent variable
        sample : True
                only plot observations within the model sample period

        """
        obs = self.obs()
        self.data[self.sample == 1]
        if dep == True:
            df = self.data[subset]
            



    def _update_variables(self):
        """internal function that updates the variables_out with new variables
        that have been added to the dataset"""
        from pandas import DataFrame
        allvars = self.data.columns.tolist()
        if self.depvar is not None:
        	self.variables_out = set(allvars) - self.variables_in - {self.depvar.name}
        else:
        	self.variables_out = set(allvars) - self.variables_in
        self.variables = DataFrame(allvars, columns=['Variable Name'])