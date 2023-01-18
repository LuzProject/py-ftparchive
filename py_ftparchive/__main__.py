# module imports
from argparse import ArgumentParser

# local imports
from . import logger
from .packages import Packages
from .release import Release
from .utils import get_version


def main(argv=None) -> None:
	parser = ArgumentParser()
	parser.add_argument('-v', '--version', action='version', version=f'py-ftparchive v{get_version()}',
	help='show current version and exit')
	sub_parsers = parser.add_subparsers(help='sub-command help', dest='command')
	
	# packages
	parser_packages = sub_parsers.add_parser('packages', help='compile all deb files in a directory into a Packages file')
	parser_packages.add_argument('dir', action='store', help='directory to read deb files from')
	parser_packages.add_argument('--output', type=str, help='file to output result to')
	
	# release
	parser_release = sub_parsers.add_parser('release', help='compile a release file')
	parser_release.add_argument('dir', action='store', help='directory to create a release file from')
	parser_release.add_argument('--output', type=str, help='file to output result to')
	parser_release.add_argument('-o', action='append', nargs='+', help='release config')
	
	args = parser.parse_args()
	
	if args.command is None:
		logger.error('Please specify an operation.')
		exit(1)
	
	if args.command == 'packages':
		Packages(args)
	elif args.command == 'release':
		Release(args)
	else:
		logger.error(f'Unknown command "{args.command}".')

if __name__ == '__main__':
	main()