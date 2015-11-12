from nose import SkipTest
from nose.tools import assert_true
from yummy import Data
import pandas as pd

class TestData(object):
	numpy=1 # nosetests attribute, use nosetests -a 'not numpy' to skip test
	
	def __init__(self)
		self.r = pd.np.random.RandomState(seed=5)
		ints = self.r.random_integers(1, 10, size=(3,2))
	    df = pd.DataFrame(ints, columns=['Sales', 'Marketing Spend'])
	    self.df = df

	def test_pow()
