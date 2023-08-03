import click

from cicd.core._cli.opts import Opts
from cicd.core.cipher.cli import decrypt, encrypt
from cicd.core.utils.file import FileUtils

from .codesign import CodeSign

opts = Opts(
    dir=click.option(
        '--dir', required=True, help='Dir containing certificates and profiles'
    ),
    password=click.option(
        '--password', required=True, help='Encryption/decryption password'
    ),
)


@click.group()
def main():
    pass


@main.command
@opts.use('dir')
@click.option('--password', help='Password to decrypt certificates and profiles')
@click.option('--cert-password', help='Certificate password')
def prepare(**kwargs):
    with FileUtils.tempdir() as dec_dir:
        if kwargs.get('password') is not None:
            kwargs['enc_dir'] = kwargs.pop('dir')
            kwargs['dir'] = dec_dir
        CodeSign(**kwargs).prepare()


@main.command
def cleanup(**kwargs):
    CodeSign(**kwargs).cleanup()


main.add_command(encrypt, name='encrypt')
main.add_command(decrypt, name='decrypt')


if __name__ == '__main__':
    main()
