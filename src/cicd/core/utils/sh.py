import os
import signal
import subprocess
from typing import Optional

from cicd.core.logger import logger


class Shell:
    class ExecError(Exception):
        pass

    def run(self, *args, **kwargs) -> Optional[str]:
        if isinstance(args[0], str):
            kwargs['shell'] = True
        if 'check' not in kwargs:
            kwargs['check'] = True
        if 'capture_output' not in kwargs:
            kwargs['capture_output'] = True
        try:
            log_cmd = kwargs.pop('log_cmd', False)
            if log_cmd:
                logger.info(f'$ {args[0]}')
            proc = subprocess.run(*args, **kwargs)
            if kwargs.get('capture_output'):
                return proc.stdout.decode('utf-8').strip()
        except Exception as e:
            raise Shell.ExecError(e)

    def popen(self, *args, **kwargs) -> subprocess.Popen:
        return subprocess.Popen(*args, **kwargs)

    def exec(self, *args, **kwargs):
        timeout = kwargs.pop('timeout', None)
        log_cmd = kwargs.pop('log_cmd', False)
        if isinstance(args[0], str):
            kwargs['shell'] = True
        if log_cmd:
            logger.info(f'$ {args[0]}')
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


sh = Shell()
