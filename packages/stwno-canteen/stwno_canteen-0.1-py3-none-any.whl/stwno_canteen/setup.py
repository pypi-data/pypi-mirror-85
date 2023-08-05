from distutils.core import setup
setup(
  name = 'stwno_canteen',
  packages = ['stwno_python'],
  version = '0.1',
  license='MIT',
  description = 'simple API to access the STWNO canteen\'s menus',
  author = 'Stefan Sommer aka somsky',
  author_email = 'stefan.sommer.per@gmail.com',
  url = 'https://github.com/somsky/stwno_canteen',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['stwno'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)
