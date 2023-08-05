# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genni', 'genni.griding', 'genni.nets']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0',
 'ray[tune]>=1.0.0,<2.0.0',
 'tensorboard>=2.3.0,<3.0.0',
 'torch>=1.7.0,<2.0.0',
 'torchvision>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'genni',
    'version': '0.1.0',
    'description': 'GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability',
    'long_description': '# GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability\n\n## Disclaimer\n\nThis is code associated with the paper "GENNI: Visualising the Geometry of\nEquivalences for Neural Network Identifiability," published in the\n[NeurIPS](https://nips.cc/) Workshop on [Differential Geometry meets Deep\nLearning 2020](https://sites.google.com/view/diffgeo4dl/).\n\n## Preliminaries\n\nOur package is designed to run in Python 3.6 and pip version 20.2.4....\n\n```\npip install -r requirements.txt\n```\n\n## Usage\n\nTo use our package...\n\n```\n>>> from GENNI import genni_vis\n>>> plot = genni_vis(mesh, V, X, Y, eigenpairs)\n>>> plot.optimize()\n```\n\n```\npython demo_dragon.py --help\nusage: demo_dragon.py [-h] [--num-eigenpairs NUM_EIGENPAIRS] [--seed SEED]\n                      [--output-dir OUTPUT_DIR]\n                      [--eigenpairs-file EIGENPAIRS_FILE] [--mayavi]\n                      [--num-samples NUM_SAMPLES]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --num-eigenpairs NUM_EIGENPAIRS\n                        Number of eigenpairs to use. Default is 500\n  --seed SEED           Random seed\n  --output-dir OUTPUT_DIR\n                        Output directory to save .pvd files to. Default is\n                        ./output\n  --eigenpairs-file EIGENPAIRS_FILE\n                        .npy file with precomputed eigenpairs\n  --mayavi              Render results to .png with Mayavi\n  --num-samples NUM_SAMPLES\n                        Number of random samples to generate\n```\n\nHow saving is done:\n\nResults are expected to saved in specific locations. If this code is not used to create equivalences classes, but the plotting functions want to be used, we advise to follow the structure laied out in get_grid.py and simply use the methods in interpolation.py which are agnostic to the saved locations.\n\n### Run experiment.py to produce elements in equivalence classes\n\n### To check if the elements converged to elements in the equivalence class, run stats_plotting.\n\n### Run the griding code to produce a set of elements in a subspace spanned by elements that were found.\n\n### Subset the set by elements wiht loss less than some epsilon and choose appropriate plotting mechanism.\n\n## Reproducing the paper\n\n- [ ] How to reproduce figures\n- [ ] How to reproduce values\n\n## Citing\n\nIf you use GENNI anywhere in your work, please cite use using\n\n```\n@article{2020,\n    title={GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability},\n    author={},\n    booktitle={},\n    year={2020}\n}\n```\n\n## TODO LIST\n\n- [x] Licence (MIT)\n- [ ] Documentation\n- [ ] Github actions\n  - Contributing\n  - Pull request / Issues templates\n- [ ] Put on PyPI\n- [ ] Make environment?\n- [ ] CI\n- [ ] Make package conform to PEP and packaging standards\n',
    'author': 'Arinbjörn Kolbeinsson',
    'author_email': None,
    'maintainer': 'Isak Falk',
    'maintainer_email': 'ucabitf@ucl.ac.uk',
    'url': 'https://github.com/Do-Not-Circulate/GENNI_public',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
