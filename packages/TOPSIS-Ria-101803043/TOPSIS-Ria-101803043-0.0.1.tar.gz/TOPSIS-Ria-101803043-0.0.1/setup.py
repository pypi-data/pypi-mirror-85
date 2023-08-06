from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
  name = 'TOPSIS-Ria-101803043',
  version = '0.0.1',
  description = 'Find the Topsis Score ',
  py_modules = ["topsis"],
  package_dir = {'':'TOPSIS-Ria-101803043'},
  package_data={'':['LICENSE.txt']},
  include_package_data=True,
  author="Ria Kapoor",
  author_email="kkapoorria581@gmail.com",
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  long_description=long_description,
  long_description_content_type="text/markdown",
  extras_require={
    "dev":[
        "pytest>=3.7",
    ],
  },
)
