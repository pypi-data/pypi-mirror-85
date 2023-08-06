"""
Setup script for PuLP-MiA (PuLP Multi-index Addon)
"""
from setuptools import setup

import pulp_mia

readme_file = 'README.rst'
Description = open(readme_file).read()

with open(readme_file, "r") as fh:
    long_description = fh.read()

setup(name="PuLP_MiA",
      version=pulp_mia.__version__,
      description="Multi-index Addon for PuLP",
      long_description = long_description,
      long_description_content_type = "text/x-rst",
      keywords = ["Optimization", "Linear Programming", "Operations Research"],
      author=pulp_mia.__author__,
      author_email=pulp_mia.__email__,
      url="https://github.com/Palich239/PuLP-MiA",
      py_modules=['pulp_mia'],
      scripts=['pulp_mia.py'],
      license='MIT',
      platforms = 'any',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Intended Audience :: Science/Research',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Natural Language :: Russian',
                     'Programming Language :: Python',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Scientific/Engineering :: Mathematics',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: 3.9',
      ],
      install_requires = ['pulp>=1.6.10', 'amply>=0.1.2'],
)
