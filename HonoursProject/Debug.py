import json
with open("values.txt")as f:
    symbolNameConverter = json.load(f)
count = {}
for v in symbolNameConverter.values():
    if v in count.keys():
        count[v] +=1
    else:
        count[v] =0
print(count)
    