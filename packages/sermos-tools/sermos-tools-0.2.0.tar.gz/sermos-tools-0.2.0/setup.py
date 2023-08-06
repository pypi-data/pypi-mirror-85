""" Sermos Tools Setup
"""
import os
import re
import ast
from setuptools import setup, find_packages
from sermos_tools.constants import BASE_CATALOG_DIR
from sermos_tools.sermos_tools import list_available_tools

_VERSION_RE = re.compile(r'__version__\s+=\s+(.*)')

with open('sermos_tools/__init__.py', 'rb') as f:
    __version__ = str(
        ast.literal_eval(
            _VERSION_RE.search(f.read().decode('utf-8')).group(1)))

# Dynamically add extras based on available tools in the catalog.
_TOOL_REQUIREMENTS = {}
_TOOLS = list_available_tools(as_dict=True)

for tool in _TOOLS.keys():
    with open(BASE_CATALOG_DIR + tool + '/requirements.txt', 'r') as f:
        _TOOL_REQUIREMENTS[tool] = f.read().splitlines()

# Create our extras require dictionary.
extras_require = {
    **{
        'dev': ['honcho'],
        'build': ['twine', 'wheel'],
        'docs': ['sphinx>=3.0.2,<4', 'boto3>=1.11,<2'],
        'test': [
            'pytest-cov>=2.6.1,<3', 'tox>=3.14.1,<4', 'coverage>=4.5,<5', 'mock>=1,<2'
        ]
    },
    **_TOOL_REQUIREMENTS
}

setup(name='sermos-tools',
      version=__version__,
      description="Sermos Tools",
      long_description=open('README.md', 'r').read(),
      maintainer="Sermos, LLC",
      license="Commercial",
      url="https://bitbucket.org/rhoai/sermos-tools",
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      install_requires=[],
      extras_require=extras_require,
      cmdclass={})
