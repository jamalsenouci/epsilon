def grid_display(dataframe):
    # qgrid has no tests
    import qgrid
    qgrid.nbinstall()
    return qgrid.show_grid(dataframe)
