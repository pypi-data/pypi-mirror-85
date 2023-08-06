from distutils.core import setup

setup(
  name = 'TOPSIS_Bibekpreet_101803272', 
  packages = ['TOPSIS_Bibekpreet_101803272'], 
  version = '1.0.0',  
  license='MIT', 
  description = 'Topsis score calculator',
  long_description=open("README.txt").read(),
  author = 'Bibekpreet Singh',               
  author_email = 'bsingh3_be18@thapar.edu', 
  url = 'https://https://github.com/bibekpreet99/TOPSIS-Bibekpreet-101803272',
  download_url = 'https://github.com/bibekpreet99/TOPSIS-Bibekpreet-101803272/archive/v_1.0.0.tar.gz', 
  keywords = ['topsis', 'thapar', 'rank', 'topsis score'], 
  install_requires=["pandas"],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)