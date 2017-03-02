from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ossi_tool',
      version='0.1',
      description='Tool to creact CSV output from Avaya Communcation Manager commands. \
                    Commands are listed in an input csv',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Communications :: Telephony',
        ],
      url='https://github.com/deesnow/ossi_tool',
      author='DeeSnow',
      author_email='janos.tarajnyi@gmail.com',
      license='ISC',
      packages=['ossi_tool'],
      install_requires=['pexpect'],
      zip_safe=False)
