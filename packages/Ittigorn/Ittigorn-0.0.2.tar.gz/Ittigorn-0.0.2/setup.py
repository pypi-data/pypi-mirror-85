import setuptools

with open('README.md', 'r') as fh:
  long_desc = fh.read()

setuptools.setup(
  name                          = 'Ittigorn',
  version                       = '0.0.2',
  auther                        = 'Ittigorn Tradussadee',
  auther_email                  = 'ittigorn.tra@gmail.com',
  description                   = 'My helper classes library',
  long_description              = long_desc,
  long_description_content_type = 'text/markdown',
  url                           = 'https://github.com/ittigorn-tra/Ittigorn',
  packages                      = setuptools.find_packages(),
  install_requires              = ['pandas'],
  classifiers                   = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
  python_requires               = '>=3.7',
)