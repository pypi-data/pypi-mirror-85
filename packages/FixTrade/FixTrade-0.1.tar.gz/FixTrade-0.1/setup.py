from distutils.core import setup
setup(
  name = 'FixTrade',
  packages = ['FixTrade'],   # Chose the same as "name"
  version = '0.1',
  license='MIT',
  description = 'Fix Protocol Client and Server for Test Trading',
  author = 'Raj Gupta',                   # Type in your name
  author_email = 'raazgupta@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/raazgupta/Fix_Trade',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/raazgupta/Fix_Trade/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['FIX', 'TRADE', 'TEST', 'CLIENT', 'SERVER'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)