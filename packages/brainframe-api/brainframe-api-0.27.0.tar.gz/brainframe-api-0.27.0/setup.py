# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api', 'api.bf_codecs', 'api.stubs']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0', 'pillow>=7.2.0,<8.0.0', 'requests>=2.24.0,<3.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'brainframe-api',
    'version': '0.27.0',
    'description': 'Provides a Python wrapper around the BrainFrame REST API.',
    'long_description': '=====================\nBrainFrame Python API\n=====================\n\n.. image:: https://readthedocs.org/projects/brainframe-python-api/badge/?version=latest\n   :target: https://brainframe-python-api.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://circleci.com/gh/aotuai/brainframe_python.svg?style=svg\n   :target: https://circleci.com/gh/aotuai/brainframe_python\n   :alt: Publish Packages CI Status\n\nThis library is a Python wrapper around the BrainFrame REST API. It allows for\neasy interaction with a BrainFrame server.\n\n.. code-block:: python\n\n   from brainframe.api import BrainFrameAPI, bf_codecs\n\n   # Connect to the server\n   api = BrainFrameAPI("http://localhost")\n   # Create a new IP camera stream\n   stream_config = api.set_stream_configuration(\n       bf_codecs.StreamConfiguration(\n           name="New Stream",\n           connection_type=bf_codecs.ConnType.IP_CAMERA,\n           connection_options={"url": "rtsp://192.168.1.100"},\n           runtime_options={},\n       ))\n   api.start_analyzing(stream_config.id)\n   # Get results\n   analysis_results = api.get_latest_zone_statuses()\n\n\nInstallation\n------------\n\nThe BrainFrame Python API is available on PyPI and can be installed with pip.\nInstall the version of the library that matches the version of BrainFrame that\nyou are using. For example, if you are using BrainFrame version 0.26.1:\n\n.. code-block:: bash\n\n   pip3 install brainframe-api==0.26.1\n\nDocumentation\n-------------\n\nDocumentation for this library is available on `ReadTheDocs`_.\n\n.. _`ReadTheDocs`:\n   https://brainframe-python-api.readthedocs.io/en/latest/\n\n',
    'author': 'Aotu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aotuai/brainframe_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
