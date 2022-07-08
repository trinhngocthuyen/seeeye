import subprocess
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from cicd.core.syntax.json import JSON


class XCResultTool:
    def exec(
        self,
        cmd: str,
        cmd_args: Optional[List[str]] = None,
        cmd_kwargs: Optional[Dict[str, Any]] = None,
        to_json=False,
    ) -> Union[JSON, str]:
        if cmd_args is None:
            cmd_args = []
        if cmd_kwargs is None:
            cmd_kwargs = {}
        args = ['xcrun', 'xcresulttool', cmd]
        args += [x for (k, v) in cmd_kwargs.items() for x in [f'--{k}', v]]
        args += cmd_args
        proc = subprocess.run(args, check=True, stdout=subprocess.PIPE)
        output = proc.stdout.decode('utf-8')
        if to_json:
            output = JSON.from_str(output)
        return output

    def get(
        self, path: Union[str, Path], id: Optional[str] = None, to_json=False
    ) -> Union[JSON, str]:
        cmd_kwargs = {'path': str(path)}
        if id:
            cmd_kwargs['id'] = id
        if to_json:
            cmd_kwargs['format'] = 'json'
        return self.exec('get', cmd_kwargs=cmd_kwargs, to_json=to_json)


class XCResultToolMixin:
    @cached_property
    def xcresulttool(self) -> XCResultTool:
        return XCResultTool()
