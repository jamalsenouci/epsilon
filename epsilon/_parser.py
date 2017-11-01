def read(df):
    """reads from DataFrame to create epsilon object"""
    from epsilon.core import EO
    return EO(df)

def read_folder(folderpath, sheetname='output', header=0, check_date_format=False, date_format="w-sat"):
    """
    loops through excel files in folder and concatenates output sheets to
    produce a epsilon object
    """
    from epsilon.core import EO
    import os
    import pandas as pd
    import fnmatch
    import pyarrow as pa
    import pyarrow.parquet as pq

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
        temp = pd.read_excel(file,
                             sheetname=sheetname,
                             header=header,
                             index_col=0)
        temp.name = file
        data.append(temp)
        success.append(file)


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
    table = pa.Table.from_pandas(df)
    pq.write_table(table, folderpath + '/AllData.parquet')

    return EO(df)
