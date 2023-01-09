# module imports
from argparse import Namespace
from datetime import datetime
from hashlib import md5, sha1, sha256, sha512
from os import listdir, path
from pathlib import Path
from time import gmtime, strftime

class Release:
	def __init__(self, args: Namespace):
		# dir
		self.dir: str = args.dir
		
		# output
		self.output: str = args.output
		
		# config
		self.config: list = list(map(lambda x: x[0].replace('APT::FTPArchive::Release::', ''), args.o))
		
		self.release()
	
	def __hash(self, file: str):
		hashed = {
			'filename': Path(file).name,
			'filepath': file,
			'size': path.getsize(file),
			'md5': md5(),
			'sha1': sha1(),
			'sha256': sha256(),
			'sha512': sha512()
		}
			
		with open(file, 'rb') as source:
			block = source.read(2**16)
			while len(block) != 0:
				hashed['md5'].update(block)
				hashed['sha1'].update(block)
				hashed['sha256'].update(block)
				hashed['sha512'].update(block)
				block = source.read(2**16)
		
		return hashed

	
	def release(self):
		# release var
		release = ''
		# hashes
		hashes = []
		
		# check if path exists
		if not path.exists(self.dir):
			logger.error(f'Directory "{self.dir}" does not exist.')
			exit(1)
		# make sure path is a dir
		if not path.isdir(self.dir):
			logger.error(f'"{self.dir}" is not a directory.')
			exit(1)
		
		# add config first
		for obj in self.config:
			release += f'{obj.split("=")[0]}: {obj.split("=")[1]}\n'
		
		# add date
		release += f'Date: {datetime.now().strftime("%a, %d %b %Y %H:%M:%S")} {strftime("%z", gmtime())}\n'
			
		# iterate through files
		for file in listdir(self.dir):
			if file == 'Packages' or file.startswith('Packages.'):
				hashes.append(self.__hash(path.join(self.dir, file)))
		
		if len(hashes) != 0:
			# md5
			release += 'MD5sum:\n'
			for hash in hashes:
				release += f' {hash.get("md5").hexdigest()} {(7 - len(str(hash.get("size")))) * " "} {hash.get("size")} {hash.get("filename")}\n'
			
			# sha1
			release += 'SHA1:\n'
			for hash in hashes:
				release += f' {hash.get("sha1").hexdigest()} {(7 - len(str(hash.get("size")))) * " "} {hash.get("size")} {hash.get("filename")}\n'
			
			# sha256
			release += 'SHA256:\n'
			for hash in hashes:
				release += f' {hash.get("sha256").hexdigest()} {(7 - len(str(hash.get("size")))) * " "} {hash.get("size")} {hash.get("filename")}\n'
				
			# sha512
			release += 'SHA512:\n'
			for hash in hashes:
				release += f' {hash.get("sha512").hexdigest()} {(7 - len(str(hash.get("size")))) * " "} {hash.get("size")} {hash.get("filename")}\n'
			
		
		# log if necessary
		if self.output is None:
			print(release)
			exit(0)
		
		# write if necessary
		with open(self.output, 'w') as f:
			f.write(release)
			f.close()
		
		logger.log('Done!')