# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manim',
 'manim.animation',
 'manim.camera',
 'manim.config',
 'manim.grpc',
 'manim.grpc.gen',
 'manim.grpc.impl',
 'manim.mobject',
 'manim.mobject.svg',
 'manim.mobject.types',
 'manim.renderer',
 'manim.scene',
 'manim.utils']

package_data = \
{'': ['*'], 'manim.grpc': ['proto/*']}

install_requires = \
['Pillow',
 'cairocffi>=1.1.0,<2.0.0',
 'colour',
 'grpcio',
 'grpcio-tools',
 'numpy',
 'pangocairocffi>=0.3.0,<0.4.0',
 'pangocffi>=0.6.0,<0.7.0',
 'progressbar',
 'pycairo>=1.20,<2.0',
 'pydub',
 'pygments',
 'rich>=4.2.1',
 'scipy',
 'tqdm',
 'watchdog']

entry_points = \
{'console_scripts': ['manim = manim.__main__:main',
                     'manimcm = manim.__main__:main']}

setup_kwargs = {
    'name': 'manim',
    'version': '0.1.0',
    'description': 'Animation engine for explanatory math videos.',
    'long_description': "![logo](https://raw.githubusercontent.com/ManimCommunity/manim/master/logo/banner.png)\n\n![CI](https://github.com/ManimCommunity/manim/workflows/CI/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/manimce/badge/?version=latest)](https://manimce.readthedocs.io/en/latest/?badge=latest)\n[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)\n[![Manim Subreddit](https://img.shields.io/reddit/subreddit-subscribers/manim.svg?color=ff4301&label=reddit)](https://www.reddit.com/r/manim/)\n[![Manim Discord](https://img.shields.io/discord/581738731934056449.svg?label=discord)](https://discord.gg/mMRrZQW)\n\nManim is an animation engine for explanatory math videos. It's used to create precise animations programmatically, as seen in the videos at [3Blue1Brown](https://www.3blue1brown.com/).\n\n> NOTE: This repository is maintained by the Manim Community, and is not associated with Grant Sanderson or 3Blue1Brown in any way (though we are definitely indebted to him for providing his work to the world). If you want to study how Grant makes his videos, head over to his repository (3b1b/manim). This is a more frequently updated repository than that one, and is recommended if you want to use Manim for your own projects.\n\n## Table of Contents:\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [Documentation](#documentation)\n- [Help with Manim](#help-with-manim)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Installation\n\nManim has a few dependencies that need to be installed before it. Please visit\nthe\n[documentation](https://manimce.readthedocs.io/en/latest/installation.html)\nand follow the instructions according to your operating system.\n\n## Usage\n\nHere is an example manim script:\n\n```python\nfrom manim import *\n\nclass SquareToCircle(Scene):\n    def construct(self):\n        circle = Circle()\n        square = Square()\n        square.flip(RIGHT)\n        square.rotate(-3 * TAU / 8)\n        circle.set_fill(PINK, opacity=0.5)\n\n        self.play(ShowCreation(square))\n        self.play(Transform(square, circle))\n        self.play(FadeOut(square))\n```\n\nSave this code in a file called `example.py`. Now open your terminal in the\nfolder where you saved the file and execute\n\n```sh\nmanim example.py SquareToCircle -pl\n```\n\nYou should see your video player pop up and play a simple scene where a square\nis transformed into a circle. You can find some more simple examples in the\n[GitHub repository](https://github.com/ManimCommunity/manim/tree/master/example_scenes).\nVisit the [official gallery](https://manimce.readthedocs.io/en/latest/examples.html) for more advanced examples.\n\n## Command line arguments\n\nThe general usage of manim is as follows:\n\n![manim-illustration](https://raw.githubusercontent.com/ManimCommunity/manim/master/readme-assets/command.png)\n\nThe `-p` flag in the command above is for previewing, meaning the video file will automatically open when it is done rendering. The `-l` flag is for a faster rendering at a lower quality.\n\nSome other useful flags include:\n\n- `-s` to skip to the end and just show the final frame.\n- `-n <number>` to skip ahead to the `n`'th animation of a scene.\n- `-f` show the file in the file browser.\n\nFor a thorough list of command line arguments, visit the\n[documentation](https://manimce.readthedocs.io/en/latest/tutorials/configuration.html).\n\n## Documentation\n\nDocumentation is in progress at [ReadTheDocs](https://manimce.readthedocs.io/en/latest/).\n\n## Help with Manim\n\nIf you need help installing or using Manim, please take a look at [the Reddit\nCommunity](https://www.reddit.com/r/manim) or the [Discord\nCommunity](https://discord.gg/mMRrZQW). For bug reports and feature requests,\nplease open an issue.\n\n## Contributing\n\nIs always welcome. In particular, there is a dire need for tests and\ndocumentation. For guidelines please see the\n[documentation](https://manimce.readthedocs.io/en/latest/contributing.html).\nThis project uses [Poetry](https://python-poetry.org/docs/) for management. You need to have poetry installed and available in your environment.\nYou can find more information about it in its [Documentation](https://manimce.readthedocs.io/en/latest/installation/for_dev.html)\n\n## License\n\nThe software is double-licensed under the MIT license, with copyright\nby 3blue1brown LLC (see LICENSE), and copyright by Manim Community\nDevelopers (see LICENSE.community).\n",
    'author': 'The Manim Community Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manimcommunity/manim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
