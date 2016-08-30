import json

num_flops = 0

with open("84.json") as jsonfile:
    j_file = json.load(jsonfile)

    flops = j_file['cpu']['sequence']

    for i in range(len(flops)):
        num_flops += flops[i][1]['flops']


print round(num_flops)
