
from distutils.core import setup
setup(
  name = 'Py-Electron',         # How you named your package folder (MyLib)
  packages = ['Py-Electron'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='GNU-GPL',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library for making Electron-like applications in Python',   # Give a short description about your library
  author = 'Lasal M',                   # Type in your name
  author_email = 'lasal2014m@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/LasalM/Py-Electron',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/LasalM/Py-Electron/archive/0.0.1.tar.gz',    # I explain this later on
  keywords = ['Electron', 'GUI', 'Application'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Flask',
          'websocket_client',
          'requests_futures',
          'requests'
      ],
  classifiers=[
    'Programming Language :: Python :: 3.6',
  ],
)
