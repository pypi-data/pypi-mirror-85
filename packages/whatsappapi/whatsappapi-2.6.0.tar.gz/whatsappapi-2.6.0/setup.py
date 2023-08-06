from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='whatsappapi',
  version='2.6.0',
  description='A Basic Beta Whatsapp API',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Enzo Barizza Leal',
  author_email='enzobarizza@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='whatsapp', 
  packages=find_packages(),
  install_requires=['selenium']
)
