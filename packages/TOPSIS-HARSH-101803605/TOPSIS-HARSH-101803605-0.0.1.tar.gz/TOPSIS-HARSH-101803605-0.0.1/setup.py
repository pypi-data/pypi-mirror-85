from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
  name = 'TOPSIS-HARSH-101803605',
  version = '0.0.1',
  description = 'Find the Topsis Score Easily',
  py_modules = ["topsis"],
  package_dir = {'':'TOPSIS-HARSH-101803605'},
  package_data={'':['LICENSE.txt']},
  include_package_data=True,
  author="Harsh Garg",
  author_email="harshgarg4842@gmail.com",
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
