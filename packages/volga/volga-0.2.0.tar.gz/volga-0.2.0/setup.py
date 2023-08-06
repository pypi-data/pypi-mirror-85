# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volga']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'volga',
    'version': '0.2.0',
    'description': 'A python framework for deserialization',
    'long_description': '# volga: flexible object deserialization\n\n[![Build Status]][build] [![Azure DevOps coverage]][Azure coverage url] [![license]][license-file] [![release]][releases] [![python-version]][pypi]\n[![Docs](https://img.shields.io/readthedocs/volga.svg)](https://volga.readthedocs.io)\n\n[Build Status]: https://dev.azure.com/yefrigaitan/volga/_apis/build/status/yefrig.volga?branchName=main\n[build]: https://dev.azure.com/yefrigaitan/volga/_build/latest?definitionId=9&branchName=main\n\n[Azure DevOps coverage]: https://img.shields.io/azure-devops/coverage/yefrigaitan/volga/9\n[Azure coverage url]: https://dev.azure.com/yefrigaitan/volga/_build/latest?definitionId=9&branchName=main\n\n[license]: https://img.shields.io/github/license/yefrig/volga\n[license-file]: https://github.com/yefrig/volga/blob/main/LICENSE\n\n[release]: https://img.shields.io/github/v/release/yefrig/volga?include_prereleases&sort=semver\n[releases]: https://github.com/yefrig/volga/releases\n\n[python-version]: https://img.shields.io/pypi/pyversions/volga\n[pypi]: https://pypi.org/project/volga/\n\n## What is it?\n**volga** provides fast, extensible, and expressive APIs\nto deserialize any python data structure from any supported data format\n(such as JSON and *eventually* YAML and more). Volga allows full customization of the deserialization \nbehavior of your data structures resulting in schema-tized, validated, type-checked \nobjects.\n\n```python3\nimport volga\n\n# Define your model\nclass User(volga.Schema):\n    name: volga.fields.Str\n    age: volga.fields.Int\n    verified: volga.fields.Bool\n  \njson_data = \'{"name":"bob","age":20,"verified":true}\'\n\nbob = volga.json.deserialize(json_data, User)\n\nassert isinstance(bob, User)\n\nprint(bob) # prints object User(name=\'bob\', age=20, verified=True)\n```\n\n## Main Features\n\n\n## Documentation\n\nFull documentation will soon be available on https://volga.readthedocs.io/en/latest/\n\n\n## Where to get it\nThe source code is currently hosted on GitHub at:\nhttps://github.com/yefrig/volga\n\nBinary installers for the latest released version are available at the [Python\npackage index](https://pypi.org/project/volga).\n\n```sh\npip install volga\n```\n\n## Main Contributors\n\n- Yefri Gaitan [@yefrig](https://github.com/yefrig)\n\n- Ecenaz (Jen) Ozmen [@eozmen410](https://github.com/eozmen410)\n',
    'author': 'Yefri Gaitan',
    'author_email': 'yefrigaitan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yefrig/volga',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
