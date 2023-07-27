import os
import shlex
import signal
import subprocess
import typing as t

from cicd.core.logger import logger


class Shell:
    class ExecError(Exception):
        pass

    def popen(self, *args, **kwargs) -> subprocess.Popen:
        return subprocess.Popen(*args, **kwargs)

    def exec(self, *args, **kwargs):
        timeout = kwargs.pop('timeout', None)
        log_cmd = kwargs.pop('log_cmd', False)
        if isinstance(args[0], str):
            kwargs['shell'] = True
        if log_cmd:
            logger.info(f'$ {args[0]}')

        if kwargs.pop('capture_output', True):
            kwargs['stdout'] = subprocess.PIPE
            kwargs['stderr'] = subprocess.PIPE

        proc = self.popen(*args, **kwargs)
        try:
            output, err = proc.communicate(timeout=timeout)
            if proc.returncode != 0:
                raise Shell.ExecError(
                    'Command failed with code {}: {}. Error: {}'.format(
                        proc.returncode,
                        args,
                        err.decode('utf-8').strip() if err else None,
                    )
                )
            return output.decode('utf-8').strip() if output else None
        except (subprocess.TimeoutExpired, TimeoutError) as e:
            # Clean up process group. For some long-running (shell) commands such as `xcodebuild foo | bar`,
            # the child processes are not getting cleaned up properly.
            # --> Kill the process group to clean up them all.
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            raise e

    def quote(self, s) -> t.Optional[str]:
        return shlex.quote(str(s)) if s is not None else None


sh = Shell()
