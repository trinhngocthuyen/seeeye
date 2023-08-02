import click

from .codesign import CodeSign


@click.group()
def main():
    pass


@main.command
@click.option('--dir', required=True, help='Dir containing certificates and profiles')
@click.option('--cert-password', help='Certificate password')
def prepare(**kwargs):
    CodeSign(**kwargs).prepare()


@main.command
def cleanup(**kwargs):
    CodeSign(**kwargs).cleanup()


if __name__ == '__main__':
    main()
