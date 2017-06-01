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


def read_folder(folderpath, sheetname='output', header=0, check_date_format=False, date_format="w-sat"):
    """
    loops through excel files in folder and concatenates output sheets to
    produce a epsilon object

    sheets must be in specific format
    """
    import os
    import pandas as pd
    import fnmatch
    date_formats = {
        "w-mon": 0,
        "w-tue": 1,
        "w-wed": 2,
        "w-thu": 3,
        "w-fri": 4,
        "w-sat": 5,
        "w-sun": 6
    }

    # find excel workbook paths in subfolders
    matches = []
    for root, dirnames, filenames in os.walk(folderpath):
        for filename in fnmatch.filter(filenames, '*.xlsx'):
            matches.append(os.path.join(root, filename))
    matches = [x for x in matches if "~" not in x]
    success = []

    data = []
    for i, file in enumerate(matches):
        print("Processing file {0} of ".format(i + 1) +
              str(len(matches) + 1), end="\r")
        try:
            temp = pd.read_excel(file, sheetname=sheetname, header=header)
            temp.name = file
            temp = temp.set_index('date')
            data.append(temp)
            success.append(file)

        except:
            pass

    if check_date_format:
        for df in data:
            df.index = df.index.to_datetime()
            dayofweek = date_formats[date_format]
            # trying to check that columns have been named properly
            if not type(df.columns) == pd.indexes.base.Index:
                raise ValueError("columns have not been named" +
                                 " for " + df.name)
            if all(df.index.dayofweek != dayofweek):
                raise ValueError("dates are not all " +
                                 date_format + " for " + df.name)
    print("successfully loaded the following files " + str(success))
    df = pd.concat(data, axis=1)
    df.to_csv(folderpath + '/AllData.csv')

    return EO(df)
