import json
from collections import namedtuple

# Opening JSON file
f = open('clientes.json', "r")


def customClienteDecoder(clientDict):
    return namedtuple('cliente', clientDict.keys())(*clientDict.values())


# Parse JSON into an object with attributes corresponding to dict keys.
clientes = json.loads(f.read(), object_hook=customClienteDecoder)


# print(clientes)
for c in clientes[0]:
    print(c.nome)
    print(c.saldo)
