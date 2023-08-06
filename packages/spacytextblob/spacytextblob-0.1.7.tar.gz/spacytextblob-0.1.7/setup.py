# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacytextblob']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=2.3.2,<3.0.0', 'textblob>=0.15.3,<0.16.0']

setup_kwargs = {
    'name': 'spacytextblob',
    'version': '0.1.7',
    'description': 'A TextBlob sentiment analysis pipeline compponent for spaCy',
    'long_description': '# spaCyTextBlob\n\nA TextBlob sentiment analysis pipeline compponent for spaCy.\n\n- [Docs](https://spacytextblob.netlify.app/)\n- [GitHub](https://github.com/SamEdwardes/spaCyTextBlob)\n- [PyPi](https://pypi.org/project/spacytextblob/)\n\n## Table of Contents\n\n- [Install](#install)\n- [Quick Start](#quick-start)\n- [API](#api)\n- [Reference and Attribution](#reference-and-attribution)\n\n## Install\n\nInstall spaCyTextBlob from pypi.\n\n```bash\npip install spacytextblob\n```\n\nTextBlob also requires some data to be downloaded before getting started.\n\n```bash\npython -m textblob.download_corpora\n```\n\nspaCy requires that you download a model to get started.\n\n```bash\npython -m spacy download en_core_web_sm\n```\n\n## Quick Start\n\n\n```python\nimport spacy\nfrom spacytextblob.spacytextblob import SpacyTextBlob\n\nnlp = spacy.load(\'en_core_web_sm\')\nspacy_text_blob = SpacyTextBlob()\nnlp.add_pipe(spacy_text_blob)\ntext = "I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy."\ndoc = nlp(text)\nprint(\'Polarity:\', doc._.sentiment.polarity)\n```\n\n    Polarity: -0.125\n    \n\n\n```python\nprint(\'Sujectivity:\', doc._.sentiment.subjectivity)\n```\n\n    Sujectivity: 0.9\n    \n\n\n```python\nprint(\'Assessments:\', doc._.sentiment.assessments)\n```\n\n    Assessments: [([\'really\', \'horrible\'], -1.0, 1.0, None), ([\'worst\', \'!\'], -1.0, 1.0, None), ([\'really\', \'good\'], 0.7, 0.6000000000000001, None), ([\'happy\'], 0.8, 1.0, None)]\n    \n\n## Reference and Attribution\n\n- TextBlob\n    - [https://github.com/sloria/TextBlob](https://github.com/sloria/TextBlob)\n    - [https://textblob.readthedocs.io/en/latest/](https://textblob.readthedocs.io/en/latest/)\n- negspaCy (for inpiration in writing pipeline and organizing repo)\n    - [https://github.com/jenojp/negspacy](https://github.com/jenojp/negspacy)\n- spaCy custom components\n    - [https://spacy.io/usage/processing-pipelines#custom-components](https://spacy.io/usage/processing-pipelines#custom-components)\n',
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/spaCyTextBlob',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
