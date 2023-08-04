import click

from cicd.core.cipher.cli import main as cipher


@click.group()
def main():
    pass


main.add_command(cipher, name='cipher')


if __name__ == '__main__':
    main()
