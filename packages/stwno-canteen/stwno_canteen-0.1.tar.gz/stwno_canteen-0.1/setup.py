import setuptools
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README").read_text()

# This call to setup() does all the work
setuptools.setup(
  name = 'stwno_canteen',
  version = '0.1',
  license='MIT',
  description = 'simple API to access the STWNO canteen\'s menus',
  long_description=README,
  long_description_content_type='text/markdown',
  author = 'Stefan Sommer aka somsky',
  author_email = 'stefan.sommer.per@gmail.com',
  url = 'https://github.com/somsky/stwno_canteen',
  keywords = ['stwno'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
  packages=['stwno_canteen'],
  python_requires='>=3.8'
)
