from setuptools import setup
import os
f = open('README.md')
long_description = f.read()

setup(
  name = 'ayushbot',         # How you named your package folder (MyLib)
  packages = ['ayushbot'],   # Chose the same as "name"
  version = '0.0.2.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Interfaces mitsuku or kuki chatbot with whatsapp',   # Give a short description about your library
  author = 'Ayush Garg',                   # Type in your name
  author_email = 'themoviechannel77@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ayush4921/ayushbot',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ayush4921/ayushbot/archive/0.0.2.2.tar.gz',    # I explain this later on
  keywords = ['whatsapp','mitsuku','kuki','chatbot'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'beautifulsoup4==4.6.3',
          'lxml==4.6.1',
          'Pillow==7.0.0',
          'requests==2.20.0',
          'selenium==3.12.0',
          'Pillow',
          'chromedriver_autoinstaller'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  long_description=long_description,
  long_description_content_type="text/markdown",
)
