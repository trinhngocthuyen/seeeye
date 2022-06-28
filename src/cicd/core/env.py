import os


class Env:
    ci: bool = os.getenv('CI') == 'true'
