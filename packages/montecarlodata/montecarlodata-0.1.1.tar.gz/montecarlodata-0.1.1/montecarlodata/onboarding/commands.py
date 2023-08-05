import click
import click_config_file

import montecarlodata.settings as settings
from montecarlodata.errors import complain_and_abort
from montecarlodata.onboarding.data_lake.presto import PrestoOnBoardService


@click.group(help='On-board Monte Carlo warehouse or data-lake.')
def on_boarding():
    """
    Group for any on-board sub-commands
    """
    pass


@on_boarding.command(help='Setup Presto SQl Connection. For health queries like metrics and distribution.')
@click.pass_obj
@click.option('--host', help='Hostname.', required=True)
@click.option('--port', help='HTTP port (default=8889).', default=8889, type=click.INT)
@click.option('--user', help='Username with access to catalog/schema.', required=False)
@click.password_option('--password', help='User\'s password.', prompt='Password for user (enter to skip)',
                       default='', required=False)
@click.option('--catalog', help='Mount point to access data source.', required=False)
@click.option('--schema', help='Schema to access.', required=False)
@click.option('--http-scheme', help='Scheme for authentication.',
              type=click.Choice(['http', 'https'], case_sensitive=True), required=True)
@click.option('--cert-file', help='Local SSL certificate file to upload to collector.', required=False,
              type=click.Path(dir_okay=False, exists=True))
@click.option('--cert-s3', help='Object path (key) to a certificate already uploaded to the collector.',
              required=False)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def presto_sql(ctx, host, port, user, password, catalog, schema, http_scheme, cert_file, cert_s3):
    """
    On-board a presto sql connection
    """
    if not password:
        password = None  # make explicitly null if not set. Prompts can't be None
    if cert_file is not None and cert_s3 is not None:
        complain_and_abort('Can have a cert-file or cert-s3-path, but not both')
    PrestoOnBoardService(config=ctx['config']).on_board_presto_sql(host=host, port=port, user=user, password=password,
                                                                   catalog=catalog, schema=schema,
                                                                   http_scheme=http_scheme, cert_file=cert_file,
                                                                   cert_s3=cert_s3)
