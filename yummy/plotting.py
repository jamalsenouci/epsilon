import bokeh.plotting as bk
import bokeh
bokeh.plotting.output_notebook()
def line2(varlist, namelist=None):
    """takes in a dataframe and plots series as lines"""
    from pandas.core.series import Series
    from pandas.tseries.index import DatetimeIndex
    
    if namelist is None:
        if isinstance(varlist, Series):
            namelist = varlist.name
        else:
            namelist = varlist.columns
    
    obs = varlist.index
    if isinstance(obs, DatetimeIndex):
        obs = obs.map(lambda x: x.strftime('%d-%b-%y'))
    obs = obs.tolist()
    
    plot = bk.Figure(plot_width=900, plot_height=500, x_range=obs)
    plot.xaxis.major_label_orientation = np.pi/3
    plot.left[0].formatter.use_scientific = False
    for i in range(varlist):
        plot.line(obs, varlist.ix[:,i], legend=namelist[i])
    return bk.show(plot)

def line(df, namelist=None):
    from bokeh.charts import Line
    from pandas.core.series import Series
    if namelist is not None:
        if isinstance(df, Series):
            df.name = namelist
        else:
            df.columns = namelist
    plt = Line(df)    
    bk.show(plt)
    