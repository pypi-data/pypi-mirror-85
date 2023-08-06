# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scvi',
 'scvi.core',
 'scvi.core.data_loaders',
 'scvi.core.distributions',
 'scvi.core.models',
 'scvi.core.modules',
 'scvi.core.modules._base',
 'scvi.core.trainers',
 'scvi.core.utils',
 'scvi.data',
 'scvi.data._built_in_data',
 'scvi.inference',
 'scvi.model']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.7.5',
 'h5py>=2.9.0',
 'hyperopt==0.1.2',
 'ipywidgets',
 'numba>=0.41.0',
 'numpy>=1.17.0',
 'pandas>=1.0',
 'rich>=6.2.0',
 'scikit-learn>=0.21.2',
 'torch>=1.3',
 'tqdm>=4.31.1',
 'xlrd>=1.2.0']

extras_require = \
{':(python_version < "3.8") and (extra == "docs")': ['typing_extensions'],
 ':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'dev': ['black>=20.8b1',
         'codecov>=2.0.8',
         'flake8>=3.7.7',
         'jupyter>=1.0',
         'loompy>=3.0.6',
         'nbconvert>=5.4.0',
         'nbformat>=4.4.0',
         'pre-commit>=2.7.1',
         'prospector',
         'pytest>=4.4',
         'scanpy>=1.6'],
 'docs': ['ipython>=7.1.1',
          'nbsphinx',
          'nbsphinx-link',
          'pydata-sphinx-theme>=0.4.0',
          'scanpydoc>=0.5',
          'sphinx>=3.0,<4.0',
          'sphinx-autodoc-typehints'],
 'tutorials': ['leidenalg',
               'loompy>=3.0.6',
               'python-igraph',
               'scanpy>=1.6',
               'scikit-misc>=0.1.3']}

setup_kwargs = {
    'name': 'scvi-tools',
    'version': '0.8.0b0',
    'description': 'Deep generative models for end-to-end analysis of single-cell omics data.',
    'long_description': "==========\nscvi-tools\n==========\n\n|Stars| |PyPI| |BioConda| |Docs| |Build Status| |Coverage| |Code Style| |Downloads|\n\n.. |Stars| image:: https://img.shields.io/github/stars/YosefLab/scvi-tools?logo=GitHub&color=yellow\n   :target: https://github.com/YosefLab/scvi-tools/stargazers\n.. |PyPI| image:: https://img.shields.io/pypi/v/scvi-tools.svg\n    :target: https://pypi.org/project/scvi-tools\n.. |BioConda| image:: https://img.shields.io/conda/vn/bioconda/scvi-tools\n   :target: https://bioconda.github.io/recipes/scvi-tools/README.html\n.. |Docs| image:: https://readthedocs.org/projects/scvi/badge/?version=latest\n    :target: https://scvi.readthedocs.io/en/stable/?badge=stable\n    :alt: Documentation Status\n.. |Build Status| image:: https://travis-ci.com/YosefLab/scvi-tools.svg?branch=master\n    :target: https://travis-ci.com/YosefLab/scvi-tools\n.. |Coverage| image:: https://codecov.io/gh/YosefLab/scvi-tools/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/YosefLab/scvi-tools\n.. |Code Style| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/python/black\n.. |Downloads| image:: https://pepy.tech/badge/scvi-tools\n   :target: https://pepy.tech/project/scvi-tools\n\nscvi-tools (single-cell variational inference tools) is a package for end-to-end analysis of single-cell omics data. The package is composed of several deep generative models for omics data analysis, namely:\n\n* scVI_ for analysis of single-cell RNA-seq data, as well as its improved differential expression framework_\n* scANVI_ for cell annotation of scRNA-seq data using semi-labeled examples\n* totalVI_ for analysis of CITE-seq data\n* gimVI_ for imputation of missing genes in spatial transcriptomics from scRNA-seq data\n* AutoZI_ for assessing gene-specific levels of zero-inflation in scRNA-seq data\n* LDVAE_ for an interpretable linear factor model version of scVI\n\nTutorials, API reference, and installation guides are available in the documentation_.\nPlease use the issues here to submit bug reports.\nFor discussion of usage, checkout out our `forum`_.\nIf you'd like to contribute, check out our `development guide`_.\nIf you find a model useful for your research, please consider citing the corresponding publication (linked above).\n\nPackage transition\n------------------\n\n``scvi`` is now ``scvi-tools``. If you're looking for ``scvi`` source code, please use the branch tags. ``scvi`` is still available via pypi and bioconda, but there will be no future releases past ``0.6.8``. Documentation for ``scvi`` is available at the same documentation website.\n\n.. _documentation: https://scvi-tools.org/\n.. _`development guide`: https://scvi-tools.org/en/stable/development.html\n.. _scVI: https://rdcu.be/bdHYQ\n.. _scANVI: https://www.biorxiv.org/content/biorxiv/early/2019/01/29/532895.full.pdf\n.. _totalVI: https://www.biorxiv.org/content/10.1101/2020.05.08.083337v1.full.pdf\n.. _AutoZI: https://www.biorxiv.org/content/biorxiv/early/2019/10/10/794875.full.pdf\n.. _LDVAE: https://www.biorxiv.org/content/10.1101/737601v1.full.pdf\n.. _gimVI: https://arxiv.org/pdf/1905.02269.pdf\n.. _framework: https://www.biorxiv.org/content/biorxiv/early/2019/10/04/794289.full.pdf\n.. _forum: https://discourse.scvi-tools.org\n",
    'author': 'Romain Lopez',
    'author_email': 'romain_lopez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/YosefLab/scvi-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
