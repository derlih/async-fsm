#!/usr/bin/env python

from distutils.core import setup

setup(name='async-fsm',
      version='0.1',
      description='Python FSM implementation that supports asyncio',
      author='Dmitry Erlikh',
      author_email='derlih@gmail.com',
      url='https://github.com/derlih/async-fsm',
      packages=['async_fsm'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Libraries',
          'Framework :: AsyncIO',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'pytest-asyncio', 'pytest-cov']
      )
