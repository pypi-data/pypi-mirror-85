from distutils.core import setup
setup(
  name = 'Rahul Mahajan',         
  packages = ['Topsis-Rahul-101803526'],  
  version = '0.1',     
  license='MIT',       
  description = 'Topsis project evaluation',   
  author = 'Rahul Mahajan',                   # Type in your name
  author_email = 'rmahajan1_be18@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/rahulmahajan01/Topsis/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/rahulmahajan01/Topsis/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['TOPSIS','IMPLEMENTATION','PYTHON'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
  ],
)