# test point to point reachibilty
# get vlan, vrf, and ip 

import re
from netmiko import ConnectHandler
import getpass

device_ip = input('Please Enter Device IP : ')
user_name = input ('Please Enter your user name : ')
password = getpass.getpass("enter device password")
enable_pass = getpass.getpass('enter enable password')
order_id = input('Please enter order ID : ')

device_info = {'device_type': 'cisco_ios',
                'ip':device_ip,
                'username':user_name,
                'password': password,
                'secret':enable_pass
} 

net_connect = ConnectHandler(**device_info)
net_connect.enable()                                             # to enter enable mode , require enable password .. in secret 
output = net_connect.send_command('sh interface description | i ' + order_id )
print (output)
main_int = re.search('(\S+)',output).groups()
output = net_connect.send_command('sh run interface ' + main_int[0])     # re.search return tuple so use main_int[0]   
print (output)
ip = re.search('address (\S+)',output).groups()
vlan = re.search('dot1Q (\S+)',output).groups()
vrf= re.search('forwarding (\S+)',output).groups()
ip =ip[0].split('.')                                # convert list to string , (.) is delimater between each element
if (int(ip[-1]) %2 == 0):                            # add or remove 1 from last digit in ip add to get point to point ip 
    ip[-1] = int(ip[-1]) - 1
    ip[-1] = str(ip[-1])                            # convert last digit to string again 
else:
    ip[-1] = int(ip[-1]) + 1
    ip[-1] = str(ip[-1])    

ip = '.'.join(ip)      # convert list to string again , (.) is delimater between each element)
reachipility = net_connect.send_command('ping vrf ' + vrf[0] + " "+ ip)
print(reachipility)
print('Main Vlan is : ' + vlan[0])
