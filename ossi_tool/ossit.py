# -*- coding: utf-8 -*-

from pexpect import pxssh
import getpass
import argparse
# import os
import csv
import re

__version__ = "0.3.3.3"

"""
Handle imput paramaters

"""

parser = argparse.ArgumentParser(description='''My Description. \
        And what a lovely description it is. ''', epilog="""All's well that ends well.""")
parser.add_argument("host", help="Host name or address, where want to connect")
parser.add_argument("username", help="Username for host")
parser.add_argument("-p", "--password", help="Password for host")
parser.add_argument("-i", "--inputfile", help="Input file name (CSV)")
parser.add_argument("-o", "--outputfile", help="Output file name")
parser.add_argument("-v", "--debug", help="Trun ON the debug logging of OSSI terminal. \
                    Debugis loggeg into the debug.log", action='count')
# Planned feature
parser.add_argument("-c", "--command", help="CM command as a string; \
                     eg. <display station xxxx>")
# parser.add_argument("-f", "--fieldID", help="FieldID /what you want t change/")
# parser.add_argument("-d", "--data", help="data for change command")
args = parser.parse_args()

if args.password is not None:
    password = args.password
else:
    password = getpass.getpass('password: ')


class Ossi(object):
    """
    Ossi handler class object

    Init the base object with some default variables.
    """

    def __init__(self):
        """
        Init ossi object

        Init the base object with some default variables.
        """
        self.cmd_error = 0
        self.debug = args.debug
        self.ossi_alive = False

    def ossi_open(self, host, username, password):
        """
        Ssh ession opening, and switch to ossi termnal.

        Open an ssh session to the 'host' with 'username' and 'password'.
        If the password does not provided, than get it with getpass.
        If the connection established, go into SAT with ossi terminal.
        """
        self.host = host
        self.username = username
        self.password = password
        # print self.host, self.username, self.password
        try:
            self.s = pxssh.pxssh(options={"StrictHostKeyChecking": "no"})
            # hostname = raw_input('hostname: ')
            # username = raw_input('username: ')
            # print args.host, args.username, password
            if self.debug is not None:
                self.s.logfile = open("debug.log", "wb")
            try:
                self.s.login(self.host, self.username, self.password, terminal_type='vt100', original_prompt='[#$>t\]]')
                self.s.timeout = 5
                print "--- Connection established ---"
                self.s.sendline('sat')   # run a command
                try:
                    self.s.expect('Terminal Type.*')             # match the prompts
                    self.s.sendline('ossit')
                    try:
                        self.s.expect('t')             # match the prompt
                        print '--- Ossi is logged in and ready ---'
                        self.ossi_alive = self.s.isalive()
                    except Exception as identifier:
                        print 'Did not recognized ossi terminal prompt'
                        self.ossi_alive = False
                except Exception as identifier:
                    print 'Did not recognized prompt for Terminal Type'
                    self.ossi_alive = False
                 
            except Exception as identifier:
                print 'Login failed', self.s.before
                self.ossi_alive = False
            
            
            
                    
            
            
        except pxssh.ExceptionPxssh as self.e:
            print("pxssh failed on login.")
            print(self.e)

    def ossi_close(self):
        """
        Session closing.

        Print how many wrong command were sent to the ossi
        Logging off from ossi, and close the ssh session
        """
        try:
            # print (' - Logging out from ossi - ')
            self.s.sendline('clogoff')
            self.s.sendline('t')
            self.s.expect('Proceed With Logoff.*')
            self.s.sendline('y')
            self.s.prompt()
            # print(s.before)
            self.s.logout()
            print '--- Ossi logged out ---'
            if self.cmd_error is not 0:
                print '*** {0} commands are failed ***'.format(self.cmd_error)
                for self.key in self.failed_cmd:
                    print '{0} --- {1}'.format(self.key, self.failed_cmd[self.key])
                print'*** End of Errors ***'
        except pxssh.ExceptionPxssh as self.e:
            print("pxssh failed on logoff.")
            print(self.e)

    def cmd_parser(self, inputfile):
        """
        It is parsing the 'inputfile' csv file.

        Each line is an ossi command, so it reads line by line, and concatenate with withspace.
        """
        self.inputfile = inputfile
        if self.inputfile is not None:
            try:
                self.info = csv.reader(open(self.inputfile))
                print ' -- {0} is opened --'.format(self.inputfile)
            except:
                print ("Failed to open: ", self.inputfile)
            else:
                for self.row in self.info:
                    # self.row_cmd = ' '.join(self.row)
                    self.cmd = ' '.join(self.row)
                    if len(self.cmd.translate(None, ' \n\t\r')) > 0:
                        print '-------- \n\r{0}\n\r--------'.format(self.cmd)
                        self.output_writer('-------- \n{0}\n--------\n'.format(self.cmd))
                        self.ossi_cmd(self.cmd)

    def ossi_prompt(self, timeout=-1):

        
    
        if timeout == -1:
            timeout = self.timeout
        try:
            i = self.s.expect(['\rmore..y.'], timeout=timeout)
            return True
        except Exception as e:
            #print (e)
            return False
                  
       
    def ossi_cmd(self, command):
        """
        Send 'command' to ossi terminal, and read the output.

        It gets the command as a string object. The command output is read page by page and passed as an object to 'data_parse'.
        The result is printed out, and writen into the output file if it is defined.
        """
        self.command = command
        if self.command is not None:
            self.cmd_raw_result = ""
            self.cmd_result = ""
            self.failed_cmd = {}
            self.s.sendline('c'+self.command)
            self.s.sendline('t')

            if self.ossi_prompt(2):
                self.index = 0
                while self.index == 0:
    
                    self.cmd_raw_result += self.s.before
                    self.s.sendline('y')
                        

                    if self.ossi_prompt(2):
                        pass
                    else:
                        self.index = self.s.expect(['####fake', '\rd\r\n\rt\r\n\r', '\rd*t\r\n\r'])
                        self.cmd_raw_result += self.s.before
           
                

            else:
                self.index = self.s.expect(['\rmore..y.', 'e1.*', 'f.*'])
                if self.index == 1:
                    print '-- Command Error --'
                    self.cmd_error += 1
                    self.failed_cmd[str(self.command)] = self.s.after
                elif self.index == 2:
                    self.cmd_raw_result += self.s.after
            

            #Call command output parser
            self.cmd_result = self.data_parse(self.cmd_raw_result)
                
            # print '---- last data ---'

                
            self.output_writer(self.cmd_result)
            self.output_writer('\n')
            
                     


    def data_parse(self, data):
        """
        Parsing the ossi commnad page 'data', and retun its back.

        Parsing only the dxxxxxx fields from the output. Values are comma separated.
        """
        self.data = data
        self.page_data = ""
        self.fields = 0
        self.new_record = True
        
        self.lines = self.data.split('\n')

        for self.line in self.lines:
            self.line = self.line.lstrip().rstrip()
            if re.match('^f', self.line):
                self.fields = self.line.count('\t') + 1
                
            elif re.match('^e', self.line):
                self.result = self.line.lstrip('e')
                self.page_data += self.result
                

            elif re.match('^d', self.line):
                self.result = self.line.lstrip('d')
                if len(self.result) is not 0:
                    if len(self.page_data) > 0:
                        if self.new_record is False:
                            self.page_data +=  ','
                        self.page_data += re.sub('\t', ',', self.result)
                        self.new_record = False
                    else:
                        self.page_data += re.sub('\t', ',', self.result)
                        self.new_record = False
            elif re.match('^n', self.line):
                self.page_data += "\n"
                self.new_record = True
            
  
            
            

        # print '*** page data ***'
        # print ''.join(page_data)
        print self.page_data
        return self.page_data

    
    def output_writer(self, output):
        """
        Write 'output' object into the outputfile.

        If the outputfile is not defined than only print output to the screen.
        """
        self.outputfile = args.outputfile
        self.output = output
        if self.outputfile is not None:
            # print self.output
            try:
                with open(self.outputfile, 'a+') as self.f:
                    self.f.write(self.output)
            except:
                print ("Failed to open: ", self.outputfile)


def main():
    """
    Main modul of ossi script.

    Bring things together.
    """
    print '--- Let Start! ---'
    a = Ossi()
    if args.password is not None:
        password = args.password
    else:
        password = getpass.getpass('password: ')
    a.ossi_open(args.host, args.username, password)
    # print args.inputfile
    # print a.cmd_parser(args.inputfile)

    if a.ossi_alive is True:
        if args.inputfile is not None and args.command is None:
            a.cmd_parser(args.inputfile)
            
        elif args.inputfile is None and args.command is not None:
            print '-------- \n\r{0}\n\r--------'.format(args.command)
            a.output_writer('-------- \n{0}\n--------\n'.format(args.command))
            a.ossi_cmd(args.command)
            
        else:
            print('There is neither an input csv file neither a command to execute')
    a.ossi_close()
    print '--- Script running is finished ---'
