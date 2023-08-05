# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sinagot', 'sinagot.models', 'sinagot.plugins', 'sinagot.plugins.models']

package_data = \
{'': ['*']}

install_requires = \
['concurrent-log-handler>=0.9.17,<0.10.0',
 'json-lines>=0.5.0,<0.6.0',
 'json-log-formatter>=0.3.0,<0.4.0',
 'pandas>=1.0.2,<2.0.0',
 'toml>=0.10.0,<0.11.0',
 'ujson>=3.2.0,<4.0.0']

extras_require = \
{'dask': ['dask>=2.12.0,<3.0.0', 'distributed>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'sinagot',
    'version': '0.2.9',
    'description': 'Python library to batch scripts on a file-system workspace.',
    'long_description': '# Sinagot\n\nSinagot is a Python library to batch multiple **scripts** on a file-system **dataset** with a simple API.\nParallelization of data processing is made possible by [Dask.distributed](https://distributed.dask.org/en/latest/). \n\n## Installation\n\nSinagot is available on PyPi:\n\n```bash\npip install sinagot\n```\n\n## Full Documentation\n\n<https://sinagot.readthedocs.io>\n\n## Concept\n\nSinagot main class is build around the `sinagot.Workspace` class. To create an instance, you must provide 3 pathes to :\n\n- A configuration file in `.toml` format.\n- A data folder.\n- A scripts fodler.\n\n<img src="https://github.com/YannBeauxis/sinagot/raw/master/docs/workspace_structure.png" width="200">\n\nDataset is structured as a collection of **records**. A record is identified by an unique ID but many files can be generated for a single record. Those files are processed with **scripts** which generate other files as results.\n\n## Basic example \n\n### Harbor workspace\n\nYou can find in "example" folder of the git the [harbor](https://github.com/YannBeauxis/sinagot/tree/master/example/harbor) workspace that has a record per day of a harbor occupancy. In this example, a record is created each day to count the boats that occupy the harbor. The record ID include a timestamp for the day of recording.\n\nIn Unix environment, you can that type this to get the workspace :\n\n```bash\nwget -qO- https://github.com/YannBeauxis/sinagot/raw/master/example/harbor.tar.gz | tar xvz\n```\n\nTo create the workspace instance :\n\n```python\n>>> from sinagot import Workspace\n>>> ws = Workspace(\'/path/to/harbor/workspace/folder\')\n>>> ws\n<Workspace instance>\n```\n\n### Explore records\n\nYou can list all records ids:\n\n```python\n>>> list(ws.records.iter_ids())\n[\'REC-20200602\', \'REC-20200603\', \'REC-20200601\']\n```\n\nCreate a `Record` instance. For a specific record:\n\n```python\n>>> ws.records.get(\'REC-20200603\')\n<Record instance | id: REC-20200603>\n```\n\nOr the first record found:\n\n```python\n>>> ws.records.first()\n<Record instance | id: REC-20200602>\n```\n\n> Records are not sort by their ids.\n\n### run scripts\n\nYou can run all scripts for each record of the dataset:\n\n```python\n>>> ws.steps.run()\nREC-20200602 | 2020-08-20 11:19:11,530 |\xa0count : Init run\nREC-20200602 | 2020-08-20 11:19:11,531 |\xa0count : Processing run\nREC-20200602 | 2020-08-20 11:19:11,556 |\xa0count : Run finished\n...\nREC-20200601 | 2020-08-20 11:19:11,625 |\xa0mean : Init run\nREC-20200601 | 2020-08-20 11:19:11,626 |\xa0mean : Processing run\nREC-20200601 | 2020-08-20 11:19:11,634 |\xa0mean : Run finished\n\n```\n\nOr for a single record:\n\n```python\n>>> ws.records.get(\'REC-20200603\').steps.run()\nREC-20200603 | 2020-08-20 11:28:32,588 |\xa0count : Init run\nREC-20200603 | 2020-08-20 11:28:32,590 |\xa0count : Processing run\nREC-20200603 | 2020-08-20 11:28:32,616 |\xa0count : Run finished\nREC-20200603 | 2020-08-20 11:28:32,619 |\xa0mean : Init run\nREC-20200603 | 2020-08-20 11:28:32,621 |\xa0mean : Processing run\nREC-20200603 | 2020-08-20 11:28:32,637 |\xa0mean : Run finished\n```\n\n## More complex dataset\n\nYou can handle more complexity of dataset structure with **task** and **modality** concepts. During a recording session for a single record, data can be generate for differents task and each task can generate different kind of data called **modality**. \n\n### SoNeTAA usecase\n\nThe idea of Sinagot emerged for the data management of an EEG platform called SoNeTAA :\nhttps://research.pasteur.fr/en/project/sonetaa/ .\n\nFor documentation purpose SoNeTAA workspace structure will be used as example. \n\nOn SoNeTAA, a record with an ID with timestamp info in this format `REC-[YYMMDD]-[A-Z]`, \nfor example `"REC-200331-A"`. \n\nFor a record, 3 tasks are performed: \n\n* "RS" for Resting State\n* "MMN" for MisMatch Negativity\n* "HDC" for Human Dynamic Clamp.\n\n3 modalities handle data depending of the tasks\n* For each tasks, "EEG" modality create data from ElectroEncephalogram .\n* A "behavior" modality create date only for HDC task.\n* A "clinical" modality handle data used for every task.\n\n### Explore by task or modality\n\nEach record collection or single record has **subscopes** corresponding to their tasks and modalities accessible as attribute.\n\nFor example to select only the task RS of the dataset:\n\n```python\n>>> ws.RS\n<RecordCollection instance | task: RS, modality: None>\n```\n\n> A dataset subscope is a **RecordCollection**.\n\nOr the EEG modality of a record:\n\n```python\n>>> rec.EEG\n<Record instance | id: REC-200331-A, task: None, modality: EEG>\n```\n\nYou can select a specific couple of task and modality (called **unit**):\n\n```python\n>>> ws.RS.EEG\n<RecordCollection instance | task: RS, modality: EEG>\n>>> ws.EEG.RS\n<RecordCollection instance | task: RS, modality: EEG>\n```\n',
    'author': 'Yann Beauxis',
    'author_email': 'dev@yannbeauxis.net',
    'maintainer': 'Yann Beauxis',
    'maintainer_email': 'dev@yannbeauxis.net',
    'url': 'https://github.com/YannBeauxis/sinagot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
