import yummy as ym
import statsmodels.api as sm

data = sm.datasets.engel.load_pandas()
df = data.data

x = ym.Yummy(df)

x.data.corr()

