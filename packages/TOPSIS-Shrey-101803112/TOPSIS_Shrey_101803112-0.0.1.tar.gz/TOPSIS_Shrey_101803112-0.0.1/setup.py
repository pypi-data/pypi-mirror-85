from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TOPSIS_Shrey_101803112',
  version='0.0.1',
  description='Topsis_Assignment',
  url='',  
  author='Shrey Shourya',
  author_email='sshourya_be18@thapar.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='Topsis_Score', 
  packages=find_packages(),
  install_requires=['pandas','numpy','time','copy'] 
)