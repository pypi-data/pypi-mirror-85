from distutils.core import setup
setup(
  name = 'TOPSIS-Aneesh-101853025',         
  packages = ['TOPSIS-Aneesh-101853025'],   
  version = '0.1',      
  license='MIT',        
  description = 'Python Library containing classes and code for implementing TOPSIS on a given dataset',   
  author = 'Aneesh Jindal',                   
  author_email = 'aneeshjindal811@gmail.com',      
  url = 'https://github.com/aj8101/TOPSIS-Aneesh-101853025',   
  download_url = 'https://github.com/aj8101/TOPSIS-Aneesh-101853025/archive/0.1.tar.gz',    
  keywords = ['TOPSIS', 'PYTHON', 'DATASET'],   
  install_requires=[            
          'numpy',
          'pandas',
          'sys',
          'math',
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