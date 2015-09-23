import bokeh.plotting as bk
import bokeh

_colors = ['#1f77b4',
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
    """takes dataframe and plots a line chart"""
    from bokeh.charts import Line
    from pandas.core.series import Series
    from bokeh.models import HoverTool, ColumnDataSource

    import numpy as np
    if namelist is not None:
        if isinstance(df, Series):
            df.name = namelist
        else:
            df.columns = namelist

    hover = HoverTool(
        tooltips=[
            ("obs", "$index"),
            ("Date", "@date"),
            ("Value", "@y"),
            ("Variable", "@variable")
        ]
    )

    plot = bk.figure(plot_width=900, plot_height=500, x_axis_type="datetime",tools=[hover,"pan","wheel_zoom","box_zoom","reset","resize"])
    plot.left[0].formatter.use_scientific = False
    plot.xgrid.grid_line_color = None
    
    obs = df.index.to_datetime()
    #obs = np.array(df.index, dtype=np.datetime64)
    if isinstance(df, Series):
      source = ColumnDataSource({'x': obs, 'y': df.values , 'date': [x.strftime('%d %b %Y') for x in obs],'variable':[df.name for x in obs]})
      plot.circle('x', 'y', source=source, size=4, color='darkgrey', alpha=0.1, legend=df.name)
      plot.line(obs, df.values, color='navy', legend=df.name)
    else:
        for i, col in enumerate(df):
          source = ColumnDataSource({'x': obs, 'y': df[col].values , 'date': df.index.format(), 'variable':[df[col].name for x in obs]})
          plot.circle('x', 'y', source=source, size=4, color=_colors[i], alpha=0.2, legend=col)
          plot.line(obs, df[col].values, color=_colors[i], legend=col)
    bk.show(plot)

def stackedBarAndLine(line,stackedbar, namelist=None):
    """TODO: Datetime index
              Use ColumnDataSource to allow HoverTool to pick var name"""
    from pandas.tseries.index import DatetimeIndex
    import numpy as np
    from bokeh.models import HoverTool, ColumnDataSource
    
    obs = np.array(line.index, dtype=np.datetime64)
    hover = HoverTool(
        tooltips=[
            ("obs", "$index"),
            ("Date", "($x)"),
            ("Value", "($y)"),
            ("Variable", "(@variable)")
        ]
    )
    plot = bk.figure(plot_width=900, plot_height=500, 
                    x_axis_type=None, tools=[hover,"pan","wheel_zoom","box_zoom","reset","resize"])
    plot.left[0].formatter.use_scientific = False 
    plot.axis.major_tick_line_color = None
    plot.xaxis.major_label_orientation = np.pi/3
    pos_sum = 0
    neg_sum = 0
    for i, contrib in enumerate(stackedbar):
        name = contrib
        contrib = stackedbar[contrib] #check this is equivalent to contrib then remove
        if contrib.max() > 0:
            #source = ColumnDataSource({'x': obs, 'y': pos_sum+contrib/2, 'variable': contrib})
            plot.rect(x='x', y='y', source=source, width=1, height=contrib, 
                      color=_colors[i], alpha=0.6, legend=name)
            pos_sum += contrib
        else:
            #source = ColumnDataSource({'x': obs, 'y': neg_sum+contrib/2 })
            plot.rect(x='x', y='y', source=source, width=1, height=contrib, 
                      color=_colors[i], alpha=0.6, legend=name)
            neg_sum += contrib
            line -= contrib
    plot.line(x=obs, y=line, line_dash=[4, 4], color='#000000', 
              legend=line.name)
    return bk.show(plot)

def stackedBarAndLine2(line,stackedbar, namelist=None):
    """TODO: Datetime index"""
    from pandas.tseries.index import DatetimeIndex
    import numpy as np
    from bokeh.models import HoverTool, ColumnDataSource
    
    obs = line.index
    if isinstance(obs, DatetimeIndex):
        obs = obs.map(lambda x: x.strftime('%d-%b-%y'))
    obs = obs.tolist()
    hover = HoverTool(
        tooltips=[
            ("obs", "$index"),
            ("Date", "$x"),
            ("Value", "@y"),
            ("Variable", "@variable")
        ]
    )
    plot = bk.figure(plot_width=900, plot_height=500, x_range=obs,
                    x_axis_type=None, tools=[hover,"pan","wheel_zoom","box_zoom","reset","resize"])
    plot.left[0].formatter.use_scientific = False 
    plot.grid.grid_line_color = None
    plot.axis.major_tick_line_color = None
    plot.xaxis.major_label_orientation = np.pi/3
    #ticker = bokeh.models.formatters.DatetimeTickFormatter()
    #xaxis = bokeh.models.DatetimeAxis(num_labels=10)
    #plot.add_layout(xaxis, 'below')
    pos_sum = 0
    neg_sum = 0
    for i, contrib in enumerate(stackedbar):
        name = contrib
        contrib = stackedbar[contrib] #check this is equivalent to contrib then remove
        if contrib.max() > 0:
            source = ColumnDataSource({'x': obs, 'y': pos_sum+contrib/2, 'variable': [str(name) for x in obs]})
            plot.rect(x='x',y='y', source=source, width=1, height=contrib, 
                      color=_colors[i], alpha=0.6, legend=name)
            pos_sum += contrib
        else:
            source = ColumnDataSource({'x': obs, 'y': neg_sum+contrib/2 })
            plot.rect(x='x',y='y', source=source, width=1, height=contrib, 
                      color=_colors[i], alpha=0.6, legend=name)
            neg_sum += contrib
            line -= contrib
    plot.line(x=obs, y=line, line_dash=[4, 4], color='#000000', 
              legend='Sales')
    return bk.show(plot)