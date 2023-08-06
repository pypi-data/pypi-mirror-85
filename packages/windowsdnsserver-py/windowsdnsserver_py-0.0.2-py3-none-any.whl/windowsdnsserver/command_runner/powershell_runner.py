import subprocess
import sys

from .runner import Command, CommandRunner, Result
from ..util import logger


DEFAULT_POWER_SHELL_EXE_PATH = "C:\Windows\syswow64\WindowsPowerShell\\v1.0\powershell.exe"


class PowerShellCommand(Command):

    def __init__(self, cmdlet: str, *flags, **args):
        super().__init__()

        self.cmdlet = cmdlet
        self.flags = flags
        self.args = args

    def build(self):
        cmd = [self.cmdlet]

        # add flags, ie -Force
        for flag in self.flags:
            cmd.append('-%s' % flag)

        # add arguments
        for arg, value in self.args.items():
            cmd.append('-%s %s' % (arg, value))

        # convert to json to make machine readable
        cmd.append('|')
        cmd.append('ConvertTo-Json')

        return cmd


class PowerShellRunner(CommandRunner):

    def __init__(self, power_shell_path: str = None):
        self.logger = logger.create_logger("PowerShellRunner")

        self.power_shell_path = power_shell_path
        if power_shell_path is None:
            self.power_shell_path = DEFAULT_POWER_SHELL_EXE_PATH

    def run(self, command: PowerShellCommand) -> Result:
        assert isinstance(command, PowerShellCommand)

        cmd = command.build()
        cmd.insert(0, self.power_shell_path)

        self.logger.debug("Running: [%s]" % ' '.join(cmd))

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = proc.communicate(timeout=60)
        except:
            proc.kill()
            out, err = proc.communicate()
        finally:
            pass

        self.logger.debug('using default encoding: [%s]' % sys.stdout.encoding)

        out = out.decode(sys.stdout.encoding, 'replace')
        err = err.decode(sys.stdout.encoding, 'replace')

        self.logger.debug("Returned: \n\tout:[%s], \n\terr:[%s]" % (out, err))

        success = proc.returncode == 0
        return Result(success, proc.returncode, out, err)



