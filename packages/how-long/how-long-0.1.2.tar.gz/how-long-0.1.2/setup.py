# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['how_long']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.0,<3.0']

setup_kwargs = {
    'name': 'how-long',
    'version': '0.1.2',
    'description': 'A simple decorator to measure a function excecution time.',
    'long_description': 'how_long\n========\n\nSimple Decorator to measure a function execution time.\n\nExample\n_______\n\n.. code-block:: python\n\n    from how_long import timer\n\n\n    @timer\n    def some_function():\n        return [x for x in range(10_000_000)]\n',
    'author': 'wilfredinni',
    'author_email': 'carlos.w.montecinos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
