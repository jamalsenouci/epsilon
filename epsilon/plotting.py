import bokeh.plotting as bk
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


class ModelPlots(object):

    def __init__(self, model):
        self.model = model

    def avm(self):
        """Produce a line chart of actual data vs fitted data."""
        from pandas import concat
        from pandas import Series

        obs = self.model.obs()
        actual = self.model.depvar[self.model.sample[0]]
        predict = self.model.fitdetail.predict()
        model = Series(predict, index=obs, name='Model')

        combined = concat([actual, model], axis=1)
        line(combined)

    def con(self):
        """Produce a contribution chart. A stacked chart of all the components
        that make up the dependent variable"""
        from pandas import DataFrame
        obs = self.model.obs()
        actual = self.model.depvar[self.model.sample[0] == 1]
        exog = self.model.fitdetail.model.exog
        coeffs = self.model.fitdetail.params.values
        contribs = (exog*coeffs)

        contribs = DataFrame(contribs, index=obs,
                             columns=self.model.fitdetail.params.keys())
        stackedBarAndLine(actual, contribs)

    def res(self, percent=True):
        """
        Produce a residual chart.

        Parameters
        ----------
        percent : Boolean
                display in percentage terms
        """

        resid = self.model.fitdetail.resid
        resid.name = "Residuals"
        if percent is True:
            resid = self.model.fitdetail.resid / \
                self.model.fitdetail.model.endog
        line(resid)

    def plot(self, subset, dep=False, sample=True):
        """
        Produce a plot of the variable.

        Parameters
        ----------
        subset : list or string
                variable or list of variables to plot
        dep : Boolean, default False
                plot variable against the dependent variable
        sample : True
                only plot observations within the model sample period

        """
        self.data[self.sample == 1]
        if dep is True:
            df = self.data[subset]


def line2(varlist, namelist=None):
    """takes in a dataframe and plots series as lines"""
    import numpy as np
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
        plot.line(obs, varlist.ix[:, i], legend=namelist[i])
    return bk.show(plot)


def line(df, namelist=None):
    """
    takes dataframe and plots a line chart

    Parameters
    ---------

    df : the dataframe of series to chart
    namelist : a list of display names if variable names are not desirable

    """
    from bokeh.charts import Line
    from pandas.core.series import Series
    from bokeh.models import HoverTool, ColumnDataSource

    if namelist is not None:
        if isinstance(df, Series):
            df.name = namelist
        else:
            df.columns = namelist

    # http://stackoverflow.com/questions/31496628/in-bokeh-how-do-i-add-tooltips-to-a-timeseries-chart-hover-tool
    hover = HoverTool(
        tooltips=[
            ("obs", "$index"),
            ("Date", "@date"),
            ("Value", "@y"),
            ("Variable", "@variable")
        ]
    )

    plot = bk.figure(plot_width=900, plot_height=500, x_axis_type="datetime",
                     tools=[hover, "pan", "wheel_zoom", "box_zoom", "reset",
                            "resize"])
    plot.left[0].formatter.use_scientific = False
    plot.xgrid.grid_line_color = None

    obs = df.index.to_datetime()
    # obs = np.array(df.index, dtype=np.datetime64)
    if isinstance(df, Series):
        source = ColumnDataSource({'x': obs, 'y': df.values,
                                   'date': [x.strftime('%d %b %Y') for x in obs],
                                   'variable': [df.name for x in obs]})
        plot.line('x', 'y', source=source, color='darkgrey', legend=df.name)
        plot.circle('x', 'y', source=source, size=4, color='darkgrey',
                    alpha=0.1, legend=df.name)
    else:
        for i, col in enumerate(df.columns):
            source = ColumnDataSource({'x': obs, 'y': df[col].values,
                                       'date': df.index.format(),
                                       'variable': [df[col].name for x in obs]})
            plot.line('x', 'y', source=source, color=_colors[i], legend=col)
            plot.circle('x', 'y', source=source, size=4, color=_colors[i],
                        alpha=0.2, legend=col)
    bk.show(plot)


"""
def stackedBarAndLine(line, stackedbar, namelist=None):
    # TODO: Datetime index
    # TODO: use ColumnDataSource to allow HoverTool to pick var name
    import numpy as np
    from pandas.tseries.index import DatetimeIndex
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
                     x_axis_type=None, tools=[hover, "pan", "wheel_zoom",
                                              "box_zoom", "reset", "resize"])
    plot.left[0].formatter.use_scientific = False
    plot.axis.major_tick_line_color = None
    plot.xaxis.major_label_orientation = np.pi/3
    pos_sum = 0
    neg_sum = 0
    for i, contrib in enumerate(stackedbar):
        name = contrib
        # check this is equivalent to contrib then remove
        contrib = stackedbar[contrib]
        if contrib.max() > 0:
            # source = ColumnDataSource({'x': obs, 'y': pos_sum+contrib/2, 'variable': contrib})
            plot.rect(x='x', y='y', source=source, width=1, height=contrib,
                      color=_colors[i], alpha=0.6, legend=name)
            pos_sum += contrib
        else:
            # source = ColumnDataSource({'x': obs, 'y': neg_sum+contrib/2 })
            plot.rect(x='x', y='y', source=source, width=1, height=contrib,
                      color=_colors[i], alpha=0.6, legend=name)
            neg_sum += contrib
            line -= contrib
    plot.line(x=obs, y=line, line_dash=[4, 4], color='#000000',
              legend=line.name)
    return bk.show(plot)
"""


def stackedBarAndLine(line, stackedbar, namelist=None):
    """TODO: Datetime index"""
    import numpy as np
    from pandas import DatetimeIndex
    from bokeh.models import HoverTool, ColumnDataSource, Legend

    obs = stackedbar.index
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
                     x_axis_type=None, tools=[hover, "pan", "wheel_zoom",
                                              "box_zoom", "reset", "resize"])
    plot.left[0].formatter.use_scientific = False
    plot.axis.major_tick_line_color = None
    plot.xaxis.major_label_orientation = np.pi/3
    # ticker = bokeh.models.formatters.DatetimeTickFormatter()
    # xaxis = bokeh.models.DatetimeAxis(num_labels=10)
    # plot.add_layout(xaxis, 'below')
    pos_sum = 0
    neg_sum = 0
    items = []
    for i, contrib in enumerate(stackedbar):
        name = contrib
        # TODO: check this is equivalent to contrib then remove
        contrib = stackedbar[contrib]
        if contrib.max() > 0:
            source = ColumnDataSource({'x': obs, 'y': pos_sum+contrib/2,
                                       'variable': [str(name) for x in obs]})
            r1 = plot.rect(x='x', y='y', source=source, width=1, height=contrib,
                      color=_colors[i], alpha=0.6)
            pos_sum += contrib
        else:
            source = ColumnDataSource({'x': obs, 'y': neg_sum+contrib/2,
                                       'variable': [str(name) for x in obs]})
            r1 = plot.rect(x='x', y='y', source=source, width=1, height=contrib,
                      color=_colors[i], alpha=0.6)
            neg_sum += contrib
            line -= contrib
        items.append((name, [r1]))
    l1 = plot.line(x=obs, y=line, line_dash=[4, 4], color='#000000')
    items.append(("Sales", [l1]))
    legend = Legend(legends=items, location=(30, 0))
    plot.add_layout(legend, 'right')
    return bk.show(plot)
