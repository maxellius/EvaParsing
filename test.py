import json

with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
print(data)