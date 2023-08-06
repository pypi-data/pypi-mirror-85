from pathlib import Path

from fire import Fire

FORMATS = ['json', 'toml', 'yaml']

DIR = Path.cwd()

gitignore = DIR.joinpath('.gitignore')
config_ignore = '\n\n# myconfig\n{}'

python_code = """from myconfig import MyConfig

config = MyConfig(['{}', '{}'])
"""


def init(format: str, settings: str = 'settings', secrets: str = '.secrets') \
        -> None:
    '''Creates the file myconfig.
    Adds the path to the .settings file in .gitignore.

    Args:
        format (str): File format.
        settings (str, optional): Default config file. Defaults to 'settings'.
        secrets (str, optional): Default secret config file.\
        Defaults to '.secrets'.

    Raises:
        Exception: Unknown format.
    '''

    if format not in FORMATS:
        raise Exception('Unknown format.')
    for file in [settings, secrets]:
        f = open(DIR.joinpath(
            '{}.{}'.format(file, format)),
            'a',
            encoding='utf-8')
        f.close()

    if gitignore.exists():
        file = gitignore.read_text(encoding='utf-8')
        file += config_ignore.format(secrets + '.*')
        with open(gitignore, 'r+', encoding='utf-8') as f:
            text = f.read() + config_ignore.format(secrets + '.*')
            f.seek(0)
            f.write(text)
    with open(DIR.joinpath('settings.py'), 'w', encoding='utf-8') as f:
        f.write(
            python_code.format(
                '{}.{}'.format(settings, format),
                '{}.{}'.format(secrets, format)))


def main() -> None:
    '''CLI function'''
    Fire({
        'init': init
    })


if __name__ == '__main__':
    main()
