from distutils.core import setup
setup(
  name = 'TOPSIS-Karan-101803135',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-Karan-101803135'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A python package for Multiple Criteria Decision Making (MCDM) using Topsis',   # Give a short description about your library
  author = 'Karan Goyal',                   # Type in your name
  author_email = 'karandps7@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/karangoyal7/TOPSIS-Karan-101803135',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/karangoyal7/TOPSIS-Karan-101803135/archive/v0.2.tar.gz',    # I explain this later on
  keywords = ['TOPSIS', '101803135', 'Karan Goyal'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
