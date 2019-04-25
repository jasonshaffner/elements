import sys
from elements import GraphQLQueryGenerator
from elements.utils.graphqlclient import GraphQLClient

table = 'device'
columns = ['hostname', {'makeByMake': 'make'}, {'deviceIpByDeviceIp': ['v4Ip', 'v6Ip']}]

query = GraphQLQueryGenerator.queryAll(table, columns)
server = sys.argv[1]
print(query)
gql = GraphQLClient(server)
print(gql.execute(query))
