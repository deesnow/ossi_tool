ossi_tool
-------------------------

It is a Python script, to execute multiple commands on Avaya Communication Manager,
and write output data into the CSV file for later processing. It is ideal tool to
repeat a command many times which not available as import in Avaya Site Administration
Tool (eg. list usage)

As input arguments need to define the followings:
    - host
    - Username
    - Password
    - Input file
    - Output file

For all available option use "ossi_tool -h" 

Usage example:

#ossi_tool 192.168.10.10 sampleuser -ppassword -i commands.csv -o outputfile.csv

---------------------
Installation (Linux):
---------------------

You can easily install ossi_tool with pip. It takes care about the prerequisits.
Usage
#pip install ossi_tool

------------------------
Installation (Windows):
------------------------

Due to lack of ssh on windows command line, a good alternative to use Cygwin to get linux like
shell on windows machine. Download it from here:
https://www.cygwin.com/
Run the installer, and at the package selection add the python, and python-setuptools.
If the cygwin is ready to use, open the cygwin terminal, and install pip, and finally the ossi_tool
$  easy_install-2.7 pip
$ pip install ossi_tool

ossi_tool is ready to use ;)

---------------------
Known issues
---------------------

- If the RSA key of the host where want to connect not in the .ssh/known_hosts file, than it drops an exception.
    Workaround:
    ssh to the host with regular ssh and accept the RSA key.
