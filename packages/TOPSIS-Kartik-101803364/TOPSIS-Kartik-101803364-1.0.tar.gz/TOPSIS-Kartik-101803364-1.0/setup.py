from distutils.core import setup
setup(
  name = 'TOPSIS-Kartik-101803364',        
  packages = ['TOPSIS-Kartik-101803364'],  
  version = '1.0',     
  license='MIT',       
  description = 'Topsis',   
  author = 'Kartik Vasudev',                   
  author_email = 'kvasudev_be18@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Topsis', 'TOPSIS', 'KEYWORDS'],   
  install_requires=[            
          'panda',
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
)