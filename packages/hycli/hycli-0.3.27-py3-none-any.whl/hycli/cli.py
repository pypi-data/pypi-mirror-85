import os

import click
import toml

from .commands import to_csv, to_xlsx, to_json, config
from .commons.endpoints import default_endpoints
from . import __version__


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"Version {__version__}")
    ctx.exit()


@click.group()
@click.option(
    "-c",
    "--config-file",
    type=click.Path(),
    default="~/.hycli/config.toml",
    show_default=True,
)
@click.option(
    "-v",
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Print out hycli version",
)
@click.option(
    "-e",
    "--endpoint-env",
    default="production",
    show_default=True,
    type=click.Choice(["localhost", "staging", "production"], case_sensitive=False),
    help="endpoint environment",
)
@click.option(
    "-u",
    "--username",
    envvar="HYCLI_USERNAME",
    default=None,
    help="your API username for accessing the environment",
)
@click.option(
    "-p",
    "--password",
    envvar="HYCLI_PASSWORD",
    default=None,
    help="your API password for accessing the environment",
)
@click.option(
    "--extractor", help="custom extractor endpoint",
)
@click.option(
    "-H",
    "--header",
    multiple=True,
    help="extractor endpoint header(s) can be multiple. Similair to curl, e.g. -H 'keyheader: value' -H '2ndkeyheader: 2ndvalue'",
)
@click.pass_context
def main(ctx, config_file, endpoint_env, username, password, extractor, header):
    """
    Can convert 1 invoice to xml or a directory of invoices to csv/xlsx.
    It is advised to configurate credentials and endpoints before use with: \n >> hycli config
    """
    filename = os.path.expanduser(config_file)
    ctx.obj = {
        "config_file": filename,
        "env": endpoint_env,
        "headers": {h.split(":")[0].strip(): h.split(":")[1].strip() for h in header},
    }

    try:
        with open(filename) as cfg:
            conf = toml.loads(cfg.read())

        ctx.obj["config"] = conf[endpoint_env]

    except (FileNotFoundError, KeyError):
        click.echo(
            f"No configuration found, using default endpoints for {endpoint_env} environment."
        )
        click.echo("Define custom endpoints for environment with: >> hycli config \n")
        ctx.obj["config"] = {
            "endpoints": {
                k: v
                for k, v in default_endpoints[endpoint_env].items()
                if v is not None
            }
        }

    if username:
        ctx.obj["config"]["username"] = username

    if password:
        ctx.obj["config"]["password"] = password

    if extractor:
        ctx.obj["config"]["endpoints"]["extractor"] = extractor


main.add_command(to_csv.to_csv)
main.add_command(to_xlsx.to_xlsx)
main.add_command(to_json.to_json)
main.add_command(config.config)

if __name__ == "__main__":
    main()
