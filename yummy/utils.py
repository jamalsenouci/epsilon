def drop_constant(data):
    keepcolumns = data.columns[data.std() != 0]
    data = data[keepcolumns]
    return data
