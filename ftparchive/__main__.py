# module imports
from argparse import ArgumentParser

# local imports
from . import logger
from .packages import Packages
from .utils import get_version


def main(argv=None) -> None:
	parser = ArgumentParser()
	sub_parsers = parser.add_subparsers(help='sub-command help', dest='command')
	
	# packages
	parser_packages = sub_parsers.add_parser('packages', help='compile all deb files in a directory into a Packages file')
	parser_packages.add_argument('dir', action='store', help='directory to read deb files from')
	parser_packages.add_argument('--output', type=str, help='file to output result to')
	
	# release
	parser_release = sub_parsers.add_parser('release', help='compile a release file')
	parser_release.add_argument('dir', action='store', help='directory to create a release file from')
	parser_release.add_argument('--output', type=str, help='file to output result to')
	
	args = parser.parse_args()
	
	if args.command == 'packages':
		Packages(args)
	elif args.command == 'release':
		logger.log('RELEASE')
	else:
		logger.error(f'Unknown command "{args.command}".')

if __name__ == '__main__':
	main()