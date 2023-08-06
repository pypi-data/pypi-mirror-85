from montecarlodata.config import Config
from montecarlodata.onboarding.data_lake.data_lakes import DataLakeOnBoardService
from montecarlodata.queries.onboarding import TEST_PRESTO_CRED_MUTATION, TEST_S3_CRED_MUTATION


class PrestoOnBoardService(DataLakeOnBoardService):
    _CERT_PREFIX = 'certificates/presto/'
    _EXPECTED_PRESTO_SQL_GQL_RESPONSE_FIELD = 'testPrestoCredentials'
    _EXPECTED_PRESTO_S3_GQL_RESPONSE_FIELD = 'testS3Credentials'
    _SQL_CONNECTION_TYPE = 'presto'
    _S3_CONNECTION_TYPE = 's3'  # TODO - change to presto-s3 (requires monolith changes)
    _QL_JOB_TYPE = ['query_logs']

    def __init__(self, config: Config, **kwargs):
        super().__init__(config, **kwargs)

    def onboard_presto_sql(self, **kwargs) -> None:
        """
        Onboard a presto-sql connection by validating and adding a connection.
        Also, optionally uploads a certificate to the DC bucket.
        """
        self._handle_cert(cert_prefix=self._CERT_PREFIX, options=kwargs)
        temp_path = self._validate_connection(query=TEST_PRESTO_CRED_MUTATION,
                                              response_field=self._EXPECTED_PRESTO_SQL_GQL_RESPONSE_FIELD, **kwargs)
        self._add_connection(temp_path=temp_path, connection_type=self._SQL_CONNECTION_TYPE)

    def onboard_presto_s3(self, **kwargs) -> None:
        """
        Onboard a presto-s3 connection by validating and adding a connection
        """
        temp_path = self._validate_connection(query=TEST_S3_CRED_MUTATION,
                                              response_field=self._EXPECTED_PRESTO_S3_GQL_RESPONSE_FIELD, **kwargs)
        self._add_connection(temp_path=temp_path, connection_type=self._S3_CONNECTION_TYPE, job_types=self._QL_JOB_TYPE)
