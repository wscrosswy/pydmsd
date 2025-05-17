from setuptools import setup

setup(name='PyDMSD',
      version='1.0',
      description='Python App for Analyzing Semantic Data Models',
      author='Spencer Crosswy',
      author_email='spencer.crosswy@gmail.com',
      url='https://www.github.com/wscrosswy',
      packages=['pydmsd'],
      python_requires=">=3.9",
      entry_points={"console_scripts": ["pydmsd=pydmsd.main:main"]}
     )