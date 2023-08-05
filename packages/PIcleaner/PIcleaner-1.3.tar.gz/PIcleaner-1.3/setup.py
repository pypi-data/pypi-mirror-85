from setuptools import setup

setup(name='PIcleaner',
      version='1.3',
      description='Clean the dirty things in our lovely data.',
      url='',
      author='Martin Kirilov, Dung Le (Eric)',
      author_email='martin.kirilov@pandoraintelligence.com, dung.le@pandoraintelligence.com',
      license='Pandora Intelligence',
      packages=['PIcleaner'],
      install_requires=[
          'clean-text[gpl]',
          'lxml'
      ],
      zip_safe=False)