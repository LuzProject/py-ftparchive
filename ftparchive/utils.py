# module imports
from pathlib import Path
from pkg_resources import get_distribution
from shutil import which
from sys import stdout
from typing import Union

# local imports
from .logger import colors


def cmd_in_path(cmd: str) -> Union[None, str]:
	'''Check if command is in PATH'''
	path = which(cmd)
	
	if path is None:
		return None
	
	return path

def log_stdout(tolog: str):
	log = colors['bold'] + colors['darkgrey'] + '[' + colors['reset'] + colors['bold'] + colors['green'] + '*' + colors['bold'] + colors['darkgrey'] + '] ' + colors['reset'] + tolog
	stdout.write(log)
	stdout.flush()


def remove_log_stdout(toremove: str):
	log = colors['bold'] + colors['darkgrey'] + '[' + colors['reset'] + colors['bold'] + colors['green'] + '*' + colors['bold'] + colors['darkgrey'] + '] ' + colors['reset'] + toremove
	for _ in range(len(log)):
		stdout.write('\033[D \033[D')
		stdout.flush()

def get_version() -> str:
	# Check if running from a git repository,
	# then, construct version in the following format: version-branch-hash
	#if Path('.git').exists():
	#	return f'{get_distribution(__package__).version}-{getoutput('git rev-parse --abbrev-ref HEAD')}-{getoutput('git rev-parse --short HEAD')}'
	#else:
	#	return get_distribution(__package__).version
	return '0.0.1'