from setuptools import setup, find_packages

setup(
  name = 'fcryptor',
  version = '1.0.6',
  author = 'Omid Karimzade',
  author_email = 'omidekz@gmail.com',
  description = 'python package that encrypt/decrypt files by key.',
  long_description=open('README.md', 'r').read(),
  long_description_content_type="text/markdown",
  license='MIT',
  keywords = ['file encryptor', 'file cryptography', 'file crypt', 'decrypt', 'fcryptor', 'file-cryptor'],
  url = 'https://github.com/omidekz/fcryptor',
  packages = find_packages(),
  install_requires=[
          'cryptography'
  ],
  entry_points={
	'console_scripts': [
		'fcryptor = fcryptor.fcryptor:main'
	]
  },
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Security :: Cryptography',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
