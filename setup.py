from setuptools import setup

setup(name='ossi_tool',
      version='0.1',
      description='Tool to creact CSV output from Avaya Communcation Manager commands. \
                    Commands are listed in an input csv',
      url='https://github.com/deesnow/ossi_tool',
      author='DeeSnow',
      author_email='janos.tarajnyi@gmail.com',
      license='ISC',
      packages=['ossi_tool'],
      install_requires=['pexpect'],
      zip_safe=False)
