# test point to point reachibilty
# get vlan, vrf, and ip 
# check reachibility for main and minitor interfaces


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

interfaces = re.findall('([GT]\S+)',output)                            # get giga interfaces (main and monitor) and put them in list 
output = net_connect.send_command('sh run interface ' + interfaces[0])     # re.search return tuple so use main_int[0] 
print (output)


def check_reachibility():                                            # create function to check main mad monitor reachibility
    ip = re.search('address (\S+)',output).groups()
    vlan = re.search('dot1Q (\S+)',output).groups()
    vrf= re.search('forwarding (\S+)',output).groups()
    ip =ip[0].split('.')                                             # convert list to string , (.) is delimater between each element
    if (int(ip[-1]) %2 == 0):                                        # add or remove 1 from last digit in ip add to get point to point ip 
        ip[-1] = int(ip[-1]) - 1
        ip[-1] = str(ip[-1])                                           # convert last digit to string again 
    else:
        ip[-1] = int(ip[-1]) + 1
        ip[-1] = str(ip[-1])    

    ip = '.'.join(ip)      # convert list to string again , (.) is delimater between each element)
    reachipility = net_connect.send_command('ping vrf ' + vrf[0] + " "+ ip)
    print(reachipility)


check_reachibility()

if (len(interfaces[1] > 0)):                                                  # check if there is main and monitor interface or not 
    output = net_connect.send_command('sh run int ' + interfaces[1])
    check_reachibility()


physical_int = re.search('([GT]\S\S\S\S)',output).groups()                       # get main physical interface
output = net_connect.send_command('sh run int ' + physical_int)
print (output)
output = net_connect.send_command('sh arp int '+ physical_int + '.400')            


