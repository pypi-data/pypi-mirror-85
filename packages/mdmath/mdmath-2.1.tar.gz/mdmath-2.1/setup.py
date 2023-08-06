from distutils.core import setup
setup(
  name = 'mdmath',
  packages = ['mdmath'],
  version = '2.1',
  license='MIT',
  description = 'open source advanced calculator',
  author = 'MyDen',
  author_email = 'myden001002@gmail.com',
  url = 'https://github.com/myden5279/mymath.git',
  download_url = 'https://github.com/myden5279/mymath/archive/v2.0.tar.gz',
  keywords = ['calculator', 'maths', 'mdmath'],
  install_requires=['numpy'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
