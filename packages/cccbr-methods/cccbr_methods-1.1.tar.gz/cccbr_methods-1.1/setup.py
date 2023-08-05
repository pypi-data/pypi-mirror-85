from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='cccbr_methods',
      version='1.1',
      description='A Pythonic interface to the CCCBR Methods Library',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='http://github.com/lelandpaul/cccbr_methods',
      author='Leland Paul Kusmer',
      author_email='me@lelandpaul.com',
      license='MIT',
      packages=['cccbr_methods'],
      package_data={'cccbr_methods': ['data/*']},
      install_requires=[
          'bs4',
          'sqlalchemy',
          'lxml',
      ],
      entry_points = {
          'console_scripts': ['update-cccbr-methods=cccbr_methods.update:update_database'],
      },
      include_package_data=True,
      zip_safe=False)
