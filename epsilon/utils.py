def has_variation(data):
    keepcolumns = data.columns[data.std() != 0]
    return keepcolumns
