from distutils.core import setup

setup(
  name = 'TOPSIS_Tannishtha_101803201', 
  packages = ['TOPSIS_Tannishtha_101803201'], 
  version = '1.0',  
  license='MIT', 
  description = 'Topsis score calculator',
  long_description=open("README.md").read(),
  author = 'episkey24',               
  author_email = 'ttannishtha_be18@thapar.edu', 
  url = 'https://github.com/episkey24/TOPSIS_Tannishtha_101803201',
  download_url = 'https://github.com/episkey24/TOPSIS_Tannishtha_101803201/archive/v1.0.tar.gz', 
  keywords = ['topsis', 'thapar', 'rank', 'topsis score'], 
  install_requires=["pandas"],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)