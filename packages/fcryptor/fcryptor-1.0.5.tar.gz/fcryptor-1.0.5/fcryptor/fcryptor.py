import os
import argparse

from cryptography.fernet import Fernet

class FCryptorBase:
	def __init__(self, key=None):
		if not key:
			key = Fernet.generate_key()
		FCryptorBase.__check_type_is(key, bytes)
		self.key = key.decode()
		self.__fkey = Fernet(key)

	@staticmethod
	def __check_type_is(item, be, raise_error=True):
		if type(item) != be:
			if raise_error:
				raise ValueError(str(item)+" must be bytes")
			return False
		return True

	def crypt(self, message):
		FCryptorBase.__check_type_is(message, bytes)
		return self.__fkey.encrypt(message).decode()

	def decrypt(self, message):
		FCryptorBase.__check_type_is(message, bytes)
		return self.__fkey.decrypt(message).decode()

class FCryptor(FCryptorBase):
	def __init__(self, key=None):
		super().__init__(key)

	@staticmethod
	def __check_files(path, exists=True, file=True):
		path = os.path.abspath(path)
		if exists and not os.path.exists(path):
			raise ValueError("{} not exists".format(path))
		if file and not os.path.isfile(path):
			raise ValueError("{} is not regular file".format(path))
		return path

	@staticmethod
	def __load_file(path):
		return open(path, 'rb').read()

	def crypt(self, inputpath, outpath=None, from_stdin=None):
		if from_stdin:
			input_data = inputpath.encode()
		else:
			inputpath = FCryptor.__check_files(inputpath)
			input_data = FCryptor.__load_file(inputpath)

		output = super().crypt(input_data)

		if outpath:
			outpath = FCryptor.__check_files(outpath, exists=False, file=False)
			output_file = open(outpath, 'w')
			output_file.write(output)
			output_file.close()

		return output

	def decrypt(self, inputpath, outpath, from_stdin=None):
		if from_stdin:
			input_data = inputpath.encode()
		else:
			inputpath = FCryptor.__check_files(inputpath)
			input_data = FCryptor.__load_file(inputpath)
		output = super().decrypt(input_data)

		if outpath:
			outpath = FCryptor.__check_files(outpath, exists=False, file=False)
			output_file = open(outpath, 'w')
			output_file.write(output)
			output_file.close()

		return output

def main():
	parser = argparse.ArgumentParser()
	
	crypt_xor_decryot = parser.add_mutually_exclusive_group(required=True)
	crypt_xor_decryot.add_argument("-c", "--crypt", action="store_true",help="Crypt File", dest='crypt')
	crypt_xor_decryot.add_argument("-d", "--decrypt", action="store_true", help="Decrypt File")

	parser.add_argument("-si", "--stdin", help="when stdin is true", action="store_true", default=False)

	parser.add_argument("-i", "--input", help="Input File/stdin [for stdin pass -si | --stdin]", required=True)
	parser.add_argument("-o", "--output", help="Output File")

	parser.add_argument("-k", "--key", help="key of/for file")

	parser.add_argument("-gk", "--genkey", help="generate a key", action="store_true")

	args = parser.parse_args()

	if args.genkey:
		print (Fernet.generate_key().decode())
		return
	
	if args.decrypt and not args.key:
		print ('when pass -d, you have to pass -k [the Key] argument')
		return

	key = args.key or Fernet.generate_key().decode()
	show_key = not bool(args.key)

	fc = FCryptor(key.encode())
	output = getattr(fc, "crypt" if args.crypt else "decrypt")(args.input, args.output, args.stdin)

	if show_key:
	    print("Key is:", key)

	if not args.output:
	    print ("{}:".format("encrypt" if args.crypt else "decrypt"))
	    print(output)

if __name__ == '__main__':
	main()
