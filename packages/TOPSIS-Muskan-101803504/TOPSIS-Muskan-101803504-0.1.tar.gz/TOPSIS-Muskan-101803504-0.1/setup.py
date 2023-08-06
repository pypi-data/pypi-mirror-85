from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README  
setup(
  name = 'TOPSIS-Muskan-101803504',         
  packages = ['Topsis_Muskan'],
  version = '0.1',      
  license='MIT',        
  description = 'A python package to implement TOPSIS on a given dataset',
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'Muskan Gupta',                   
  author_email = 'mgupta2_be18@thapar.edu',  
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
            "topsis=Topsis_Muskan.Topsis:main",
        ]
    },
)