# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nb_clean']

package_data = \
{'': ['*']}

install_requires = \
['nbformat>=5.0.5']

entry_points = \
{'console_scripts': ['nb-clean = nb_clean.cli:main']}

setup_kwargs = {
    'name': 'nb-clean',
    'version': '2.0.2',
    'description': 'Clean Jupyter notebooks for versioning',
    'long_description': "# nb-clean\n\n`nb-clean` cleans Jupyter notebooks of cell execution counts, metadata, outputs,\nand (optionally) empty cells, preparing them for committing to version control.\nIt provides a Git filter to automatically clean notebooks before they're staged,\nand can also be used with other version control systems, as a command line tool,\nand as a Python library. It can determine if a notebook is clean or not, which\ncan be used as a check in your continuous integration pipelines.\n\n:warning: _`nb-clean` 2.0.0 introduced a new command line interface to make\ncleaning notebooks in place easier. If you upgrade from a previous release,\nyou'll need to migrate to the new interface as described under\n[Migrating to `nb-clean` 2](#migrating-to-nb-clean-2)._\n\n## Installation\n\nTo install the latest release from [PyPI], use [pip]:\n\n```bash\npython3 -m pip install nb-clean\n```\n\nAlternately, in Python projects using [Poetry] or [Pipenv] for dependency\nmanagement, add `nb-clean` as a development dependency with\n`poetry add --dev nb-clean` or `pipenv install --dev nb-clean`. `nb-clean`\nrequires Python 3.6 or later.\n\n## Usage\n\n### Cleaning\n\nTo add a filter to an existing Git repository to automatically clean notebooks\nwhen they're staged, run the following from the working tree:\n\n```bash\nnb-clean add-filter\n```\n\nThis will configure a filter to remove cell execution counts, metadata, and\noutputs. To also remove empty cells, use:\n\n```bash\nnb-clean add-filter --remove-empty-cells\n```\n\nTo preserve cell metadata, such as that required by tools such as [papermill],\nuse:\n\n```bash\nnb-clean add-filter --preserve-cell-metadata\n```\n\n`nb-clean` will configure a filter in the Git repository in which it is run, and\nwon't mutate your global or system Git configuration. To remove the filter, run:\n\n```bash\nnb-clean remove-filter\n```\n\nAside from usage from a filter in a Git repository, you can also clean up a\nJupyter notebook with:\n\n```bash\nnb-clean clean notebook.ipynb\n```\n\nThis cleans the notebook in place. You can also pass the notebook content on\nstandard input, in which case the cleaned notebook is written to standard\noutput:\n\n```bash\nnb-clean clean < original.ipynb > cleaned.ipynb\n```\n\nTo also remove empty cells, add the `-e`/`--remove-empty-cells` flag. To\npreserve cell metadata, add the `-m`/`--preserve-cell-metadata` flag.\n\n### Checking\n\nYou can check if a notebook is clean with:\n\n```bash\nnb-clean check notebook.ipynb\n```\n\nor by passing the notebook contents on standard input:\n\n```bash\nnb-clean check < notebook.ipynb\n```\n\nTo also check for empty cells, add the `-e`/`--remove-empty-cells` flag. To\nignore cell metadata, add the `-m`/`--preserve-cell-metadata` flag.\n\n`nb-clean` will exit with status code 0 if the notebook is clean, and status\ncode 1 if it is not. `nb-clean` will also print details of cell execution\ncounts, metadata, outputs, and empty cells it finds.\n\n### Migrating to `nb-clean` 2\n\nThe following table maps from the command line interface of `nb-clean` 1.6.0 to\nthat of `nb-clean` 2.0.0.\n\n| Description                             | `nb-clean` 1.6.0                                                    | `nb-clean` 2.0.0                                            |\n| --------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------- |\n| Clean notebook                          | `nb-clean clean -i/--input notebook.ipynb \\| sponge notebook.ipynb` | `nb-clean clean notebook.ipynb`                             |\n| Clean notebook (remove empty cells)     | `nb-clean clean -i/--input notebook.ipynb -e/--remove-empty`        | `nb-clean clean -e/--remove-empty-cells notebook.ipynb`     |\n| Clean notebook (preserve cell metadata) | `nb-clean clean -i/--input notebook.ipynb -m/--preserve-metadata`   | `nb-clean clean -m/--preserve-cell-metadata notebook.ipynb` |\n| Check notebook                          | `nb-clean check -i/--input notebook.ipynb`                          | `nb-clean check notebook.ipynb`                             |\n| Check notebook (remove empty cells)     | `nb-clean check -i/--input notebook.ipynb -e/--remove-empty`        | `nb-clean check -e/--remove-empty-cells notebook.ipynb`     |\n| Check notebook (preserve cell metadata) | `nb-clean check -i/--input notebook.ipynb -m/--preserve-metadata`   | `nb-clean check -m/--preserve-cell-metadata notebook.ipynb` |\n| Add Git filter to clean notebooks       | `nb-clean configure-git`                                            | `nb-clean add-filter`                                       |\n| Remove Git filter                       | `nb-clean unconfigure-git`                                          | `nb-clean remove-filter`                                    |\n\n## Copyright\n\nCopyright © 2017-2020 [Scott Stevenson].\n\n`nb-clean` is distributed under the terms of the [ISC licence].\n\n[isc licence]: https://opensource.org/licenses/ISC\n[papermill]: https://papermill.readthedocs.io/\n[pip]: https://pip.pypa.io/\n[pipenv]: https://pipenv.readthedocs.io/\n[poetry]: https://python-poetry.org/\n[pypi]: https://pypi.org/project/nb-clean/\n[scott stevenson]: https://scott.stevenson.io\n",
    'author': 'Scott Stevenson',
    'author_email': 'scott@stevenson.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/srstevenson/nb-clean',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
