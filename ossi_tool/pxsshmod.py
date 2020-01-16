"""
Modify the original pxssh class, and extend it to
handle new hosr RSA key acceptions prompt.
"""

from pexpect.pxssh import *

class pxsshmod(pxssh):
    """


    """
    def login (self, server, username, password='', terminal_type='ansi',
                original_prompt=r"[#$]", login_timeout=10, port=None,
                auto_prompt_reset=True, ssh_key=None, quiet=True,
                sync_multiplier=1, check_local_ip=True):
        '''This logs the user into the given server.

        It uses
        'original_prompt' to try to find the prompt right after login. When it
        finds the prompt it immediately tries to reset the prompt to something
        more easily matched. The default 'original_prompt' is very optimistic
        and is easily fooled. It's more reliable to try to match the original
        prompt as exactly as possible to prevent false matches by server
        strings such as the "Message Of The Day". On many systems you can
        disable the MOTD on the remote server by creating a zero-length file
        called :file:`~/.hushlogin` on the remote server. If a prompt cannot be found
        then this will not necessarily cause the login to fail. In the case of
        a timeout when looking for the prompt we assume that the original
        prompt was so weird that we could not match it, so we use a few tricks
        to guess when we have reached the prompt. Then we hope for the best and
        blindly try to reset the prompt to something more unique. If that fails
        then login() raises an :class:`ExceptionPxssh` exception.

        In some situations it is not possible or desirable to reset the
        original prompt. In this case, pass ``auto_prompt_reset=False`` to
        inhibit setting the prompt to the UNIQUE_PROMPT. Remember that pxssh
        uses a unique prompt in the :meth:`prompt` method. If the original prompt is
        not reset then this will disable the :meth:`prompt` method unless you
        manually set the :attr:`PROMPT` attribute.
        '''

        ssh_options = ''.join([" -o '%s=%s'" % (o, v) for (o, v) in self.options.items()])
        if quiet:
            ssh_options = ssh_options + ' -q'
        if not check_local_ip:
            ssh_options = ssh_options + " -o'NoHostAuthenticationForLocalhost=yes'"
        if self.force_password:
            ssh_options = ssh_options + ' ' + self.SSH_OPTS
        if port is not None:
            ssh_options = ssh_options + ' -p %s'%(str(port))
        if ssh_key is not None:
            try:
                os.path.isfile(ssh_key)
            except:
                raise ExceptionPxssh('private ssh key does not exist')
            ssh_options = ssh_options + ' -i %s' % (ssh_key)
        cmd = "ssh %s -l %s %s" % (ssh_options, username, server)

        # This does not distinguish between a remote server 'password' prompt
        # and a local ssh 'passphrase' prompt (for unlocking a private key).
        spawn._spawn(self, cmd)
        i = self.expect(["(?i)are you sure you want to continue connec.*", original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT, "(?i)connection closed by remote host", EOF], timeout=login_timeout)

        # First phase
        if i==0:
            # New certificate -- always accept it.
            # This is what you get if SSH does not have the remote host's
            # public key stored in the 'known_hosts' cache.
            self.sendline("yes")
            i = self.expect(["(?i)are you sure you want to continue connec.*", original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        if i==2: # password or passphrase
            self.sendline(password)
            i = self.expect(["(?i)are you sure you want to continue connec.*", original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        if i==4:
            self.sendline(terminal_type)
            i = self.expect(["(?i)are you sure you want to continue connect.*", original_prompt, "(?i)(?:password)|(?:passphrase for key)", "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        if i==7:
            self.close()
            raise ExceptionPxssh('Could not establish connection to host')

        # Second phase
        if i==0:
            # This is weird. This should not happen twice in a row.
            self.close()
            raise ExceptionPxssh('Weird error. Got "are you sure" prompt twice.')
        elif i==1: # can occur if you have a public key pair set to authenticate.
            ### TODO: May NOT be OK if expect() got tricked and matched a false prompt.
            pass
        elif i==2: # password prompt again
            # For incorrect passwords, some ssh servers will
            # ask for the password again, others return 'denied' right away.
            # If we get the password prompt again then this means
            # we didn't get the password right the first time.
            self.close()
            raise ExceptionPxssh('password refused')
        elif i==3: # permission denied -- password was bad.
            self.close()
            raise ExceptionPxssh('permission denied')
        elif i==4: # terminal type again? WTF?
            self.close()
            raise ExceptionPxssh('Weird error. Got "terminal type" prompt twice.')
        elif i==5: # Timeout
            #This is tricky... I presume that we are at the command-line prompt.
            #It may be that the shell prompt was so weird that we couldn't match
            #it. Or it may be that we couldn't log in for some other reason. I
            #can't be sure, but it's safe to guess that we did login because if
            #I presume wrong and we are not logged in then this should be caught
            #later when I try to set the shell prompt.
            pass
        elif i==6: # Connection closed by remote host
            self.close()
            raise ExceptionPxssh('connection closed')
        else: # Unexpected
            self.close()
            raise ExceptionPxssh('unexpected login response')
        if not self.sync_original_prompt(sync_multiplier):
            self.close()
            raise ExceptionPxssh('could not synchronize with original prompt')
        # We appear to be in.
        # set shell prompt to something unique.
        if auto_prompt_reset:
            if not self.set_unique_prompt():
                self.close()
                raise ExceptionPxssh('could not set shell prompt '
                                     '(received: %r, expected: %r).' % (
                                         self.before, self.PROMPT,))
        return True
