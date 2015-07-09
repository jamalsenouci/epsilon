from yummy.core import Yummy

def read_csv(filepath, *args):
    df = pd.read_csv(filepath, args)
    return Yummy(df)

def read_excel(filepath, sheetname, *args):
    df = pd.read_excel(filepath, sheetname, args)
    return Yummy(df)
