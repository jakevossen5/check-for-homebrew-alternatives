from setuptools import setup

setup(
   name='omnifocus-graph-creator',
   version='1.0.0',
   description='Searches for homebrew versions of apps installed from other sources',
   author='Jake Vossen',
   scripts=['bin/check-for-homebrew-alternatives'],
   author_email='jake@vossen.dev',
   packages=[],  #same as name
   install_requires=[], #external packages as dependencies
)
