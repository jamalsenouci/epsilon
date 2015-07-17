import yummy as ym
import statsmodels.api as sm

data = sm.datasets.engel.load_pandas()
df = data.data

yo = ym.Yummy(df)

yo.data.corr()

yo.model.dep('income')
yo.model.add('foodexp')
yo.model.ols()

