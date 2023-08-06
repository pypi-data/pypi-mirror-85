# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['btf_extractor']

package_data = \
{'': ['*'], 'btf_extractor': ['c_ext/*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0', 'numpy>=1.19.3,<2.0.0']

setup_kwargs = {
    'name': 'btf-extractor',
    'version': '0.1.5b2',
    'description': 'Extract various BTF archive format.',
    'long_description': '# BTF Extractor\nExtract various BTF archive format.\n\n## Tested on\n- [ ] Windows MSVC\n- [ ] Windows MinGW(GCC with Scoop)\n- [x] MacOS Homemrew GCC 10.2.0 (x86_64-apple-darwin19)\n- [x] Linux\n',
    'author': '2-propanol',
    'author_email': 'nuclear.fusion.247@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2-propanol/btf_extractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
