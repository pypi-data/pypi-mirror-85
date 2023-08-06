from typing import List
import functools
import os

import isort
import isort.format

import cq.checker
import cq.checkers.isort_config
import cq.utils


class IsortChecker(cq.checker.Checker):
	NAME = 'isort'
	HELP_LINE = 'Run `cq --fix`'
	DESCRIPTION = 'Checks whether imports are sorted according to the code style.'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		# We are monkey-patching isort module to redirect stdout to os.devnull.
		# This relies on the current implementation where
		# `isort.check_file` calls `create_terminal_printer` without `output` argument.
		_create_terminal_printer = isort.format.create_terminal_printer
		isort.format.create_terminal_printer = functools.partial(_create_terminal_printer, output = os.devnull)

		results = {
			python_file: isort.check_file(python_file, config = cq.checkers.isort_config.Config)
			for python_file in cq.utils.get_all_python_files(modules)
		}

		# Revert the monkey-patch
		isort.format.create_terminal_printer = _create_terminal_printer

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = 0,
			output = [
				cq.checker.ResultLine(
					file = filename,
					line = None,
					message = 'Imports are incorrectly sorted and/or formatted.',
					is_error = False,
				)
				for filename, result in results.items()
				if result is False
			],
		)
