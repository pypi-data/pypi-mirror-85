from setuptools import setup, find_packages

with open('README.md') as f:
    long_description_from_readme = f.read()

setup(name='knilb',
      #  version='', see setup.cfg [metadata]
      author='nko',
      author_email='nate@knilb.com',
      description='Example implementation of an Agent for Knilb',
      long_description=long_description_from_readme,
      long_description_content_type="text/markdown",      
      url='http://knilb.com',
      packages=find_packages(exclude=["deprecated"]),
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.8'],
      install_requires=['requests', 'responses', 'six'],
      entry_points={'console_scripts': ['knilb=knilb.__main__:main']},
      include_package_data=True,
      zip_safe=False,
      license='MIT')
