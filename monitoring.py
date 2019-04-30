import subprocess
from influxdb import InfluxDBClient
from datetime import datetime
import re
from time import sleep
#import pprint

dbhost = "localhost"
dbport = "8086"
arpRegex = "(?:hosts\/sec).(.*)"
#pp = pprint.PrettyPrinter()

influxClient = InfluxDBClient(host=dbhost, port=dbport)

influxClient.switch_database('network-devices')

def getNetworkDeviceCount():
    output = subprocess.Popen(["arp-scan", "-l", "-B", "1024000", "-q"], stdout= subprocess.PIPE)
    stdout,stderr = output.communicate()
    arpScanOutput = stdout
    arpScanOutput = "".join(re.findall(arpRegex, str(arpScanOutput)))
    networkDeviceCount = int(re.findall('-?\d+\.?\d*', arpScanOutput)[0])
    return networkDeviceCount

while True:
    currentTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_body = [
        {
            "measurement": "network-device-count",
            "time": currentTime,
            "fields": {
                "network-device-count": getNetworkDeviceCount()
            }
        }
    ]
    #pp.pprint(json_body)
    influxClient.write_points(json_body)
    sleep(5)
