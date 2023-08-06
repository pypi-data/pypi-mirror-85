from setuptools import setup

def readme():
    with open("README.md",encoding="utf-8") as f:
        README = f.read() 
    return README


setup(
  name = 'TOPSIS-Aryan-101803035',         
  packages = ['TOPSIS-Aryan-101803035'],   
  version = '0.0.2',      
  license='MIT',      
  description = 'A Python package in which TOPSIS technique is implemented.',   
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'Aryan',                  
  author_email = 'ayadav_be18@thapar.edu',      
  url = 'https://github.com/justgoofingaround/TOPSIS',   
  install_requires=[           
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  entry_points={
        "console_scripts": [
            "topsis=topsis_python.topsis:main",
        ]
    }
)