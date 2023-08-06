from distutils.core import setup
from os import path


setup(
  name = 'TelegramBotInterface',         # How you named your package folder (MyLib)
  packages = ['TelegramBotInterface'],   # Chose the same as "name"
  version = '3.0',                # Start with a small number and increase it with every change you make
  license='GPL-3.0-only',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This a module who is work like an interface to telegram bot API',   # Give a short description about your library
  long_description = 'All Docs on https://github.com/emaaForlin/TelegramBotInterface',
  long_description_content_type = 'text/markdown',
  author = 'Emanuel Forlin',                   # Type in your name
  author_email = 'emaforlin@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/emaaForlin/TelegramBotInterface',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/emaaForlin/TelegramBotInterface/archive/v0.3.tar.gz',    # I explain this later on
  keywords = ['API', 'BOT', 'TELEGRAM', 'INTERFACE'],   # Keywords that define your package best
  install_requires=['requests'],            # I get to this in a second
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support'
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
    ],
)
