from setuptools import setup
setup(
  name = 'TOPSIS-ANMOL-101803669',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-ANMOL-101803669'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'THIS PACKAGE IS TO IMPLEMENT TOPSIS',   # Give a short description about your library
  author = 'ANMOL JINDAL',                   # Type in your name
  author_email = 'ajindal4_be18@thapar.edu',      # Type in your E-Mail
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
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