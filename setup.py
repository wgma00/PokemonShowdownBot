from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='PokemonShowdownBot',
      version='1.0',
      description='PokemonShowdown chatbot',
      long_description=readme(),
      classifiers=[
        'License :: OSI Approved :: GPLv3',
        'Programming Language :: Python :: 3.4+',
        'Topic :: Chat Bot',
      ],
      keywords='chatbot latex chatgames ',
      url='http://github.com/wgma00/PokemonShowdownBot',
      author='William Granados',
      author_email='me@wgma00.me',
      license='GPLv3',
      packages=['venv'],
      platforms=['deb', 'rpm'],
      install_requires=[
          'PyYAML',
          'websocket',
          'requests',
          'simplejson', 
          'websocket-client', 
          'pylatex',
          'pyimgur', 
          'markdown',
          'pytest'
      ],
      include_package_data=True,
      zip_safe=False)
