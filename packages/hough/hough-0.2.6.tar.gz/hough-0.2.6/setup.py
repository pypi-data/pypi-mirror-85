# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hough', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['coverage[toml]>=5.0.4,<6.0.0',
 'docopt-ng>=0.7.2,<0.8.0',
 'filetype>=1.0.6,<2.0.0',
 'imageio>=2.8.0,<3.0.0',
 'numpy>=1.18.2,<2.0.0',
 'pymupdf>=1.17.0,<2.0.0',
 'scikit-image>=0.16.2,<0.18.0',
 'scipy>=1.4.1,<2.0.0',
 'termplotlib>=0.3.0,<0.4.0',
 'tqdm>=4.43.0,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=2.0.0,<3.0.0']}

entry_points = \
{'console_scripts': ['hough = hough.cli:run']}

setup_kwargs = {
    'name': 'hough',
    'version': '0.2.6',
    'description': 'Skew detection and correction in scanned images',
    'long_description': '# hough - Skew detection in scanned images\n\n<p align="center">\n<a href="https://github.com/wohali/hough/actions"><img alt="Actions Status" src="https://github.com/wohali/hough/workflows/Tests/badge.svg"></a>\n<a href="https://pypi.org/project/hough/"><img alt="PyPI" src="https://img.shields.io/pypi/v/hough"></a>\n<a href="https://pypi.org/project/hough/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/hough"></a>\n<a href="https://github.com/wohali/hough/blob/master/COPYING"><img src="https://img.shields.io/github/license/wohali/hough.svg" alt="GPL v2.0 License" /></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://codecov.io/gh/wohali/hough"><img alt="Coverage stats" src="https://codecov.io/gh/wohali/hough/branch/master/graph/badge.svg" /></a>\n</p>\n\n_Hough_ finds skew angles in scanned document pages, using the Hough transform.\n\nIt is oriented to batch processing, and can make use of multiple cores. (You\'ll\nwant this - analysis and image processing is very CPU intensive!)\n\n# Installation and usage\n\n## Installation\n\n```\npip install -U pip\npip install hough\n```\n\nThe first line is required to update `pip` to a new enough version to be\ncompatible with `manylinux` wheel packaging, required for PyMuPDF.\n\nOlder versions of `pip` are fine, but you\'ll have to install MuPDF, its\nheaders, and a compiler first, so PyMuPDF can be compiled locally.\n\n## Usage\n\nTo get started right away, here\'s some examples.\n\nGenerate angles (in CSV form) for a bunch of TIFF page images, one page per file:\n\n```\nhough --csv in/*.tif\n```\n\nThe same, but for a PDF file, and display a histogram at the end:\n\n```\nhough --histogram Able_Attach_Sep83.pdf\n```\n\nThe same, but show progress while running:\n\n```\nhough -v --histogram Able_Attach_Sep83.pdf\n```\n\n\nThe deskewing results are placed in the `results.csv` file. Example:\n\n```csv\n"Input File","Page Number","Computed angle","Variance of computed angles","Image width (px)","Image height (px)"\n"/home/toby/my-pages/orig/a--0000.pgm.tif",,-0.07699791151672428,0.001073874144832815,5014,6659\n"/home/toby/my-pages/orig/a--0001.pgm.tif",,,,5018,6630\n"/home/toby/my-pages/orig/a--0002.pgm.tif",,0.24936351676615068,0.005137031681286154,5021,6629\n"/home/toby/my-pages/orig/a--0003.pgm.tif",,,,5020,6608\n"/home/toby/my-pages/orig/a--0004.pgm.tif",,-0.037485115754500545,0.025945115897015238,5021,6616\n```\n\nThe program should work on various image input formats, and with both grey scale\nand RGB images. _Hough_ works best with images ≥300dpi.\n\nHere\'s a histogram sample:\n\n```\n=== Skew statistics ===\n0.00° - 0.10°  [57]  ████████████████████████████████████████\n0.10° - 0.20°  [39]  ███████████████████████████▍\n0.20° - 0.30°  [30]  █████████████████████\n0.30° - 0.40°  [30]  █████████████████████\n0.40° - 0.50°  [11]  ███████▊\n0.50° - 0.60°  [11]  ███████▊\n0.60° - 0.70°  [ 3]  ██▏\n0.70° - 0.80°  [ 4]  ██▊\n0.80° - 0.90°  [ 0]\n0.90° - 1.00°  [ 1]  ▊\n1.00° - 1.10°  [ 1]  ▊\n1.10° - 1.20°  [ 0]\n1.20° - 1.30°  [ 1]  ▊\n1.30° - 1.40°  [ 1]  ▊\n1.40° - 1.50°  [ 1]  ▊\n1.50° - 1.60°  [ 2]  █▍\n1.60° - 1.70°  [ 0]\n1.70° - 1.80°  [ 1]  ▊\n1.80° - 1.90°  [ 2]  █▍\n1.90° - 2.00°  [ 0]\nSamples: 195\n50th percentile: 0.20°\n90th percentile: 0.55°\n99th percentile: 1.77°\n```\n\n## Command line options\n\nYou can list them by running `hough --help`:\n\n```\nhough - straighten scanned pages using the Hough transform.\n\nUsage:\n  hough (-h | --help)\n  hough [options] [FILE] ...\n  hough [options] [--results=<file>] [FILE] ...\n  hough (-r | --rotate) [options] [--results=<file>]\n  hough (-r | --rotate) [options] [--results=<file>] [FILE] ...\n\nArguments:\n  FILE                          input files to analyze/rotate\n\nOptions:\n  -h --help                     display this help and exit\n  --version                     display the version number and exit\n  -v --verbose                  print status messages\n  -d --debug                    retain debug image output in debug/ dir\n                                (also enables --verbose)\n  --histogram                   display rotation angle histogram summary\n  -o DIR, --out=DIR             store output results/images in named\n                                directory. Directory is created if it\n                                does not exist [default: out/TIMESTAMP]\n  --results=<file>              save results in FILE under output path,\n                                or specify path to results file for\n                                rotation [default: results.csv]\n  -w <workers> --workers=<#>    specify the number of workers to run\n                                simultaneously. Default: total # of CPUs\n  -r --rotate                   rotates the files passed on the command\n                                line, or if none given, those listed\n                                in the results file.\n```\n\n# Examples\n\nJust about all of [these files](http://docs.telegraphics.com.au/) have been\ndeskewed this way.\n\n# Getting the best results\n\n### NOTE: This is a beta product!\n\nThere\'s a few guidelines you should follow to get the best deskewing results\nfrom your document scans:\n\n1. Bilevel (black-and-white) bitmaps will produce lower quality results.\n   For best results, scan to greyscale or RGB first, deskew with _Hough_, then\n   reduce the colour depth to bilevel.\n1. Hough deskewing is an inexact process, with many heuristics discovered\n   by trial and error. _Hough_ may not work well on your material without tuning\n   and further modification. (We\'d love your pull requests!)\n\n## Debugging output\n\nYou can spy on _Hough_\'s attempts to perform deskewing by passing the `--debug`\nflag on the command line. The generated images, and any detected lines in them,\nare placed in the `debug/<datetime>/` directory.\n\nNote that _Hough_ cannot always determine a skew for a page (e.g. blank pages\nin particular), and will very occasionally get the skew wrong (depending on\nsource material). It\'s worth reviewing these images if _Hough_ makes a bad\ndecision on your scans. Please submit these files along with the original image\nwhen filing an issue!\n\n## Recommended scanners\n\nThe authors have tested this software with output from the following scanners:\n\n* Fujitsu fi-4530C, USB\n  * Fast\n  * Cheap on eBay\n  * Requires a Windows XP VirtualBox for drivers\n* Brother ADS-2700W, USB + Ethernet + WiFi\n  * Fast\n  * Can scan directly to the network or to a memory stick\n  * Factory reconditioned models stilll available (March 2020)\n  * Very low skew out of the box\n* Epson WF-7610, USB + Ethernet + WiFi\n  * 11"x17" and duplex capable\n  * Can scan directly to the network or to a memory stick\n\n# Developing\n\nFirst, clone this repo.\n\nYou\'ll need to install [Poetry](https://python-poetry.org/docs/#installation),\nthen run:\n\n```\npoetry run pip install -U pip setuptools\npoetry install\npoetry shell\n```\n\n# License notice\n\n```\nThis file is part of "hough", which detects skew angles in scanned images\nCopyright (C) 2016-2020 Toby Thain <toby@telegraphics.com.au>\nCopyright (C) 2020 Joan Touzet <wohali@apache.org>\n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation; either version 2 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA\n```\n',
    'author': 'qu1j0t3',
    'author_email': 'support@telegraphics.com.au',
    'maintainer': 'Joan Touzet',
    'maintainer_email': 'wohali@apache.org',
    'url': 'https://github.com/wohali/hough',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
