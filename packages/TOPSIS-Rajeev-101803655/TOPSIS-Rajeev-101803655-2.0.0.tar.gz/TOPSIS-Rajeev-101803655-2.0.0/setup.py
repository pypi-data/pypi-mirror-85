from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README  
setup(
  name = 'TOPSIS-Rajeev-101803655',         
  packages = ['topsis_101803655'],
  version = '2.0.0',      
  license='MIT',        
  description = 'A python package to implement TOPSIS on a given dataset',
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'RAJEEV SINGLA',                   
  author_email = 'rsingla1_be18@thapar.edu',  
  url = 'https://github.com/rajeevsingla780/TOPSIS-Rajeev-101803655',   # Provide either the link to your github or to your website
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
            "topsis=topsis_101803655.topsis_raj:main",
        ]
    },
)