from yummy.core import Yummy

def read_csv(filepath):
    from pandas import read_csv
    df = read_csv(filepath, index_col=0)
    return Yummy(df)

def read_excel(filepath, sheetname):
    from pandas import read_excel
    df = pd.read_excel(filepath, sheetname, args)
    return Yummy(df)
