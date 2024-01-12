import json
import subprocess
import re
import sys

import xml.etree.ElementTree as ET
import sys

root = ET.parse('/conf/config.xml').getroot()

process=subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)

if len(sys.argv) == 3:
    want_name = sys.argv[1]
    want_value = sys.argv[2]
else:
    want_name = False
    want_value = False

interfaces = []
interface = None
for line in process.stdout:
    line = line.decode('utf-8')
    if not line.startswith('\t'):
        name = line.split(':')[0]

        if want_name and want_name != name:
            continue

        if interface is not None:
            interfaces.append(interface)

        interface = {
            'name': name
        }

        for conf_interface in root.findall('interfaces')[0]:
            if conf_interface.findall('if')[0].text == name:
                interface['description'] = conf_interface.findall('descr')[0].text
    else:
        if interface is None:
            continue

        line = line.replace('\t','')
        line = line.replace('\n','')
        data = line.split(':')
        if len(data) < 2:
            continue

        field_name = data[0]
        if want_value and field_name != want_value:
            continue

        # Sometimes this is data that broken up.  We don't have to use this though
        fields = data[1].split(' ')
        if field_name == 'carp':
            if fields[1] == 'MASTER':
                interface['carp'] = 0
            else:
                interface['carp'] = 1
        elif field_name == 'status':
            interface['status'] = data[1]


interfaces.append(interface)

if not want_name:
    print(json.dumps(interfaces, indent=2))
else:
    print(interfaces[0][want_value])