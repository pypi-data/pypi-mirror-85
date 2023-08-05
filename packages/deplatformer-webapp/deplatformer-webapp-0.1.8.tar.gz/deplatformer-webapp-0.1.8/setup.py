# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deplatformer_webapp',
 'deplatformer_webapp.forms',
 'deplatformer_webapp.helpers',
 'deplatformer_webapp.migrations',
 'deplatformer_webapp.migrations.versions',
 'deplatformer_webapp.models',
 'deplatformer_webapp.services',
 'deplatformer_webapp.views']

package_data = \
{'': ['*'],
 'deplatformer_webapp': ['lib/ipfshttpclient-0.7.0a1-py3-none-any.whl',
                         'static/assets/*',
                         'static/assets/Facebook/*',
                         'static/css/*',
                         'static/fontawesome/css/*',
                         'static/fontawesome/webfonts/*',
                         'static/js/*',
                         'static/sample_data/*',
                         'templates/*',
                         'templates/facebook/*',
                         'templates/filecoin/*',
                         'templates/flask_user/*',
                         'templates/flask_user/emails/*',
                         'templates/google/*',
                         'templates/icloud/*',
                         'templates/instagram/*']}

install_requires = \
['Deprecated==1.2.10',
 'Flask-Login==0.5.0',
 'Flask-Mail==0.9.1',
 'Flask-Migrate>=2.5.3,<3.0.0',
 'Flask-SQLAlchemy==2.4.4',
 'Flask-SocketIO==4.3.1',
 'Flask-User>=1.0.2,<2.0.0',
 'Flask-WTF==0.14.3',
 'Flask==1.1.2',
 'Jinja2==2.11.2',
 'MarkupSafe==1.1.1',
 'SQLAlchemy==1.3.19',
 'WTForms==2.3.3',
 'Werkzeug==1.0.1',
 'bcrypt==3.2.0',
 'blinker==1.4',
 'cffi==1.14.2',
 'click==7.1.2',
 'cryptography==3.1',
 'dnspython==1.16.0',
 'docker>=4.3.1,<5.0.0',
 'email-validator==1.1.1',
 'eventlet==0.27.0',
 'ftfy==5.8',
 'greenlet==0.4.16',
 'grpcio==1.30.0',
 'idna>=2.10,<3.0',
 'itsdangerous==1.1.0',
 'monotonic==1.5',
 'passlib==1.7.2',
 'poetry-version>=0.1.5,<0.2.0',
 'protobuf==3.12.4',
 'pycparser==2.20',
 'pygate-grpc==0.0.11',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-engineio==3.13.2',
 'python-socketio==4.6.0',
 'six==1.15.0',
 'urllib3==1.25.11',
 'wcwidth==0.2.5',
 'wrapt==1.12.1']

entry_points = \
{'console_scripts': ['deplatformer = deplatformer_webapp.cli:cli',
                     'dropdb = deplatformer_webapp.scripts:dropdb',
                     'format = deplatformer_webapp.scripts:format',
                     'lint = deplatformer_webapp.scripts:lint']}

setup_kwargs = {
    'name': 'deplatformer-webapp',
    'version': '0.1.8',
    'description': 'Flask webapp for the deplatformer platform',
    'long_description': '# Deplatformer\n\n[![PyPI](https://img.shields.io/pypi/v/deplatformer_webapp)](https://pypi.org/project/deplatformer-webapp/)\n[![License: MIT](https://img.shields.io/pypi/l/deplatformer_webapp)]()\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA prototype of the Deplatformr concept created as part of the [Gitcoin Apollo](https://gitcoin.co/hackathon/filecoin/) hackathon.\n\nBuilt with [Flask](https://palletsprojects.com/p/flask/) and [Pygate](https://pygate.tech).\n\nFor more information see:\n\n* Deplatformr Substack: [Help us test our prototype](https://deplatformr.substack.com/p/help-us-test-our-prototype)\n* Deplatformr YouTube: [project introduction](https://youtu.be/-jfq4FYopNM)\n\n![screencap](deplatformr/static/sample_data/deplatformr-prototype.png)\n',
    'author': 'Deplatformer Team',
    'author_email': 'info@deplatformer.io',
    'maintainer': 'Antreas Pogiatzis',
    'maintainer_email': 'antreas@deplatformer.io',
    'url': 'https://deplatformer.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
