from montecarlodata.config import Config
from montecarlodata.onboarding.data_lake.data_lakes import DataLakeOnBoardService
from montecarlodata.queries.onboarding import TEST_PRESTO_CRED_MUTATION


class PrestoOnBoardService(DataLakeOnBoardService):
    _CERT_PREFIX = 'certificates/presto/'
    _EXPECTED_GQL_RESPONSE_FIELD = 'testPrestoCredentials'
    _CONNECTION_TYPE = 'presto'

    def __init__(self, config: Config, **kwargs):
        super().__init__(config, **kwargs)

    def onboard_presto_sql(self, **kwargs) -> None:
        """
        Onboard a presto-sql connection by validating and adding a connection.
        Also, optionally uploads a certificate to the DC bucket.
        """
        self._handle_cert(cert_prefix=self._CERT_PREFIX, options=kwargs)
        temp_path = self._validate_connection(query=TEST_PRESTO_CRED_MUTATION,
                                              response_field=self._EXPECTED_GQL_RESPONSE_FIELD, **kwargs)
        self._add_connection(temp_path=temp_path, connection_type=self._CONNECTION_TYPE)
