
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'TOPSIS-kartikey-101803606',
  packages = setuptools.find_packages(),
  version = '1.0.0',
  license='MIT',
  description = 'TOPSIS Score Calculator',
  long_description = long_description,
  long_description_content_type="text/markdown",
  author = 'Kartikey Nigam',
  author_email = 'knigam_be18@thapar.edu',
  keywords = ['TOPSIS'],
  install_requires=[
        'numpy',
        'pandas'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
