# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strictdoc',
 'strictdoc.backend',
 'strictdoc.backend.dsl',
 'strictdoc.backend.dsl.models',
 'strictdoc.cli',
 'strictdoc.core',
 'strictdoc.core.actions',
 'strictdoc.export.html.generators',
 'strictdoc.export.html.renderers',
 'strictdoc.export.rst',
 'strictdoc.helpers']

package_data = \
{'': ['*'],
 'strictdoc': ['export/html/static/*',
               'export/html/templates/_shared/*',
               'export/html/templates/document_tree/*',
               'export/html/templates/single_document/*',
               'export/html/templates/single_document_table/*',
               'export/html/templates/single_document_traceability/*',
               'export/html/templates/single_document_traceability_deep/*']}

install_requires = \
['docutils==0.16', 'jinja2==2.11.2', 'textx==2.2.0']

entry_points = \
{'console_scripts': ['strictdoc = strictdoc.cli.main:main']}

setup_kwargs = {
    'name': 'strictdoc',
    'version': '0.0.2',
    'description': ' Software for writing technical requirements and specifications.',
    'long_description': '# StrictDoc\n\n![](https://github.com/stanislaw/strictdoc/workflows/StrictDoc%20on%20macOS/badge.svg)\n![](https://github.com/stanislaw/strictdoc/workflows/StrictDoc%20on%20Linux/badge.svg)\n![](https://github.com/stanislaw/strictdoc/workflows/StrictDoc%20on%20Windows/badge.svg)\n\nThe project and the repository are under construction.\n',
    'author': 'Stanislav Pankevich',
    'author_email': 's.pankevich@gmail.com',
    'maintainer': 'Stanislav Pankevich',
    'maintainer_email': 's.pankevich@gmail.com',
    'url': 'https://github.com/stanislaw/strictdoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
