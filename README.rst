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

Usage example:

./ossi_tool 192.168.10.10 sampleuser -ppassword -i commands.csv -o outputfile.csv

----------
Installation:

You can easily install ossi_tool with pip.
Usage
#pip install ossi_tool
