from distutils.core import setup

setup(
  name = 'TOPSIS_Shivam_101803315',
  packages = ['TOPSIS_Shivam_101803315'],
  version = '1.0.1',
  license='MIT', 
  description = 'Topsis score calculator',
  long_description=open("README.txt").read(),
  author = 'Shivam Sikri',
  author_email = 'shivamsikri99@gmail.com',
  url = 'https://github.com/shivamsikri99/TOPSIS_Shivam_101803315',
  download_url = 'https://github.com/shivamsikri99/TOPSIS_Shivam_101803315/archive/v1.tar.gz',
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