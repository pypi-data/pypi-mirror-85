# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect connect-cli.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import click

from cnctcli.actions.products import ProductSynchronizer, dump_product
from cnctcli.commands.utils import continue_or_quit
from cnctcli.config import pass_config
from cnct import ConnectClient
from cnct.rql import R


@click.group(name='product', short_help='commands related to product management')
def grp_product():
    pass  # pragma: no cover


@grp_product.command(
    name='list',
    short_help='list products',
)
@click.option(
    '--query',
    '-q',
    'query',
    help='RQL query expression.',
)
@click.option(
    '--page-size',
    '-p',
    'page_size',
    type=int,
    help='Number of products per page.',
    default=25,
)
@click.option(
    '--always-continue',
    '-c',
    'always_continue',
    is_flag=True,
    help='Do not prompt to continue.',
)
@pass_config
def cmd_list_products(config, query, page_size, always_continue):
    acc_id = config.active.id
    acc_name = config.active.name
    if not config.silent:
        click.echo(
            click.style(
                f'Current active account: {acc_id} - {acc_name}\n',
                fg='blue',
            )
        )
    client = ConnectClient(
        api_key=config.active.api_key,
        endpoint=config.active.endpoint,
    )

    if acc_id.startswith('VA'):
        default_query = R().visibility.owner.eq(True) & R().version.null(True)
    else:
        default_query = R().visibility.listing.eq(True) | R().visibility.syndication.eq(True)

    query = query or default_query
    paging = 0
    query_products = client.products.filter(query).limit(page_size)

    for prod in query_products:
        paging += 1
        click.echo(
            f"{prod['id']} - {prod['name']}"
        )
        if paging % page_size == 0 and paging != query_products.count() and not always_continue:
            if not continue_or_quit():
                return


@grp_product.command(
    name='export',
    short_help='export a product to an excel file',
)

@click.argument('product_id', metavar='product_id', nargs=1, required=True)  # noqa: E304
@click.option(
    '--out',
    '-o',
    'output_file',
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    help='Path to the output Excel file.'
)
@pass_config
def cmd_dump_products(config, product_id, output_file):
    config.validate()
    acc_id = config.active.id
    acc_name = config.active.name
    if not config.silent:
        click.echo(
            click.style(
                f'Current active account: {acc_id} - {acc_name}\n',
                fg='blue',
            )
        )
    outfile = dump_product(
        config.active.endpoint,
        config.active.api_key,
        product_id,
        output_file,
        config.silent,
    )
    if not config.silent:
        click.echo(
            click.style(
                f'\nThe product {product_id} has been successfully exported to {outfile}.',
                fg='green',
            )
        )


@grp_product.command(
    name='sync',
    short_help='sync a product from an excel file',
)

@click.argument('input_file', metavar='input_file', nargs=1, required=True)  # noqa: E304
@click.option(  # noqa: E304
    '--yes',
    '-y',
    'yes',
    is_flag=True,
    help='Answer yes to all questions.'
)
@pass_config
def cmd_sync_products(config, input_file, yes):
    config.validate()
    acc_id = config.active.id
    acc_name = config.active.name
    if not config.silent:
        click.echo(
            click.style(
                f'Current active account: {acc_id} - {acc_name}\n',
                fg='blue',
            )
        )
    # To be fixed specs_location when using new version of client
    client = ConnectClient(
        api_key=config.active.api_key,
        endpoint=config.active.endpoint,
        validate_using_specs=False,
    )
    synchronizer = ProductSynchronizer(
        client,
        config.silent,
    )
    product_id = synchronizer.open(input_file)

    if not yes:
        click.confirm(
            'Are you sure you want to synchronize '
            f'the items for the product {product_id} ?',
            abort=True,
        )
        click.echo('')

    skipped, created, updated, deleted, errors = synchronizer.sync()

    ok_actions = created + updated + deleted
    errors_count = len(errors)
    processed = skipped + ok_actions + errors_count

    synchronizer.save(input_file)

    if not config.silent:
        msg = f'\nThe product {product_id} has been successfully synchronized.'
        fg = 'green'

        if ok_actions == 0:
            msg = f'\nNo item has been synchronized for the product {product_id}.'
            fg = 'red'
        else:
            if errors:
                msg = f'\nThe product {product_id} has been partially synchronized.'
                fg = 'yellow'

        click.echo(click.style(msg, fg=fg))

        click.echo(
            click.style(
                (
                    f'\nProcessed rows: {processed}\n'
                    f'  - Created: {created}\n'
                    f'  - Updated: {updated}\n'
                    f'  - Deleted: {deleted}\n'
                    f'  - Skipped: {skipped}\n'
                    f'  - Errors: {errors_count}\n'
                ),
                fg='blue'
            )
        )

        if errors:
            click.echo(
                click.style('\nErrors:\n', fg='magenta')
            )
            for row_idx, messages in errors.items():
                click.echo(f'  Errors at row #{row_idx}')
                for msg in messages:
                    click.echo(f'    - {msg}')
                click.echo(' ')
