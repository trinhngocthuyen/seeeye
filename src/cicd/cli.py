import click

from cicd.ios.cli import main as ios


@click.group()
def main():
    pass


main.add_command(ios, name='ios')


if __name__ == '__main__':
    main()
