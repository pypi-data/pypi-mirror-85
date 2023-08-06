from typing import Set, Tuple
import pathlib
import subprocess

import toml

import cq.checkers.requirements


def _is_poetry_project(path: str) -> bool:
	pyproject_file = pathlib.Path(path) / 'pyproject.toml'
	if not pyproject_file.is_file():
		return False
	pyproject = toml.load(pyproject_file)
	return bool(pyproject.get('tool', {}).get('poetry'))


def autodisable(modules: Tuple[str]) -> Set[str]:
	'''
	Automatically disable checkers based on the environment in which cq runs.
	Rules:
		1. Disable requirements checker for poetry projects
	'''
	disable: Set[str] = set()
	# Disable requirements checker for poetry projects
	try:
		project_root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output = True, check = True)
		if _is_poetry_project(project_root.stdout.decode('utf-8').strip()):
			disable.add(cq.checkers.requirements.RequirementsvalidatorChecker.NAME)
	except subprocess.CalledProcessError:
		for module in modules:
			if _is_poetry_project(module):
				disable.add(cq.checkers.requirements.RequirementsvalidatorChecker.NAME)
	return disable
