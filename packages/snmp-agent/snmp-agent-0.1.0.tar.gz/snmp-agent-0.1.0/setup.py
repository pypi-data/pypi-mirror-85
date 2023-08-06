# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['snmp_agent']

package_data = \
{'': ['*']}

install_requires = \
['asn1>=2.4.1,<3.0.0']

setup_kwargs = {
    'name': 'snmp-agent',
    'version': '0.1.0',
    'description': 'SNMP Server',
    'long_description': '# snmp-agent\nSNMP Server\n\n\n# Requirements\n- Python >= 3.8\n- asn1\n\n\n# License\nMIT\n',
    'author': 'kthrdei',
    'author_email': 'kthrd.tech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kthrdei/snmp-agent',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
