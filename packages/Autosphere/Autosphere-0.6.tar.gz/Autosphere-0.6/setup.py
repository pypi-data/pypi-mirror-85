from distutils.core import setup
setup(
  name = 'Autosphere',         # How you named your package folder (MyLib)
  packages = ['Autosphere', 'Autosphere.Word', 'Autosphere.Desktop', 'Autosphere.Email', 'Autosphere.Excel', 'Autosphere.Outlook', 'Autosphere.Robocloud', 'Autosphere.core', 'Autosphere.includes'],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Autosphere skills to build RPA',   # Give a short description about your library
  author = 'Nauman Mahboob',                   # Type in your name
  author_email = 'nauman.mehboob@mercurialminds.com',      # Type in your E-Mail
  url = 'https://mercurialminds.com/',   # Provide either the link to your github or to your website
#   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['RPA', 'Robot', 'Autosphere'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'cryptography>=2.9.2,<3.0.0',
          'exchangelib>=3.1.1,<4.0.0',
          'fpdf>=1.7.2,<2.0.0',
          'graphviz>=0.13.2,<0.14.0',
          'jsonpath-ng>=1.5.2,<2.0.0',
          'mss>=6.0.0,<7.0.0',
          'netsuitesdk>=1.1.0,<2.0.0',
          'notifiers>=1.2.1,<2.0.0',
          'openpyxl>=3.0.3,<4.0.0',
          'pdfminer.six==20201018',
          'pillow>=8.0.1,<9.0.0',
          'pynput>=1.7.0,<2.0.0',
          'pypdf2>=1.26.0,<2.0.0',
          'pyperclip>=1.8.0,<2.0.0',
          'robotframework-pythonlibcore>=2.1.0,<3.0.0',
          'robotframework-requests>=0.6.5,<0.7.0',
          'robotframework-seleniumlibrary>=4.5.0,<5.0.0',
          'robotframework-seleniumtestability>=1.1.0,<2.0.0',
          'robotframework>=3.2.2,<4.0.0',
          'rpaframework-core>=2.1.3,<3.0.0',
          'simple_salesforce>=1.0.0,<2.0.0',
          'tweepy>=3.8.0,<4.0.0',
          'xlrd>=1.2.0,<2.0.0',
          'xlutils>=2.0.0,<3.0.0',
          'xlwt>=1.3.0,<2.0.0'
      ],
  extras_require = \
{':python_version < "3.7.6" and sys_platform == "win32" or python_version > "3.7.6" and python_version < "3.8.1" and sys_platform == "win32" or python_version > "3.8.1" and sys_platform == "win32"': ['pywinauto>=0.6.8,<0.7.0',
                                                                                                                                                                                                        'pywin32>=227,<228'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 ':sys_platform == "linux"': ['evdev>=1.3', 'python-xlib>=0.17'],
 ':sys_platform == "win32"': ['robotframework-sapguilibrary>=1.1,<2.0',
                              'psutil>=5.7.0,<6.0.0'],
 'aws': ['boto3>=1.13.4,<2.0.0'],
 'cv': ['rpaframework-recognition>=0.3.0,<0.4.0'],
 'google': ['google-api-python-client>=1.12.3,<2.0.0',
            'google-auth-httplib2>=0.0.4,<0.0.5',
            'google-auth-oauthlib>=0.4.1,<0.5.0',
            'google-cloud-language>=1.3.0,<2.0.0',
            'google-cloud-speech>=1.3.2,<2.0.0',
            'google-cloud-storage>=1.28.1,<2.0.0',
            'google-cloud-texttospeech>=1.0.1,<2.0.0',
            'google-cloud-translate>=2.0.1,<3.0.0',
            'google-cloud-videointelligence>=1.14.0,<2.0.0',
            'google-cloud-vision>=1.0.0,<2.0.0',
            'grpcio>=1.29.0,<2.0.0']},
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