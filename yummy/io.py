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