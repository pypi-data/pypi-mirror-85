from setuptools import setup

with open("README.md", "r") as f:
  _long_description = f.read()


setup(
  name = 'levish',
  packages = ['levish', 'levish.commands'],
  version = '0.1.8.1',
  license='GPL-3.0 License',
  description = 'Create your own shell.',
  long_description = _long_description,
  long_description_content_type='text/markdown',
  author = 'Aaron Levi Can (aaronlyy)',
  author_email = 'aaronlevican@gmail.com',
  url = 'https://github.com/aaronlyy/levish',
  download_url = 'https://github.com/aaronlyy/levish/archive/v0.1.8.1tar.gz',
  keywords = ['shell', 'terminal', 'commands', 'cmd', 'console'],
  install_requires=[
        "pyfiglet"
      ],
)