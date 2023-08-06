"""
Convert ipynb notebook to python script

Requires nbconvert (pip install nbconvert) and pandoc (apt-get install pandoc)
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 2
#  as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# 3rd party
import isort  # type: ignore
import yapf_isort
from domdf_python_tools.compat import importlib_resources
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from nbconvert import PythonExporter  # type: ignore

# this package
import notebook2script

__all__ = ["convert_notebook"]

py_exporter = PythonExporter()


def convert_notebook(
		nb_file: PathLike,
		outfile: PathLike,
		):
	"""
	Convert a notebook to a python file.

	:param nb_file: Filename of the Jupyter Notebook to convert.
	:param outfile: Filename to save the output script as.
	"""

	nb_file = PathPlus(nb_file)
	outfile = PathPlus(outfile)
	outfile.parent.maybe_make()

	script, *_ = py_exporter.from_file(str(nb_file))

	outfile.write_clean(script)

	with importlib_resources.path(notebook2script, "isort.cfg") as isort_config:
		with importlib_resources.path(notebook2script, "style.yapf") as yapf_style:
			reformat_file(outfile, yapf_style=str(yapf_style), isort_config_file=str(isort_config))


def reformat_file(filename: PathLike, yapf_style: str, isort_config_file: str) -> int:
	"""
	Reformat the given file.

	:param filename:
	:param yapf_style: The name of the yapf style, or the path to the yapf style file.
	:param isort_config_file: The filename of the isort configuration file.
	"""

	old_isort_settings = isort.settings.CONFIG_SECTIONS.copy()

	try:
		isort.settings.CONFIG_SECTIONS["isort.cfg"] = ("settings", "isort")

		isort_config = isort.Config(settings_file=str(isort_config_file))
		r = yapf_isort.Reformatter(filename, yapf_style, isort_config)
		ret = r.run()
		r.to_file()

		return ret

	finally:
		isort.settings.CONFIG_SECTIONS = old_isort_settings
