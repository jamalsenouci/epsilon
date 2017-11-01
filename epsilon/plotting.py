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
        self._model = model

    def avm(self):
        """Produce a line chart of actual data vs fitted data."""
        from pandas import concat
        from pandas import Series

        obs = self._model.obs()
        actual = self._model.depvar[self._model.sample[0]]
        predict = self._model.fitdetail.predict()
        model = Series(predict, index=obs, name='Model')

        combined = concat([actual, model], axis=1)
        line(combined)

    def con(self):
        """Produce a contribution chart. A stacked chart of all the components
        that make up the dependent variable"""
        from pandas import DataFrame
        obs = self._model.obs()
        actual = self._model.depvar[self._model.sample[0] == 1]
        exog = self._model.fitdetail.model.exog
        coeffs = self._model.fitdetail.params.values
        contribs = (exog*coeffs)

        contribs = DataFrame(contribs, index=obs,
                             columns=self._model.fitdetail.params.keys())
        stackedBarAndLine(actual, contribs)

    def res(self, percent=True):
        """
        Produce a residual chart.

        Parameters
        ----------
        percent : Boolean
                display in percentage terms
        """

        resid = self._model.fitdetail.resid
        if percent is True:
            resid = self._model.fitdetail.resid.div(
                self._model.fitdetail.model.endog)
            resid.columns = ["Residuals"]
        resid.name = "Residuals"
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
        from pandas import concat

        df = self._model.data.ix[self._model.sample[0], subset]
        if dep is True:
            df = concat([self._model.depvar, df], axis=1)
        line(df)


def line(df, dep=None, namelist=None):
    """
    takes dataframe and plots a line chart

    Parameters
    ---------

    df : the dataframe of series to chart
    namelist : a list of display names if variable names are not desirable

    """
    from pandas.core.series import Series
    from bokeh.models import HoverTool, ColumnDataSource

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

    plot = bk.figure(plot_width=900, plot_height=500, x_axis_type="datetime",
                     tools=[hover, "pan", "wheel_zoom", "box_zoom", "reset"])
    plot.left[0].formatter.use_scientific = False
    plot.xgrid.grid_line_color = None

    obs = df.index.to_datetime()
    # obs = np.array(df.index, dtype=np.datetime64)
    if isinstance(df, Series):
        source = ColumnDataSource({'x': obs, 'y': df.values,
                                   'date': [x.strftime('%d %b %Y') for x in obs],
                                   'variable': [df.name for x in obs]})
        plot.circle('x', 'y', source=source, size=4, color='darkgrey',
                    alpha=0.1, legend=df.name)
        plot.line('x', 'y', source=source, color='navy', legend=df.name)
    else:
        for i, col in enumerate(df.columns):
            source = ColumnDataSource({'x': obs, 'y': df[col].values,
                                       'date': df.index.format(),
                                       'variable': [df[col].name for x in obs]})
            plot.circle('x', 'y', source=source, size=4, color=_colors[i],
                        alpha=0.2, legend=col)
            plot.line('x', 'y', source=source, color=_colors[i], legend=col)
    bk.show(plot)


def stackedBarAndLine(line, stackedbar, namelist=None):
    """TODO: Datetime index"""
    from pandas import DatetimeIndex
    import numpy as np
    from bokeh.models import HoverTool, ColumnDataSource, Range1d

    hover = HoverTool(
        tooltips=[
            ("obs", "$index"),
            ("Date", "@obs_fmt"),
            ("Value", "@y"),
            ("Variable", "@variable")
        ]
    )

    obs = stackedbar.index
    xrange = Range1d(start=obs[0], end=obs[-1])
    if isinstance(obs, DatetimeIndex):
        obs_fmt = obs.map(lambda x: x.strftime('%d-%b-%y'))
        obs_fmt = obs_fmt.tolist()
    else:
        obs_fmt = obs.tolist()

    plot = bk.figure(plot_width=900, plot_height=500, x_range=xrange, tools=[hover, "pan", "wheel_zoom",
                                                                             "box_zoom", "reset"])
    plot.left[0].formatter.use_scientific = False
    plot.xaxis.major_label_orientation = np.pi/3
    plot.xaxis.axis_label = "Date"
    plot.yaxis.axis_label = "Contribution"

    pos_sum = 0
    neg_sum = 0
    for i, contrib in enumerate(stackedbar):
        name = contrib
        contrib = stackedbar[contrib]
        if contrib.max() > 0:
            datasource = ColumnDataSource({'x': obs, 'y': pos_sum+contrib/2,
                                           'obs_fmt': obs_fmt,
                                           'variable': [str(name) for x in obs],
                                           'color': [_colors[i] for x in obs],
                                           'contrib': contrib})
            plot.rect(x='x', y='y', source=datasource, width=7, height='contrib',
                      color='color', alpha=0.6, legend=name, dilate=True)
            pos_sum += contrib
        else:
            datasource = ColumnDataSource({'x': obs, 'y': neg_sum+contrib/2,
                                           'obs_fmt': obs_fmt,
                                           'variable': [str(name) for x in obs],
                                           'color': [_colors[i] for x in obs],
                                           'contrib': contrib})
            plot.rect(x='x', y='y', source=datasource, width=7, height='contrib',
                      color='color', alpha=0.6, legend=name)
            neg_sum += contrib
    datasource = ColumnDataSource({'x': obs, 'y': line, 'obs_fmt': obs_fmt,
                                   'variable': [line.name for x in obs]})
    plot.line(x='x', y='y', source=datasource, line_dash=[4, 4], color='#000000',
              legend='variable')

    bk.show(plot)
