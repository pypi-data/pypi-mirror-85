from distutils.core import setup
setup(
  name = 'pipmate',
  packages = ['src/pipmate'],
  version = '0.1.0',
  license='MIT',
  description = 'Move between pipfiles, pyproject.toml and requirements.txt with ease!',
  author = 'Srujan Deshpande',
  author_email = 'srujan.deshpande@gmail.com',
  url = 'https://github.com/srujandeshpande/pipmate',
  download_url = 'https://github.com/srujandeshpande/pipmate/releases/tag/v0.1.0',
  keywords = ['Poetry', 'PyPip', 'Dependencies'],
  install_requires=[
          'cleo',
          'toml',
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
