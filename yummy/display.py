def grid_display(dataframe):
	import qgrid
	qgrid.nbinstall()
	return qgrid.show_grid(dataframe)