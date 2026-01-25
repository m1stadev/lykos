import asyncio
import sys
from typing import Annotated

import typer
from async_typer import AsyncTyper
from loguru import logger

import lykos
from lykos import Client, __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def version_callback(val: bool) -> None:
    if val:
        print(f'lykos {__version__}')
        raise typer.Exit()


app = AsyncTyper()


@app.async_command(context_settings=CONTEXT_SETTINGS)
async def cli(
    buildid: Annotated[
        str, typer.Option('--buildid', '-b', help='*OS buildid.', prompt=True)
    ],
    device: Annotated[
        str, typer.Option('--device', '-d', help='Device identifier.', prompt=True)
    ],
    verbose: Annotated[
        bool, typer.Option('--verbose', '-v', help='Enable verbose logging.')
    ] = False,
    codename: Annotated[
        str | None, typer.Option('--codename', '-c', help='*OS codename.')
    ] = None,
    component: Annotated[
        str | None,
        typer.Option('--component', '-n', help='Component to print keys for.'),
    ] = None,
    version: Annotated[
        bool | None, typer.Option('--version', callback=version_callback)
    ] = None,
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

    async with Client() as client:
        print(
            f'Searching for{" " if component is None else " " + component.lower() + " "}keys for ({device},{" " if codename is None else " " + codename + " "}{buildid})...'
        )

        try:
            data = await client.get_key_data(
                device=device, buildid=buildid, codename=codename
            )
        except lykos.PageNotFound:
            print(
                f'Failed to fetch keys for ({device},{" " if codename is None else " " + codename + " "}{buildid}).'
            )
            raise typer.Abort()

        if component:
            try:
                component = next(
                    c for c in data if c.name.casefold() == component.casefold()
                )
            except StopIteration:
                print(
                    f'No keys found for component {component.lower()} (available keys: {", ".join(c.name for c in data)}).'
                )
                raise typer.Abort()

            print(f'Component: {component.name}')
            print(f'File: {component.filename}')
            print(f'Key: {component.key.hex()}')
            print(f'IV: {component.iv.hex()}')

        else:
            for comp in data:
                print(f'Component: {comp.name}')
                print(f'File: {comp.filename}')
                print(f'Key: {comp.key.hex()}')
                print(f'IV: {comp.iv.hex()}')

                if comp != data[-1]:
                    print()


def main() -> None:
    asyncio.run(app())
