# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['npvcc2016',
 'npvcc2016.PyTorch',
 'npvcc2016.PyTorch.Lightning',
 'npvcc2016.PyTorch.Lightning.datamodule',
 'npvcc2016.PyTorch.dataset']

package_data = \
{'': ['*']}

install_requires = \
['pytorch-lightning>=1.0.6,<2.0.0', 'torch', 'torchaudio>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'npvcc2016',
    'version': '1.2.2',
    'description': 'npvcc2016: Python loader of npVCC2016 speech corpus',
    'long_description': '# npvcc2016 - Python loader of npVCC2016Corpus\n[![PyPI version](https://badge.fury.io/py/npvcc2016.svg)](https://badge.fury.io/py/npVCC2016)\n![Python Versions](https://img.shields.io/pypi/pyversions/npvcc2016.svg)  \n\n`npvcc2016` is a Python package for loader of [npVCC2016 non-parallel speech corpus](https://github.com/tarepan/npVCC2016Corpus).  \nFor machine learning, corpus/dataset is indispensable - but troublesome - part.  \nWe need portable & flexible loader for streamline development.  \n`npvcc2016` is the one!!  \n\n## Demo\n\nPython/PyTorch  \n\n```bash\npip install npvcc2016\n```\n\n```python\nfrom npvcc2016.PyTorch.dataset.waveform import NpVCC2016\n\ndataset = NpVCC2016(".", train=True, download=True)\n\nfor datum in dataset:\n    print("Yeah, data is acquired with only two line of code!!")\n    print(datum) # (datum, label) tuple provided\n``` \n\n`npvcc2016` transparently downloads corpus, structures the data and provides standarized datasets.  \nWhat you have to do is only instantiating the class!  \n\n## APIs\nCurrent `npvcc2016` support PyTorch.  \nAs interface, PyTorch\'s `Dataset` and PyTorch-Lightning\'s `DataModule` are provided.  \nnpVCC2016 corpus is speech corpus, so we provide `waveform` dataset and `spectrogram` dataset for both interfaces.  \n\n- PyTorch\n  - (pure PyTorch) dataset\n    - waveform: `NpVCC2016`\n    - spectrogram: `NpVCC2016_spec`\n  - PyTorch-Lightning\n    - waveform: `NpVCC2016DataModule`\n    - spectrogram: `NpVCC2016_spec_DataModule`\n\n### Extendibility\n`waveform` dataset has easy-to-extend structure.  \nBy overiding hook functions, you can customize preprocessing for your machine-learning tasks.  \nPlease check `dataset`-`waveform` file.  \n\n## Dependency Notes\n### PyTorch version\nPyTorch version: PyTorch v1.6 is working (We checked with v1.6.0).  \n\nFor dependency resolution, we do **NOT** explicitly specify the compatible versions.  \nPyTorch have several distributions for various environment (e.g. compatible CUDA version.)  \nUnfortunately it make dependency version management complicated for dependency management system.  \nIn our case, the system `poetry` cannot handle cuda variant string (e.g. `torch>=1.6.0` cannot accept `1.6.0+cu101`.)  \nIn order to resolve this problem, we use `torch==*`, it is equal to no version specification.  \n`Setup.py` could resolve this problem (e.g. `torchaudio`\'s `setup.py`), but we will not bet our effort to this hacky method.  \n',
    'author': 'Tarepan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tarepan/npVCC2016',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
