
from distutils.core import setup
setup(
  name = 'TOPSIS_Mehak_101983062',         # How you named your package folder (MyLib)
  packages = ['TOPSIS_Mehak_101983062'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package allows you to run topsis on your dataset for Multiple Attribute Decision Making(MADM)',   # Give a short description about your library
  author = 'Mehak',                   # Type in your name
  author_email = 'mgarg3_be18@thapar.edu',      # Type in your E-Mail
  keywords = ['TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
