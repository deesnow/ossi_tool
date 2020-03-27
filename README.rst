ossi_tool
=========
**Author:** `Janos Tarjanyi`_

.. _Janos Tarjanyi: janos.tarjanyi@gmail.com




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

    - $ ossi_tool 192.168.10.10 sampleuser -ppassword -i commands.csv -o outputfile.csv

    - $ ossi_tool 192.168.10.10 sampleuser -ppassword -c 'list node-name all'


Installation (Linux):
---------------------

In most Linux distribution the Python 2.7 is installed.

Ossi_tool can be easily installed by pip, it takes care about other dependecies.
    - Check python version
    - `Install pip`_
        - $ sudo easy_install-2.7 pip

    .. _Install pip: https://www.tecmint.com/install-pip-in-linux/           
    
    - Install ossi_tool

        - $ sudo pip install ossi_tool

ossi_tool is ready to use ;)


Installation (Windows):
------------------------

Because the ossi tool use pexpect wich is not compatible with Windows Powershell SSH client,
Linux Subsystem (WLS) should be used on Windows. You can chose many linux disctribution as
subsystem. `How_to_install_WLS`_ 

.. _How_to_install_WLS: https://docs.microsoft.com/en-us/windows/wsl/install-win10

When the WLS is ready to use all other step same like Linux usage.
    - Check python version
    - `Install pip`_
        - $ sudo easy_install-2.7 pip
        
    .. _Install pip: https://www.tecmint.com/install-pip-in-linux/           
    
    - Install ossi_tool

        - $ sudo pip install ossi_tool    

ossi_tool is ready to use ;)

Supported SAT commands
----------------------
- display
- list
- mon

*Note:
ossi_tool focuses those commands which are not scriptable by Avaya Site
Administration. With SAT export/import many change type commands can be achived
so it will not be part of the ossi_tool. If you have idea what command should include
drop me an* `E-mail`_ to discuss it.

.. _E-mail: janos.tarjanyi@gmail.com





Known issues
---------------------

Check the project `GitHub page`_

.. _GitHub page: https://github.com/deesnow/ossi_tool/issues
