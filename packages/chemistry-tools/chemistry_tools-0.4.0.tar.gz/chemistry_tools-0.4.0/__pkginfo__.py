#  This file is managed by 'repo_helper'. Don't edit it directly.
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This file is distributed under the same license terms as the program it came with.
#  There will probably be a file called LICEN[S/C]E in the same directory as this file.
#
#  In any case, this program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py
#

# stdlib
import pathlib

__all__ = [
		"__copyright__",
		"__version__",
		"repo_root",
		"install_requires",
		"extras_require",
		]

__copyright__ = """
2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

__version__ = "0.4.0"

repo_root = pathlib.Path(__file__).parent
install_requires = (repo_root / "requirements.txt").read_text(encoding="utf-8").split('\n')
extras_require = {
		'pubchem': [
				'cawdrey>=0.1.7', 'mathematical>=0.1.13', 'pillow>=7.0.0', 'pyparsing>=2.2.0', 'tabulate>=0.8.3'
				],
		'formulae': ['cawdrey>=0.1.7', 'mathematical>=0.1.13', 'pyparsing>=2.2.0', 'tabulate>=0.8.3'],
		'plotting': ['matplotlib>=3.0.0'],
		'toxnet': ['beautifulsoup4>=4.7.0'],
		'all': [
				'beautifulsoup4>=4.7.0',
				'cawdrey>=0.1.7',
				'mathematical>=0.1.13',
				'matplotlib>=3.0.0',
				'pillow>=7.0.0',
				'pyparsing>=2.2.0',
				'tabulate>=0.8.3'
				]
		}
