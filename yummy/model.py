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