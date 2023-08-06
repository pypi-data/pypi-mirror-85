# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flayyer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flayyer',
    'version': '1.0.0',
    'description': 'FLAYYER.com helper classes and methods',
    'long_description': '# flayyer-python\n![PyPI - Version](https://img.shields.io/pypi/v/flayyer)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/flayyer)\n\nThis module is agnostic to any Python framework and has zero external dependencies.\n\nTo create a FLAYYER template please refer to: [flayyer.com](https://flayyer.com?ref=flayyer-python)\n\n## Installation\n\nInstall it with [Poetry](https://python-poetry.org/), the modern package manager.\n\n```sh\npoetry add flayyer\n```\n\nDon’t worry: if poetry is not your thing, you can also use [pip](https://pip.pypa.io/en/stable/).\n\n```sh\npip install flayyer\n```\n\n**Note:** This client requires [**Python 3.6+**](https://docs.python.org/3/whatsnew/3.6.html).\n\n## Usage\n\nAfter installing the package you can format URL as:\n\n```python\nfrom flayyer import Flayyer\n\nflayyer = Flayyer(\n    tenant="tenant",\n    deck="deck",\n    template="template",\n    variables={"title": "Hello world!"},\n)\n\n# Use this image in your <head/> tags\nurl = flayyer.href()\n# > https://flayyer.io/v2/tenant/deck/template.jpeg?__v=1596906866&title=Hello+world%21\n```\n\nVariables can be complex arrays and hashes.\n\n```python\nflayyer = Flayyer(\n    tenant="tenant",\n    deck="deck",\n    template="template",\n    variables={\n        "items": [\n            { "text": "Oranges", "count": 12 },\n            { "text": "Apples", "count": 14 },\n        ],\n    },\n)\n```\n\n**IMPORTANT: variables must be serializable.**\n\nTo decode the URL for debugging purposes:\n\n```python\nfrom urllib.parse import unquote\n\nprint(unquote(url))\n# > https://flayyer.io/v2/tenant/deck/template.jpeg?title=Hello+world!&__v=123\n```\n\n## Development\n\nPrepare the local environment:\n\n```sh\npoetry install\n```\n\n```sh\npoetry shell\n```\n\nRun tests with pytest:\n\n```sh\npytest\n```\n\nDeploy with:\n\n```sh\n# Set API Token\npoetry config pypi-token.pypi pypi-TOKEN\n\npoetry version X.Y.Z\npoetry build\npoetry publish\n```\n\n## Contributing\n\nBug reports and pull requests are welcome on GitHub at https://github.com/flayyer/flayyer-python.\n\n## License\n\nThe module is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).\n\n## Acknowledgements\n\nHeads up to [**@nebil**](https://github.com/nebil) for his advice in the development of this Python module.\n',
    'author': 'Patricio López Juri',
    'author_email': 'patricio@flayyer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://flayyer.com/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
