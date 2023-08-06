from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TOPSIS_KaranAggarwal_101983065',
  version='1.0.1',
  description='Topsis_Assignment',
  url='',  
  author='Karan Aggarwal',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='Topsis_Score', 
  packages=find_packages(),
  install_requires=['pandas','numpy','time','copy'] 
)