from epsilon.core import EO


def read_csv(filepath):
    """reads from csv to create epsilon object"""
    from pandas import read_csv
    df = read_csv(filepath, index_col=0)
    return EO(df)

def read_df(df):
    """reads from DataFrame to create epsilon object"""
    return EO(df)


def read_excel(filepath, sheetname):
    """reads from excel to create epsilon object"""
    from pandas import read_excel
    df = pd.read_excel(filepath, sheetname, args)
    return EO(df)


def read_folder(folderpath):
    """
    loops through excel files in folder and concatenates output sheets to
    produce a epsilon object

    sheets must be in specific format
    """
    import os
    import pandas as pd
    import fnmatch

    if os.path.exists(folderpath + "/AllData.csv"):
        return read_csv(folderpath + "/AllData.csv")
    else:

        # find excel workbook paths in subfolders
        matches = []
        for root, dirnames, filenames in os.walk(folderpath):
            for filename in fnmatch.filter(filenames, '*.xlsx'):
                matches.append(os.path.join(root, filename))
        matches = [x for x in matches if "~" not in x]

        data = []
        for i, file in enumerate(matches):
            print("Processing file {0} of ".format(i + 1)
                  + str(len(matches) + 1), end="\r")
            try:
                temp = pd.read_excel(file, sheetname='Output', header=3)
                data.append(temp)
            except:
                pass
        df = pd.concat(data, axis=1)
        df.to_csv(folderpath + '/AllData.csv')

        return EO(df)
