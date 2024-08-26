import sys
from typing import Optional

import click
from loguru import logger

import lykos

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(message=f'lykos {lykos.__version__}')
@click.option(
    '-d',
    '--device-identifier',
    'device',
    type=str,
    required=True,
    help='Device identifier.',
)
@click.option(
    '-b',
    '--build-id',
    'buildid',
    type=str,
    required=True,
    help='*OS buildid.',
)
@click.option(
    '-c',
    '--codename',
    'codename',
    type=str,
    help='*OS codename.',
)
@click.option(
    '-n',
    '--component',
    'component',
    type=str,
    help='Component to print keys for.',
)
@click.option(
    '-v',
    '--verbose',
    'verbose',
    is_flag=True,
    default=False,
    help='Enable verbose logging.',
)
def main(
    buildid: str,
    device: str,
    verbose: bool,
    codename: Optional[str] = None,
    component: Optional[str] = None,
) -> None:
    """A Python CLI tool for fetching *OS firmware keys."""

    if verbose:
        logger.remove()
        logger.add(
            sys.stderr,
            level='DEBUG',
            format='[{time:MMM D YYYY - hh:mm:ss A zz}] {level} | {module}:{function}:{line} {message}',
        )
        logger.enable(__package__)
    else:
        sys.tracebacklimit = 0

    client = lykos.Client()

    click.echo(
        f"Searching for{' ' if component is None else ' ' + component.lower() + ' '}keys for ({device},{' ' if codename is None else ' ' + codename + ' '}{buildid})..."
    )

    try:
        data = client.get_key_data(device=device, buildid=buildid, codename=codename)
    except lykos.PageNotFound:
        raise click.ClickException(
            f"Failed to fetch keys for ({device},{' ' if codename is None else ' ' + codename + ' '}{buildid})."
        )
    if component:
        try:
            component = next(
                c for c in data if c.name.casefold() == component.casefold()
            )
        except StopIteration:
            raise click.ClickException(
                f"No keys found for component {component.lower()} (available keys: {', '.join(c.name for c in data)})."
            )

        click.echo(f'Component: {component.name}')
        click.echo(f'File: {component.filename}')
        click.echo(f'Key: {component.key.hex()}')
        click.echo(f'IV: {component.iv.hex()}')

    else:
        for comp in data:
            click.echo(f'Component: {comp.name}')
            click.echo(f'File: {comp.filename}')
            click.echo(f'Key: {comp.key.hex()}')
            click.echo(f'IV: {comp.iv.hex()}')

            if comp != data[-1]:
                click.echo()


if __name__ == '__main__':
    main()
