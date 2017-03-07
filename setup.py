from setuptools import setup
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('ossi_tool/ossit.py').read(),
    re.M
    ).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


def readme():
    """ Long description from readme file"""
    with open('README.rst') as f:
        return f.read()

setup(name='ossi_tool',
      version=version,
      description='Tool to creact CSV output from Avaya Communcation Manager commands.',
      long_description=long_descr,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Communications :: Telephony',
        ],
      url='https://github.com/deesnow/ossi_tool',
      author='Janos Tarjanyi',
      author_email='janos.tarajnyi@gmail.com',
      license='ISC',
      packages=['ossi_tool'],
      entry_points={
        "console_scripts": ['ossi_tool = ossi_tool.ossit:main']
        },
      install_requires=['pexpect'],
      zip_safe=False)
