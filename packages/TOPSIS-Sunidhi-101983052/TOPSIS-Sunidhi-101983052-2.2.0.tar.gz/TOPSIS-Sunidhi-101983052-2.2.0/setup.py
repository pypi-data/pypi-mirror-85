from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README  
setup(
  name = 'TOPSIS-Sunidhi-101983052',         
  packages = ['TOPSIS_Sunidhi_101983052'],
  version = '2.2.0',      
  license='MIT',        
  description = 'A python package to implement TOPSIS on a given dataset',
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'Sunidhi',                   
  author_email = 'ssunidhi1_be18@thapar.edu',  
  url = 'https://github.com/SunidhiSingla/TOPSIS-Sunidhi-101983052',   # Provide either the link to your github or to your website
  install_requires=[          
          "pandas","numpy"
      ],
  include_package_data=True,    
  classifiers=[
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  entry_points={
        "console_scripts": [
            "topsis=TOPSIS_Sunidhi_101983052.topsis:main",
        ]
    },
)