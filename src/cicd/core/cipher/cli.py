import click

from cicd.core._cli.opts import Opts

from .cipher import Cipher

opts = Opts(
    password=click.option(
        '--password', required=True, help='Encryption/decryption password'
    ),
    in_path=click.option('--in', required=True, help='Input file'),
    out_path=click.option('--out', help='Output file'),
)


@click.group()
def main():
    pass


def perform(action: Cipher.Action, **kwargs):
    password = kwargs.get('password')
    cipher = Cipher(password=password)
    cipher.perform(action=action, in_path=kwargs.get('in'), out_path=kwargs.get('out'))


@main.command
@opts.use_all()
def encrypt(**kwargs):
    perform(action=Cipher.Action.ENCRYPTION, **kwargs)


@main.command
@opts.use_all()
def decrypt(**kwargs):
    perform(action=Cipher.Action.DECRYPTION, **kwargs)


if __name__ == '__main__':
    main()
