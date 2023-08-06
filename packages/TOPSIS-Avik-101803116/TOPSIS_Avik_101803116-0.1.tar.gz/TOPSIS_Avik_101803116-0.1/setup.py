from distutils.core import setup
setup(
  name = 'TOPSIS_Avik_101803116',         # How you named your package folder (MyLib)
  packages = ['TOPSIS_Avik_101803116'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='APACHE 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Implementation of TOPSIS',   # Give a short description about your library
  author = 'Avik Kuthiala',                   # Type in your name
  author_email = 'avikkuthiala@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/bernard0047/topsis-avik',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/bernard0047/topsis-avik/archive/V0.1.tar.gz',    # I explain this later on
  keywords = ['implementation', 'topsis', 'datascience'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'math',
          'sys',
          'pandas',
          'copy',
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