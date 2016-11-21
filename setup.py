from setuptools import setup, find_packages

version = '0.0.1dev'


install_requires = [
    'pytest-splinter',
    'tox',
    'pytest-cov',
    'mock',
    'PyPOM[splinter]>=1.1.1',
    'colander',
]

docs_require = [
    'Sphinx',
    'sphinx_rtd_theme',
    ]

setup(name='pypom_form',
      version=version,
      description="pypom_form",
      long_description=open("README.rst").read() + "\n" +
      open("CHANGES.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pytest",
          "Topic :: Software Development :: Testing",
          "License :: OSI Approved :: Apache Software License",
          ],
      keywords='',
      author='Tierra QA Team',
      author_email='DLQA@tierratelematics.com',
      url='http://tierratelematics.com',
      license='Apache License, Version 2.0',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      """,
      extras_require={
          'docs': docs_require,
          },
      )
