import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
  name = 'TOPSIS-Karanbir-101803235',
  packages=setuptools.find_packages(),   
  version = '0.1',      
  license='MIT',        
  description = 'topsis marking for dataset to be ranked according to topsis analysis',   
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Karanbir singh',                  
  author_email = 'karanchopra21061999@gmail.com',   
  keywords = ['TOPSIS'],  
  install_requires=[           
          'pandas'
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
)
