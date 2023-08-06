import ast
import re
from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('flask_rhoauth/__init__.py', 'rb') as f:
    __version__ = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='Flask-RhoAuth',
    version=__version__,
    description="Rho AI Authorization Library",
    long_description=open('README.md', 'r').read(),
    maintainer="Rho AI",
    license="Commercial",
    url="https://bitbucket.org/rhoai/flask-rhoauth",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    extras_require={
        'openid': [
            'requests-oauthlib==1.2.0',
            'pyjwkest==1.4.0',
            'pyjwkest==1.4.0',
            'python-keycloak==0.15.0'
        ],
        'apiauth': [
            'Flask-SQLAlchemy'
        ],
        'test': [
            'pytest-cov==2.8.1',
            'tox==3.14.1',
            'mock==3.0.5',
            'psycopg2',
            'honcho'
        ]
    }
)
