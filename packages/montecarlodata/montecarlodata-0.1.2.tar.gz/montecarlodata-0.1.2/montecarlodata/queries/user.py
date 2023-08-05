# Queries related to users

GET_USER_QUERY = """
query getUser {
  getUser {
    account {
      uuid
      dataCollectors {
        uuid
        stackArn
        active
        warehouses {
          uuid
        }
      }
    }
  }
}
"""
