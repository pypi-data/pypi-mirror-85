# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['many', 'many.stats', 'many.visuals']

package_data = \
{'': ['*']}

install_requires = \
['adjusttext>=0.7.3,<0.8.0',
 'flake8>=3.8.3,<4.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.0,<2.0.0',
 'scipy>=1.5.2,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.11.1,<0.12.0',
 'tqdm>=4.48.2,<5.0.0']

setup_kwargs = {
    'name': 'many',
    'version': '0.6.0',
    'description': '',
    'long_description': '# many\n\nThis package provides a general-use toolkit for frequently-implemented statistical and visual methods. See the [blog post](https://kevinhu.io/2020/09/17/many.html) for an explanation of the purpose of this package and the methods used.\n\n**[Full documentation](https://many.kevinhu.io)**\n\n## Installation\n\n```bash\npip install many\n```\n\nNote: if you want to use CUDA-accelerated statistical methods (i.e. `many.stats.mat_mwu_gpu`), you must also independently install the corresponding version of [cupy](https://github.com/cupy/cupy).\n\n## Components\n\n### Statistical methods\n\nThe statistical methods comprise several functions for association mining between variable pairs. These methods are optimized for `pandas` DataFrames and are inspired by the `corrcoef` function provided by `numpy`.\n\nBecause these functions rely on native matrix-level operations provided by `numpy`, many are orders of magnitude faster than naive looping-based alternatives. This makes them useful for constructing large association networks or for feature extraction, which have important uses in areas such as biomarker discovery. All methods also return estimates of statistical significance.\n\nIn certain cases such as the computation of correlation coefficients, **these vectorized methods come with the caveat of [numerical instability](https://stats.stackexchange.com/questions/94056/instability-of-one-pass-algorithm-for-correlation-coefficient)**. As a compromise, "naive" loop-based implementations are also provided for testing and comparison. It is recommended that any significant results obtained with the vectorized methods be verified with these base methods.\n\nThe current functions available are listed below by variable comparison type. Benchmarks are also provided with comparisons to the equivalent looping-based method. In all methods, a `melt` option is provided to return the outputs as a set of row-column variable-variable pair statistic matrices or as a single `DataFrame` with each statistic melted to a column.\n\n### Visual methods\n\nSeveral visual methods are also included for interpretation of results from the statistical methods. Like the statistical methods, these are also grouped by variable types plotted.\n\n## Development\n\n1. Install dependencies with `poetry install`\n2. Initialize environment with `poetry shell`\n3. Initialize pre-commit hooks with `pre-commit install`\n',
    'author': 'Kevin Hu',
    'author_email': 'kevinhuwest@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kevinhu/many',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
