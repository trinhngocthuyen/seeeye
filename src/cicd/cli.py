import click

from cicd.core.cli import main as core
from cicd.ios.cli import main as ios


@click.group()
def main():
    pass


main.add_command(core, name='core')
main.add_command(ios, name='ios')


if __name__ == '__main__':
    main()
