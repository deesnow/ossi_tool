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
or
#ossi_tool 192.168.10.10 sampleuser -ppassword -c 'list node-name all'

---------------------
Installation (Linux):
---------------------

In most Linux distribution the Python 2.7 is installed.

Ossi_tool can be easily installed by pip, it takes care about other prerequisits.
    - Check python version
    - Install pip           
    - Install ossi_tool

$ sudo easy_install-2.7 pip
$ sudo pip install ossi_tool

ossi_tool is ready to use ;)

------------------------
Installation (Windows):
------------------------

Because the ossi tool use pexpect wich is not compatible with Windows Powershell SSH client,
on Windows Linux Subsystem (WLS) should be used. You can chose many linux disctribution as
subsystem.
https://docs.microsoft.com/en-us/windows/wsl/install-win10
When the WLS is ready to use all other step same like Linux usage.
    - Install Python (maybe not necessary)
    - Install pip
    - Install ossi_tool     

$ sudo easy_install-2.7 pip
$ sudo pip install ossi_tool

ossi_tool is ready to use ;)

---------------------
Known issues
---------------------

- 
