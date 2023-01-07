# module imports
from argparse import Namespace
from hashlib import md5, sha1, sha256, sha512
from multiprocessing.pool import ThreadPool
from os import getcwd, listdir, mkdir, path, remove, system
from pathlib import Path
from shutil import rmtree
from subprocess import getstatusoutput

# local imports
from . import logger
from .utils import cmd_in_path


class Packages:
	def __init__(self, args: Namespace):
		# dir
		self.dir: str = args.dir
		
		# output
		self.output: str = args.output
		
		# run
		self.packages()
	
	def __extract(self, file: str) -> str:
		# filename
		filename = Path(file).name
		# get full path
		path = f'{file if file.startswith("/") else getcwd() + "/" + file}'
		# get ar command
		ar = cmd_in_path('ar')
		# ensure file exists
		if ar == None:
			logger.error('Command "ar" is not installed. Please install it in order to use this script.')
			exit(1)
		# make tmp dir
		mkdir(f'./.{filename}.tmp')
		# extract deb
		system(f'cd ./.{filename}.tmp && ar x {path}')
		# remove all files except control
		for file in listdir(f'.{filename}.tmp'):
			if not file.startswith('control'):
				remove(f'.{filename}.tmp/{file}')
			else:
				match file:
					case 'control.tar.xz':
						system(f'cd .{filename}.tmp && tar xf control.tar.xz')
						remove(f'.{filename}.tmp/{file}')
					case 'control.tar.gz':
						system(f'cd .{filename}.tmp && tar xf control.tar.gz')
						remove(f'.{filename}.tmp/{file}')
					case 'control.tar.lzma':
						system(f'cd .{filename}.tmp && tar xf control.tar.lzma')
						remove(f'.{filename}.tmp/{file}')
					case 'control.tar.zst':
						system(f'cd .{filename}.tmp && tar xf control.tar.zst')
						remove(f'.{filename}.tmp/{file}')
					case _:
						logger.error(f'Unknown archive format. ({file.replace("control", "")})')
						exit(1)

		contents = open(f'.{filename}.tmp/control', 'r').read()
		# delete tmp dir
		rmtree(f'.{filename}.tmp')
		return contents
		
	
	def __pack(self, file: str) -> str:
		package = ''
		
		if file.endswith('.deb'):
			# declare path
			filepath = path.join(self.dir, file)
				
			# extract deb
			if self.output is not None:
				log_stdout(f'Extracting {file}...')
			control = self.__extract(filepath)
			if self.output is not None:
				remove_log_stdout(f'Extracting {file}...')
			
			# parse control file
			#if self.output is not None:
			#	log_stdout(f'Parsing {file}/control...')
			#control_parsed = Control(control)
			#if self.output is not None:
			#	remove_log_stdout(f'Parsing {file}/control...')
			
			# add control to packages
			package += control
			
			# generate hashes
			md5sum = md5()
			sha1sum = sha1()
			sha256sum = sha256()
			sha512sum = sha512()
				
			with open(filepath, 'rb') as source:
				block = source.read(2**16)
				while len(block) != 0:
					md5sum.update(block)
					sha1sum.update(block)
					sha256sum.update(block)
					sha512sum.update(block)
					block = source.read(2**16)
				
			package += f'MD5sum: {md5sum.hexdigest()}\nSHA1: {sha1sum.hexdigest()}\nSHA256: {sha256sum.hexdigest()}\nSHA512: {sha512sum.hexdigest()}\n'
				
			# add filename
			package += f'Filename: {path.join(self.dir, file)}\n'
			# add size
			package += f'Size: {path.getsize(filepath)}\n'
		return package

	
	def packages(self):
		packages = ""
		# check if path exists
		if not path.exists(self.dir):
			logger.error(f'Directory "{self.dir}" does not exist.')
			exit(1)
		# make sure path is a dir
		if not path.isdir(self.dir):
			logger.error(f'"{self.dir}" is not a directory.')
			exit(1)
			
		with ThreadPool() as pool:
		# call the function for each item concurrently
			for result in pool.map(self.__pack, listdir(self.dir)):
				if packages != "":
					packages += "\n"
				packages += result
		
		# log if necessary
		if self.output is None:
			print(packages)
			exit(0)
		
		# write if necessary
		with open(self.output, 'w') as f:
			f.write(packages)
			f.close()
		
		logger.log('Done!')