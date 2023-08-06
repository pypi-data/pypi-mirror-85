# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snappiershot', 'snappiershot.plugins', 'snappiershot.serializers']

package_data = \
{'': ['*']}

install_requires = \
['pprint_ordered_sets>=1.0.0,<2.0.0', 'tomlkit>=0.7.0,<0.8.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>1.5.1']}

entry_points = \
{'pytest11': ['snappiershot = snappiershot.plugins.pytest']}

setup_kwargs = {
    'name': 'snappiershot',
    'version': '0.2.0',
    'description': 'Snapshot testing library.',
    'long_description': '# SnappierShot\nAdd snapshot testing to your testing toolkit.\n\n## Installation\n```bash\n$ pip install snappiershot\n```\n\n## Configuration\nSnappier shot is following the [trend of packages](https://github.com/carlosperate/awesome-pyproject/)\nin performing project-wide configuration through the pyproject.toml file established by\n[PEP 518](https://www.python.org/dev/peps/pep-0518/).\n\nWithin the pyproject.toml file, all snappiershot configuration can be found under the\n`[tool.snappiershot]` heading.\n\n### Example (with default values):\n```toml\n[tool.snappiershot]\nfile_format = "json"\nfloat_absolute_tolerance = 1e-6\nfloat_relative_tolerance = 0.001\nfull_diff = false\njson_indentation = 4\n```\n\n\n## Usage\n\nSnappierShot allows you to take a "snapshot" of data the first time that a test\n  is run, and stores it nearby in a `.snapshots` directory. Then, for all\n  subsequent times that test is run, the data is assert to "match" the original\n  data.\n\n### Pytest Example\n```python\ndef test_something(snapshot):\n    """ Test that something works as expected"""\n    # Arrange\n    x = 1\n    y = 2\n\n    # Act\n    result = x + y\n\n    # Assert\n    snapshot.assert_match(result)\n```\n\n#### No Test Runner Example\n```python\nfrom snappiershot import Snapshot\n\ndef test_something():\n    """ Test that something works as expected"""\n    # Arrange\n    x = 1\n    y = 2\n\n    # Act\n    result = x + y\n\n    # Assert\n    with Snapshot() as snapshot\n        snapshot.assert_match(result)\n\ntest_something()\n```\n\n### Support Types:\n  * Primitives (`bool`, `int`, `float`, `None`, `str`)\n  * Numerics (`complex`)\n  * Collections (`lists`, `tuples`, `sets`)\n  * Dictionaries\n  * Classes (with an underlying `__dict__`)\n  * Classes with custom encoding (by defining a `__snapshot__` method).\n\n## Contributing\nSee [CONTRIBUTING.md](CONTRIBUTING.md)\n',
    'author': 'Ben Bonenfant',
    'author_email': 'bonenfan5ben@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MORSECorp/snappiershot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
