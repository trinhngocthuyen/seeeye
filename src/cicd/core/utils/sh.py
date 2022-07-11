import subprocess
from typing import Optional


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
            proc = subprocess.run(*args, **kwargs)
            if kwargs.get('capture_output'):
                return proc.stdout.decode('utf-8').strip()
        except Exception as e:
            raise Shell.ExecError(e)


sh = Shell()
