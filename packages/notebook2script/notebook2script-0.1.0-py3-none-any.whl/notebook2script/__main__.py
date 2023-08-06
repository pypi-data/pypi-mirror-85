#!/usr/bin/env python3
#
#  __main__.py
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

# stdlib
import argparse
import glob
import os
import pathlib
import sys
from typing import Iterable, Union

# 3rd party
from pre_commit_hooks.fix_encoding_pragma import fix_encoding_pragma  # type: ignore

# this package
from notebook2script.ipynb2py import convert_notebook
from notebook2script.pointless import Pointless

__all__ = ["main", "process_multiple_notebooks", "process_notebook"]

linter = Pointless()


def main() -> int:

	parser = argparse.ArgumentParser(description="Convert Jupyter Notebooks to Python scripts")

	parser.add_argument("notebooks", metavar="NOTEBOOK", type=str, nargs='+', help="The notebooks to convert")
	parser.add_argument(
		"-o", "--outdir", type=pathlib.Path, default=pathlib.Path.cwd(),
		help="Directory to save the output scripts in.")  # yapf: disable
	parser.add_argument("-f", "--overwrite", action="store_true", help="Overwrite existing files.")

	args = parser.parse_args()

	notebooks = []

	for notebook in args.notebooks:
		notebooks += glob.glob(notebook)

	# pprint(notebooks)
	# print(notebooks[0])

	if not notebooks:
		parser.error("the following arguments are required: NOTEBOOK")

	return process_multiple_notebooks(notebooks, args.outdir, overwrite=args.overwrite)


def process_multiple_notebooks(
		notebooks: Iterable[Union[str, pathlib.Path]],
		outdir: Union[str, pathlib.Path, os.PathLike],
		overwrite: bool = False,
		) -> int:
	"""

	:param notebooks: An iterable of notebook filenames to process
	:param outdir: The directory to store the Python output in.
	:param overwrite: Whether to overwrite existing files. Default :py:obj:`False`
	"""

	if not isinstance(outdir, pathlib.Path):
		outdir = pathlib.Path(outdir)

	all_notebooks = []

	for notebook in notebooks:
		all_notebooks += glob.glob(str(notebook))

	# print(all_notebooks)
	# input(">")

	ret = 0

	for notebook in all_notebooks:
		notebook = pathlib.Path(notebook)
		outfile = outdir / f"{notebook.stem}.py"

		if outfile.is_file() and not overwrite:
			print(f"Info: Skipping existing file {outfile}")
		else:
			if notebook.is_file():
				print(f"Converting {notebook} to {outfile}")
				process_notebook(notebook, outfile)
			else:
				print(f"{notebook} not found")
				ret |= 1

	return ret


def process_notebook(notebook, outfile: Union[str, pathlib.Path, os.PathLike]) -> None:
	"""

	:param notebook: The filename of the notebook to process
	:param outfile: The filename to store the Python output as.
	"""

	convert_notebook(notebook, outfile)
	linter.process_file(outfile)
	with open(outfile, "r+b") as f:
		fix_encoding_pragma(f, remove=True, expected_pragma=b"# coding: utf-8")


if __name__ == "__main__":
	try:
		sys.exit(main())
	except KeyboardInterrupt:
		sys.exit(1)
