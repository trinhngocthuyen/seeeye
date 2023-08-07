import re


class BuildSettings(dict):
    @staticmethod
    def from_xcodebuild_settings(raw: str) -> 'BuildSettings':
        settings = BuildSettings()
        lines = raw.split('\n')
        start_idx = next(
            (
                idx + 1
                for idx, line in enumerate(lines)
                if line.startswith('Build settings for')
            ),
            None,
        )
        for line in lines[start_idx:]:
            if m := re.search(r'^\s*(\S+) =\s?(.*)', line):
                settings[m.group(1)] = m.group(2)
        return settings
