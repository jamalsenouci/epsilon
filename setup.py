import sys
from setuptools import setup

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (2, 7):
    print("Yummy requires Python 2.7 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

install_requires=[
    'numpy',
    'pandas',
    'bokeh'
]
packages = ["yummy"]

if __name__ == "__main__":

    setup(
        name             = "yummy",
        version          = "0.0.1",
        maintainer       = "jamal senouci",
        maintainer_email = "jamal.senouci@outlook.co.uk",
        author           = 'jamal senouci',
        author_email     = "jamal.senouci@outlook.co.uk",
        description      = "Python package for marketing mix modelling",
        keywords         = ['Marketing', 'Econometrics', 'Modelling', 'Statistical'],
        long_description = "Python package for marketing mix modelling",
        license          = 'BSD',
        platforms        = ['Windows'],
        url              = 'http://yummy.github.io/',
        download_url     = 'https://github.com/jamalsenouci/yummy/',
        classifiers      = "",
        install_requires = install_requires,
        packages         = packages,
        test_suite       = 'nose.collector',
        tests_require    = ['nose>=0.10.1'],
        zip_safe         = False
    )