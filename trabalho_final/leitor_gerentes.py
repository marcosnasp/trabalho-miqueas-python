# Python program to read
# json file
from gerente import Gerente
import json

# Opening JSON file
f = open('gerentes.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data['gerentes']:
    print(i['nome'])


print(data)
print(type(data))

data['gerentes'].append({
    "nome": "Monica",
    "senha": "123456"
})

print(data)

with open('gerentes.json', 'w') as json_file:
    json.dump(data, json_file,
              indent=4,
              separators=(',', ': '))


# Closing file
f.close()
