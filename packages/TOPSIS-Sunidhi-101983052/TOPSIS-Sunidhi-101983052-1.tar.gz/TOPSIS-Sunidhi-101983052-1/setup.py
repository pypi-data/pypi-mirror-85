from distutils.core  import setup
def readme():
    
    with open('README.md') as f:
        README = f.read()
    return README
setup(

  name = 'TOPSIS-Sunidhi-101983052',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-Sunidhi-101983052'],   # Chose the same as "name"
  version = '1',      # Start with a small number and increase it with every change you make
  license ='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Topsis and Rank',   # Give a short description about your library
  author = 'Sunidhi',                   # Type in your name
  author_email = 'sunidhisingla21@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/SunidhiSingla/TOPSIS-Sunidhi-101983052',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/SunidhiSingla/TOPSIS-Sunidhi-101983052/archive/1.tar.gz',    # I explain this later on
  
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy'
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
  ],)
long_description=readme(),
long_description_content_type="text/markdown",
entry_points={"console_scripts":["topsis=TOPSIS-Sunidhi-101983052.topsis:main"]}

