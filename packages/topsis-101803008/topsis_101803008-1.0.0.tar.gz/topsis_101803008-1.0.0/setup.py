from distutils.core import setup

setup(
  name = 'topsis_101803008', 
  packages = ['topsis_101803008'], 
  version = '1.0.0',  
  license='MIT', 
  #description = 'Topsis score calculator',
  #long_description=open("README.txt").read(),
  author = 'Sarthak Dhingra',               
  author_email = 'sdhingra_be18@thapar.edu', 
  url = 'https://github.com/sarthakdhingra-101803008/topsis_101803008',
  download_url = 'https://github.com/sarthakdhingra-101803008/topsis_101803008/archive/v_01.tar.gz', 
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
