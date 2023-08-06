#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from distutils.core import setup
setup(
  name = 'TOPSIS-AvichalSingh-101803166',         
  packages = ['TOPSIS-AvichalSingh-101803166'],   
  version = '0.1',      
  license='MIT',        
  description = 'My library calculates the score and rank of each row of the given csv file using topsis',   
  author = 'avichal0201',                   
  author_email = 'asachdeva_be18@thapar.edu',      
  url = 'https://github.com/user/avichal0201',   
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    
  keywords = ['COMPREHENSABLE', 'HELPFUL'],   
  install_requires=[            
          'validators',
          'beautifulsoup4',
          'numpy',
          'pandas',
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

