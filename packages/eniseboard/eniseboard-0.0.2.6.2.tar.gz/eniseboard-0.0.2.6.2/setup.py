#import setuptools
from distutils.core import setup
setup(
      name = 'eniseboard',
      packages = ['eniseboard','eniseboard.demos'],
      package_data = {'eniseboard.demos': ['taquinimages/*','taquinimages/sources/*','penguinimage/*']},
      version = '0.0.2.6.2',
      description = 'A lib for making board games',
      author = 'BagEddy42',
      author_email = 'edouard.vidal@enise.fr',
      keywords = ['game', 'board'], # arbitrary keywords
      install_requires=[
          'pillow',
          'enisenet',
      ],
      classifiers = [],
)
