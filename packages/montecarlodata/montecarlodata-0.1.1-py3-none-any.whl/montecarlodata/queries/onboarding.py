# Queries related to on-boarding

TEST_PRESTO_CRED_MUTATION = """
mutation testPrestoCredentials($catalog:String, $host:String, $httpScheme:String, $password:String, $port:Int, $schema:String, $sslOptions:SslInputOptions, $user:String) {
  testPrestoCredentials(catalog:$catalog, host:$host, httpScheme:$httpScheme, password:$password, port:$port, schema:$schema, sslOptions: $sslOptions, user:$user) {
    key
  }
}
"""

ADD_CONNECTION_MUTATION = """
mutation addConnection($connectionType:String!, $createWarehouseType:String, $dwId:UUID, $jobTypes:[String], $key:String!) {
  addConnection(connectionType:$connectionType, createWarehouseType:$createWarehouseType, dwId:$dwId, jobTypes:$jobTypes, key:$key){
    connection {
      uuid
    }
  }
}
"""
