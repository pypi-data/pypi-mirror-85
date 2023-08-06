# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlrd']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['mlrd = mlrd.__main__:main']}

setup_kwargs = {
    'name': 'mlrd',
    'version': '0.1.2',
    'description': 'Mcgrill Lecture Recording Download (mlrd) tool',
    'long_description': "mlrd\n====\n[![PyPi version](https://pypip.in/v/mlrd/badge.png)](https://pypi.org/project/mlrd/)\n\nA command line tool for downloading MyCourses lectures.\n\n## Responsible use & copyright warning\n> **Before using this tool, read the [university's responsible IT use document](https://www.mcgill.ca/secretariat/files/secretariat/responsible-use-of-mcgill-it-policy-on-the.pdf).**\n\n> **Additionally:: DO NOT SHARE DOWNLOADED LECTURES, THIS IS A BREACH OF THE PROFESSOR'S/UNIVERSITIES COPYRIGHT.**\n\n## Prerequisites\n- [Python 3.8+](https://www.python.org/downloads/)\n- [ffmpeg](https://ffmpeg.org/download.html)\n\n## Usage\nAfter installation, run the following command in your terminal:\n```\nmlrd <course_id> <output_dir> <auth_token>\n```\n\nThis will download all lectures for the given course to your directory of choice. The `<course_id>` and `<auth_token>` can be found by:\n1. navigating to desired course's lecture recording page on MyCourses.\n2. right click > inspect.\n3. ctrl/cmd + f and search for `HF_CourseId` and `HF_JWT`. The values of these elements correspond to the `<course_id>` and `<auth_token>`.",
    'author': 'Brendan',
    'author_email': 'bshizzle1234@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brendan-kellam/mlrd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
