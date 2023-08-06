from distutils.core import setup

setup(
  name = 'wattson',
  packages = ['wattson'],
  version = '0.0.1',
  license='MIT',
  description = 'Wattson - Power Grid Training and Research Environment',
  author = 'Fraunhofer FKIE, Dept. CA&D',
  author_email = 'lennart.bader@fkie.fraunhofer.de',
  url = 'https://github.com/lennart-bader/wattson',
  download_url = 'https://github.com/lennart-bader/wattson/archive/v0.0.1.tar.gz',
  keywords = ['Cybersecurity', 'Research', 'Simulation', 'Power Grid'],
  install_requires = [],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
