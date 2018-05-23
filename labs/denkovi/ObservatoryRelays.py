# For python 2.7
# Suitable for all Denkovi devices which supports /current_state.xml
# Usage: ObservatoryRelays.py  ip port password
# Examples:
# denkovihttp.py 192.168.0.100:80 admin
# ObservatoryRelays.py 192.168.0.100 80 admin

import http.client
import sys
import xml.etree.ElementTree as et
import argparse




class Relay:
    def __init__(self):
        self.relayNumber = 0
        self.name = ""
        # state 0 means OFF,  1 means ON
        self.state = 0
# end class


def httpget(ip, port, pw, parametersIn):

    conn = http.client.HTTPConnection(ip, int(port), timeout=5)  # 5 seconds timeout
    conn.request("GET", "/current_state.xml?pw=" + pw + "&" + parametersIn)
    r1 = conn.getresponse()
    response = r1.read()
    conn.close()
    root = et.fromstring(response)

    print(response.decode());

# end def




def main(args):

    httpget(args.ip, args.port, args.password, args.parameters)

# end def


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Observatory Replay Board control')
    parser.add_argument('ip', help='The IP address of relay switch board')
    parser.add_argument('port', help='The port for the relay board')
    parser.add_argument('password', help='The password of the relay board')
    parser.add_argument('-p', '--parameters',help='optional parameters', default='')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    main(args)
# endif
