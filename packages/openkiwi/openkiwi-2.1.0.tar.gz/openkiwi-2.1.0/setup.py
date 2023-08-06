# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiwi',
 'kiwi.assets',
 'kiwi.assets.config',
 'kiwi.data',
 'kiwi.data.datasets',
 'kiwi.data.encoders',
 'kiwi.lib',
 'kiwi.metrics',
 'kiwi.modules',
 'kiwi.modules.common',
 'kiwi.systems',
 'kiwi.systems.decoders',
 'kiwi.systems.encoders',
 'kiwi.systems.outputs',
 'kiwi.training',
 'kiwi.utils']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'hydra-core>=0.11.3,<0.12.0',
 'more-itertools>=8.0.0,<9.0.0',
 'numpy>=1.18,<2.0',
 'omegaconf>=1.4.1,<2.0.0',
 'pydantic>=1.5,<2.0',
 'pytorch-lightning>=0.8.4,<0.9.0',
 'pytorch-nlp>=0.5.0,<0.6.0',
 'pyyaml>=5.1.2,<6.0.0',
 'scipy>=1.2,<2.0',
 'torch>=1.4.0,<1.7.0',
 'tqdm>=4.29,<5.0',
 'transformers>=3.0.2,<4.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{'mlflow': ['mlflow[mlflow]>=1.11.0,<2.0.0'],
 'search': ['optuna[search]>=2.2.0,<3.0.0',
            'plotly[search]>=4.11.0,<5.0.0',
            'sklearn[search]>=0.0,<0.1']}

entry_points = \
{'console_scripts': ['kiwi = kiwi.__main__:main']}

setup_kwargs = {
    'name': 'openkiwi',
    'version': '2.1.0',
    'description': 'Machine Translation Quality Estimation Toolkit',
    'long_description': "![OpenKiwi Logo](https://github.com/Unbabel/OpenKiwi/blob/master/docs/_static/img/openkiwi-logo-horizontal.svg)\n\n--------------------------------------------------------------------------------\n\n[![PyPI version](https://img.shields.io/pypi/v/openkiwi?color=%236ecfbd&label=pypi%20package&style=flat-square)](https://pypi.org/project/openkiwi/)\n[![python versions](https://img.shields.io/pypi/pyversions/openkiwi.svg?style=flat-square)](https://pypi.org/project/openkiwi/)\n[![CircleCI](https://img.shields.io/circleci/build/github/Unbabel/OpenKiwi/master?style=flat-square)](https://circleci.com/gh/Unbabel/OpenKiwi/tree/master)\n[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/Unbabel/OpenKiwi?style=flat-square)](https://codeclimate.com/github/Unbabel/OpenKiwi/test_coverage)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)\n[![GitHub last commit](https://img.shields.io/github/last-commit/unbabel/openkiwi?style=flat-square)](https://github.com/Unbabel/OpenKiwi/commits/master)\n\n**Open-Source Machine Translation Quality Estimation in PyTorch**\n\nQuality estimation (QE) is one of the missing pieces of machine translation: its goal is to evaluate a translation system’s quality without access to reference translations. We present **OpenKiwi**, a Pytorch-based open-source framework that implements the best QE systems from WMT 2015-18 shared tasks, making it easy to experiment with these models under the same framework. Using OpenKiwi and a stacked combination of these models we have achieved state-of-the-art results on word-level QE on the WMT 2018 English-German dataset.\n\n## News\n\n* An experimental demonstration interface called OpenKiwi Tasting has been released on [GitHub](https://github.com/Unbabel/OpenKiwiTasting) and can be checked out in [Streamlit Share](https://share.streamlit.io/unbabel/openkiwitasting/main).\n\n* A new major version (2.0.0) of OpenKiwi has been released. Introducing HuggingFace Transformers support and adoption of Pytorch-lightning.\nFor a condensed view of changed, check the [changelog](CHANGELOG.md)\n\n* Following our nomination in early July, we are happy to announce we won the [Best Demo Paper at ACL 2019](http://www.acl2019.org/EN/winners-of-acl-2019-best-paper-awards.xhtml)! Congratulations to the whole team and huge thanks for supporters and issue reporters.\n\n* Check out the [published paper](https://www.aclweb.org/anthology/P19-3020).\n\n* We have released the OpenKiwi [tutorial](https://github.com/Unbabel/KiwiCutter) we presented at MT Marathon 2019.\n\n## Features\n\n* Framework for training QE models and using pre-trained models for evaluating MT.\n* Supports both word and sentence-level (HTER or z-score) Quality estimation.\n* Implementation of five QE systems in Pytorch: NuQE [[2], [3]], predictor-estimator [[4], [5]], BERT-Estimator [[6]], XLM-Estimator [[6]] and XLMR-Estimator\n*    Older systems only supported in versions <=2.0.0: QUETCH [[1]], APE-QE [[3]] and a stacked ensemble with a linear system [[2], [3]].\n* Easy to use API. Import it as a package in other projects or run from the command line.\n* Easy to track and reproduce experiments via yaml configuration files.\n* Based on Pytorch-Lightning making the code easier to scale, use and keep up-do-date with engineering advances.\n* Implemented using HuggingFace Transformers library to allow easy access to state-of-the-art pre-trained models.\n\n## Quick Installation\n\nTo install OpenKiwi as a package, simply run\n```bash\npip install openkiwi\n```\n\nYou can now\n```python\nimport kiwi\n```\ninside your project or run in the command line\n```bash\nkiwi\n```\n\n**Optionally**, if you'd like to take advantage of our [MLflow](https://mlflow.org/) integration, simply install it in the same virtualenv as OpenKiwi:\n```bash\npip install openkiwi[mlflow]\n```\n\n\n## Getting Started\n\nDetailed usage examples and instructions can be found in the [Full Documentation](https://unbabel.github.io/OpenKiwi/index.html).\n\n\n## Contributing\n\nWe welcome contributions to improve OpenKiwi.\nPlease refer to [CONTRIBUTING.md](https://github.com/Unbabel/OpenKiwi/blob/master/CONTRIBUTING.md) for quick instructions or to [contributing instructions](https://unbabel.github.io/OpenKiwi/contributing.html) for more detailed instructions on how to set up your development environment.\n\n\n## License\n\nOpenKiwi is Affero GPL licensed. You can see the details of this license in [LICENSE](https://github.com/Unbabel/OpenKiwi/blob/master/LICENSE).\n\n\n## Citation\n\nIf you use OpenKiwi, please cite the following paper: [OpenKiwi: An Open Source Framework for Quality Estimation](https://www.aclweb.org/anthology/P19-3020).\n\n```\n@inproceedings{openkiwi,\n    author = {Fábio Kepler and\n              Jonay Trénous and\n              Marcos Treviso and\n              Miguel Vera and\n              André F. T. Martins},\n    title  = {Open{K}iwi: An Open Source Framework for Quality Estimation},\n    year   = {2019},\n    booktitle = {Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics--System Demonstrations},\n    pages  = {117--122},\n    month  = {July},\n    address = {Florence, Italy},\n    url    = {https://www.aclweb.org/anthology/P19-3020},\n    organization = {Association for Computational Linguistics},\n}\n```\n\n\n## References\n\n##### [[1]] [Kreutzer et al. (2015): QUality Estimation from ScraTCH (QUETCH): Deep Learning for Word-level Translation Quality Estimation](http://aclweb.org/anthology/W15-3037)\n[1]:#1-kreutzer-et-al-2015-quality-estimation-from-scratch-quetch-deep-learning-for-word-level-translation-quality-estimation\n\n##### [[2]] [Martins et al. (2016): Unbabel's Participation in the WMT16 Word-Level Translation Quality Estimation Shared Task](http://www.aclweb.org/anthology/W16-2387)\n[2]:#2-martins-et-al-2016-unbabels-participation-in-the-wmt16-word-level-translation-quality-estimation-shared-task\n\n##### [[3]] [Martins et al. (2017): Pushing the Limits of Translation Quality Estimation](http://www.aclweb.org/anthology/Q17-1015)\n[3]:#3-martins-et-al-2017-pushing-the-limits-of-translation-quality-estimation\n\n##### [[4]] [Kim et al. (2017): Predictor-Estimator using Multilevel Task Learning with Stack Propagation for Neural Quality Estimation](http://www.aclweb.org/anthology/W17-4763)\n[4]:#4-kim-et-al-2017-predictor-estimator-using-multilevel-task-learning-with-stack-propagation-for-neural-quality-estimation\n\n##### [[5]] [Wang et al. (2018): Alibaba Submission for WMT18 Quality Estimation Task](http://statmt.org/wmt18/pdf/WMT093.pdf)\n[5]:#5-wang-et-al-2018-alibaba-submission-for-wmt18-quality-estimation-task\n\n##### [[6]] [Kepler et al. (2019): Unbabel’s Participation in the WMT19 Translation Quality Estimation Shared Task](https://www.aclweb.org/anthology/W19-5406.pdf)\n[6]:#6-kepler-et-al-2019-unbabels-participation-in-the-wmt19-translation-quality-estimation-shared-task\n",
    'author': 'AI Research, Unbabel',
    'author_email': 'openkiwi@unbabel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Unbabel/OpenKiwi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
