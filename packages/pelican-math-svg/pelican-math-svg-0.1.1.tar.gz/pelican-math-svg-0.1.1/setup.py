# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.math_svg']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-math-svg',
    'version': '0.1.1',
    'description': 'Render math expressions to svg and embed them.',
    'long_description': '# math-svg: A Plugin for Pelican\n\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-math-svg)](https://pypi.org/project/pelican-math-svg/) ![License](https://img.shields.io/pypi/l/pelican-math-svg?color=blue)\n\nRender math expressions to svg and embed them.\n\n## Installation\n\nThis plugin can be installed via:\n```shell\npython -m pip install pelican-math-svg\n```\n\n## Roadmap\n\n- [x] inline math\n- [ ] block math\n- [x] automatic deployment\n- [ ] unit tests\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/f-koehler/pelican-math-svg/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\n## License\n\nThis project is licensed under the GPLv3 license.\n',
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/f-koehler/pelican-math-svg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
