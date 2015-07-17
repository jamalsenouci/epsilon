class Plotting(object):
    
    import bokeh.plotting as bk
    import bokeh
    bokeh.plotting.output_notebook()
    def __init__(self):
        pass
    
    def line(data,x,y):
        plot = bk.Figure(plot_width=900, plot_height=500, x_range=obs)
        plot.xaxis.major_label_orientation = np.pi/3
        plot.left[0].formatter.use_scientific = False 
        plot.line(obs,model, legend='Model')
        plot.line(obs,actual, legend='Actual')
        return bk.show(plot)
    