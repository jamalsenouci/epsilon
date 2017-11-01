
def create_project(name, filepath="./"):
    """
    Initialises an epsilon compatible project structure
    """
    import os
    if os.path.exists(filepath + name):
        os.chdir(filepath + name)
        print("Project already exists - you are now working in that directory")
    else:
        os.mkdir(filepath + name)
        os.mkdir(filepath + name + "/config")
        os.mkdir(filepath + name + "/data")
        os.mkdir(filepath + name + "/processing")
        os.mkdir(filepath + name + "/models")
        os.mkdir(filepath + name + "/output")
        os.chdir(filepath + name)
        print("New project created")


def convert_categoricals(data):
    """
    converts non-numeric variables to categoricals
    """
    import numpy as np
    categorical_cols = data.select_dtypes(exclude=[np.number]).columns
    data[categorical_cols] = data[categorical_cols].apply(
        lambda x: x.astype('category'))


def has_variation(data):
    """
    Calculates whether a variable has any variation across the dataset
    """
    import numpy as np
    import pandas as pd

    numeric_data = data.select_dtypes(include=[np.number])
    categorical_data = data.select_dtypes(exclude=[np.number])
    numeric_hasvariation = numeric_data.ix[:, numeric_data.std() != 0]
    numeric_hasvariation = pd.DataFrame(numeric_hasvariation)
    categorical_hasvariation = categorical_data.ix[:, categorical_data.apply(
        lambda x: len(set(x)) > 1)]
    categorical_hasvariation = pd.DataFrame(categorical_hasvariation)
    data_hasvariation = pd.concat([numeric_hasvariation,
                                   categorical_hasvariation], axis=1)
    return data_hasvariation
