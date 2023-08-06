
from distutils.core import setup
setup(
  name = 'TOPSIS_Harshit_3_101803010',         # How you named your package folder (MyLib)
  packages = ['TOPSIS_Harshit_3_101803010'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Implementation of TOPSIS',   # Give a short description about your library
  author = 'Harshit singh Guleria',                   # Type in your name
  author_email = 'hguleria_be18@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/Harshit161999/TOPSIS_Harshit_101803010',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Harshit161999/TOPSIS_Harshit_101803010/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
)
