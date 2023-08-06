import os, codecs
from setuptools import setup, find_packages

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

long_description = read('README.md')
setup (
       name='getjobs',
       version='1.0',
       packages = ['getjobs'],
       license='GNUv3.0',
       # Declare your packages' dependencies here, for eg:
       install_requires=[''],
       author='Ronald Rivera',
       author_email='ronaldsoft8423@gmail.com',
       url='https://github.com/ronaldsoft/getjob',
       long_description=long_description,
       long_description_content_type="text/markdown",
       keywords = ['jobs', 'work', 'recruiter'],
       include_package_data=True,
        classifiers=[
          'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Intended Audience :: Developers',      # Define that your audience are developers
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',   # Again, pick a license
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
        ],       
      )