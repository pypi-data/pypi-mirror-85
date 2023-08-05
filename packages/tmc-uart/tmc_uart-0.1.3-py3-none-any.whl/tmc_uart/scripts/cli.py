# Skeleton of a CLI

import click

import tmc_uart


@click.command('tmc_uart')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(tmc_uart.has_legs)
