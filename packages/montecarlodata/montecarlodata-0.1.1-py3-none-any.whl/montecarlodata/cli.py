import click

import montecarlodata.settings as settings
from montecarlodata.config import ConfigManager
from montecarlodata.onboarding.commands import on_boarding


@click.group(help='Monte Carlo\'s CLI.')
@click.option('--profile', default=settings.DEFAULT_PROFILE_NAME,
              help='Specify an MCD profile name. Uses default otherwise.')
@click.option('--config-path', default=settings.DEFAULT_CONFIG_PATH, type=click.Path(dir_okay=True),
              help=f'Specify path where to look for config file. Uses {settings.DEFAULT_CONFIG_PATH} otherwise.')
@click.version_option()
@click.pass_context
def entry_point(ctx, profile, config_path):
    """
    Entry point for all sub-commands and options. Reads configuration and sets as context, except when configuring
    or getting help.
    """
    if ctx.invoked_subcommand != settings.CONFIG_SUB_COMMAND and settings.HELP_FLAG not in click.get_os_args():
        config = ConfigManager(profile_name=profile, base_path=config_path).read()
        if not config:
            ctx.abort()
        ctx.obj = {'config': config}


@click.command(help='Configure the MCD CLI.')
@click.option('--profile-name', required=False, help='Specify a profile name for configuration.',
              default=settings.DEFAULT_PROFILE_NAME)
@click.option('--config-path', required=False, help='Specify path where to look for config file.',
              default=settings.DEFAULT_CONFIG_PATH, type=click.Path(dir_okay=True))
@click.option('--mcd-id', prompt='MCD ID', help='Monte Carlo token user ID.')
@click.password_option('--mcd-token', prompt='MCD Token', help='Monte Carlo token value.')
@click.option('--aws-profile', prompt='AWS profile name',
              help='AWS named profile with access to the DC stack and resources (e.g. CloudFormation and S3).',
              default='')
@click.option('--aws-region', prompt='AWS region', help='AWS region where DC is deployed.',
              default=settings.DEFAULT_AWS_REGION)
def configure(profile_name, config_path, mcd_id, mcd_token, aws_profile, aws_region):
    """
    Special sub-command for configuring the CLI
    """
    ConfigManager(profile_name=profile_name, base_path=config_path).write(mcd_id=mcd_id,
                                                                          mcd_token=mcd_token,
                                                                          aws_profile=aws_profile,
                                                                          aws_region=aws_region)


entry_point.add_command(on_boarding)
entry_point.add_command(configure)
