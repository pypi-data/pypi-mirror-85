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
    'version': '0.1.1',
    'description': 'A TextBlob sentiment analysis pipeline compponent for spaCy.',
    'long_description': '# spaCyTextBlob\n\nA TextBlob sentiment analysis pipeline compponent for spaCy.\n\n## Table of Contents\n\n- [Install](#install)\n- [Usage](#usage)\n    - [How to load the package in spaCy pipeline](#how-to-load-the-package-in-spaCy-pipeline)\n    - [How to use the pipeline](#how-to-use-the-pipeline)\n- [API](#api)\n- [Reference and Attribution](#reference-and-attribution)\n\n## Install\n\nInstall spaCyTextBlob from pypi.\n\n```bash\npip install spacytextblob\n```\n\nTextBlob also requires some data to be downloaded before getting started.\n\n```bash\npython -m textblob.download_corpora\n```\n\n## Usage\n\n### How to load the package in spaCy pipeline\n\n\n```python\nimport spacy\nfrom spacytextblob.textblob import SpacyTextBlob\n\nnlp = spacy.load(\'en_core_web_sm\')\nspacy_text_blob = SpacyTextBlob()\nnlp.add_pipe(spacy_text_blob)\n\n# pipeline contains component name\nprint(nlp.pipe_names) \n\n```\n\n    [\'tagger\', \'parser\', \'ner\', \'spaCyTextBlob\']\n    \n\n### How to use the pipeline\n\nBy adding `SpacyTextBlob` into the pipeline sentiment analysis is perofmed on the doc everytime you call `nlp`.\n\n\n```python\ntext = "I had a really horrible day. It was the worst day ever!"\ndoc = nlp(text)\nprint(\'Polarity:\', doc._.polarity)\nprint(\'Sujectivity:\', doc._.subjectivity)\nprint(\'Assessments:\', doc._.assessments)\n```\n\n    Polarity: -1.0\n    Sujectivity: 1.0\n    Assessments: [([\'really\', \'horrible\'], -1.0, 1.0, None), ([\'worst\', \'!\'], -1.0, 1.0, None)]\n    \n\n\n```python\ntext = "Wow I had just the best day ever today!"\ndoc = nlp(text)\nprint(\'Polarity:\', doc._.polarity)\nprint(\'Sujectivity:\', doc._.subjectivity)\nprint(\'Assessments:\', doc._.assessments)\n```\n\n    Polarity: 0.55\n    Sujectivity: 0.65\n    Assessments: [([\'wow\'], 0.1, 1.0, None), ([\'best\', \'!\'], 1.0, 0.3, None)]\n    \n\n## API\n\nTo make the usage simpler spacy provides custom extensions which a library can use. This makes it easier for the user to get the desired data. The below tables summaries the extensions.\n\n### `spacy.Doc` extensions\n\n\n| Extension | Type | Description | Default |\n|-----------|------|-------------|---------|\n| doc._.polarity | `Float` | The polarity of the document. The polarity score is a float within the range [-1.0, 1.0]. | `None` |\n| doc._.sujectivity | `Float` | The subjectivity of the document. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective. | `None` |\n| doc._.assessments | `tuple` | Return a tuple of form (polarity, subjectivity, assessments ) where polarity is a float within the range [-1.0, 1.0], subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective, and assessments is a list of polarity and subjectivity scores for the assessed tokens. | `None` |\n\n\n\n\n## Reference and Attribution\n\n- TextBlob\n    - [https://github.com/sloria/TextBlob](https://github.com/sloria/TextBlob)\n    - [https://textblob.readthedocs.io/en/latest/](https://textblob.readthedocs.io/en/latest/)\n- negspaCy (for inpiration in writing pipeline and organizing repo)\n    - [https://github.com/jenojp/negspacy](https://github.com/jenojp/negspacy)\n- spaCy custom components\n    - [https://spacy.io/usage/processing-pipelines#custom-components](https://spacy.io/usage/processing-pipelines#custom-components)\n',
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/spaCyTextBlob',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
