import re

props = open("Leads List 1")

for prop in props:
    x = re.search("\d{1,5}\s+(\D\s+)?\w+\s+\w{2,4}", prop)
    x = re.split('\s+', x.group())
    if(len(x) == 4):
        x = [x[0], x[1] + ' ' + x[2], x[3]]
    print(x)

props.close()



