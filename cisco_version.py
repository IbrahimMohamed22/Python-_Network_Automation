# try to get main and monitor interfaces 
# get vlan, vrf, and ip 
# test point to point reachibilty

import re
from netmiko import ConnectHandler
import getpass

device_ip = input('Please Enter Device IP : ')
user_name = input (' Please Enter your user name : ')
password = getpass.getpass()
enable_pass =input('enter enable password')
order_id = input('Please enter order ID : ')

device_info = {'device_type': 'cisco_ios',
                'ip':device_ip,
                'username':user_name,
                'password': password,
                'secret':enable_pass
} 

net_connect = ConnectHandler(**device_info)
output = net_connect.send_command('sh interface description | i ' + order_id )
print (output)
print(net_connect.find_prompt())
main_int = input ('Please Enter main interface : ')
print(main_int, type(main_int))
#monitor_int = input ('please enter monitor interface : ')
output = net_connect.send_command('sh run interface ' + main_int)
print (output)
#vrf = re.search('forwarding (\S+)',output).groups()
#ip = re.search('ip address (\S+)',output).groups()
#reachipility = net_connect.send_command('ping vrf '+ vrf + " " + ip )
#print(reachipility)
