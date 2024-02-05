import json
import subprocess
import sys

process=subprocess.Popen(['pluginctl','-r','return_gateways_status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
data = json.loads(out)

if len(sys.argv) == 3:
    want_name = sys.argv[1]
    want_value = sys.argv[2]
else:
    want_name = False
    want_value = False

data_out = []
for gw in data['dpinger']:
    data_out.append({
        "{#GW_NAME}": data['dpinger'][gw]['name']
    })

if not want_name:
    print(json.dumps(data_out, indent=2))
    sys.exit(0)


# Normalize some values
if want_value == 'status':
    if data['dpinger'][want_name][want_value] == 'none':
        value = 0
    elif data['dpinger'][want_name][want_value] == 'down':
        value = 2
    else:
        value = 1
elif want_value == 'delay' or want_value == 'stddev':
    value = data['dpinger'][want_name][want_value].replace(" ms","")
elif want_value == 'loss':
    value = data['dpinger'][want_name][want_value].replace(" %","")
else:
    value = data['dpinger'][want_name][want_value]


print(value)