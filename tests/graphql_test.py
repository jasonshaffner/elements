from elements import graphqElements

variable = graphqElements.var('deviceId', 12345)
option = graphqElements.input(variable)
deviceId = graphqElements.queryElement('deviceId')
hostname = graphqElements.queryElement('hostname')
delete = graphqElements.queryElement('deleteDeviceByDeviceId', deviceId, hostname, input=option)
mutation = graphqElements.query('deleteDevice', 'mutation', delete)


print(mutation())
