# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bhej']

package_data = \
{'': ['*']}

install_requires = \
['requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.24.0,<3.0.0',
 'tqdm>=4.51.0,<5.0.0',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':sys_platform == "linux"': ['python-magic>=0.4.3,<0.5.0'],
 ':sys_platform == "win32" or sys_platform == "darwin"': ['python-magic-bin==0.4.14']}

entry_points = \
{'console_scripts': ['bhej = bhej.main:app',
                     'deploy_prod = bhej.scripts:deploy_prod',
                     'deploy_staging = bhej.scripts:deploy_staging']}

setup_kwargs = {
    'name': 'bhej',
    'version': '0.1.6',
    'description': 'Share files like a dev.',
    'long_description': "# bhej\n\n> Share files like a dev.\n\n## Installation\n\nTo install this cli to your environment, just run...\n\n```[bash]\npip install bhej\n```\n\n...and you're good to go!\n\n## Usages\n\nTo upload a file, just run the following.\n\n```[bash]\nbhej up <filename>\n# You'll receive a 6 digit code to share.\n# You'll also get a link that you can directly download from.\n```\n\nTo download a file, just run the following.\n\n```[bash]\nbhej down <code> # Use the 6 digit code from the upload step.\n```\n\n## Development\n\nWant to contribute? After cloning and `cd`-ing into the project directory,\nyou can run the following to get set up.\n\n```[bash]\npoetry shell    # Sets up virtual environment.\npoetry install  # Installs dependencies.\nwhich bhej      # Should return your local version of the CLI.\n```\n\n### Deploying to PyPi\n\nTo deploy to Test PyPi, run `poetry run deploy_staging`. To deploy to the Prod PyPi, run `poetry run deploy_prod`.\n\nTo install it from Test PyPi, run the following.\n\n```[bash]\npip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple bhej\n```\n\nTo install from Prod PyPi, run `pip install bhej`.\n",
    'author': 'ivraj',
    'author_email': 'iseerha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bhej.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
