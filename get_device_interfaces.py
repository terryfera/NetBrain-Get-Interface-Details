import requests
import time
import urllib3
import pprint
import json
import ipaddress
import config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from rich.table import Table
from rich.console import Console

nb_url = config.nb_url

# Set proper headers
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}    
login_url = "/ServicesAPI/API/V1/Session"

# Login script
body = {
    "username" : config.username,      
    "password" : config.password  
}

try:
    response = requests.post(nb_url + login_url, headers=headers, data = json.dumps(body), verify=False)
    if response.status_code == 200:
        js = response.json()
        token = js['token']
        headers["Token"] = token
    else:
        print ("Get token failed! - " + str(response.text))
except Exception as e:
    print (str(e))


# Set Tenant and Domain
set_domain_url = "/ServicesAPI/API/V1/Session/CurrentDomain"

body = {
  "tenantId": config.tenantID,
  "domainId": config.domainID
}

try:
    # Do the HTTP request
    response = requests.put(nb_url + set_domain_url, data=json.dumps(body), headers=headers, verify=False)
    # Check for HTTP codes other than 200
    if response.status_code == 200:
        # Decode the JSON response into a dictionary and use the data
        result = response.json()
        #print ("Set domain result: ")
        #print (result)
    elif response.status_code != 200:
        print ("Set Tenant Failed - " + str(response.text))

except Exception as e: 
    print (str(e))

# Get Device Attributes

query_device = "dc-rt01"
get_dev_att_url = "/ServicesAPI/API/V1/CMDB/Devices"

try:
    response = requests.get(nb_url + get_dev_att_url, data=json.dumps(body), headers=headers, verify=False)
    if response.status_code == 200:
        result = response.json()
    elif response.status_code != 200:
        print ("Get Device Attributes Failed - " + str(response.text))

except Exception as e: 
    print (str(e))

# Print Device Table

table = Table(title="Device Details")

table.add_column("Device Hostname", style="cyan", no_wrap=True)
table.add_column("Mgmt IP", style="magenta", justify="right")
table.add_column("Device Type", style="sky_blue3", justify="right")

for dev in result['devices']:
    table.add_row(dev['hostname'], dev['mgmtIP'], dev['deviceTypeName'])
    
console = Console()
console.print(table)

# Print Interface Attributes for each devices

for dev in result['devices']:

    query_device = str(dev['hostname'])

    get_dev_att_url = "/ServicesAPI/API//V1/CMDB/Interfaces/?hostname=" + query_device

    try:
        response = requests.get(nb_url + get_dev_att_url, data=json.dumps(body), headers=headers, verify=False)
        if response.status_code == 200:
            dev_result = response.json()
        elif response.status_code != 200:
            print ("Get Device Attributes Failed - " + str(response.text))

    except Exception as e: 
        print (str(e))

    table = Table(title=str(dev['hostname']))

    
    table.add_column("Interface", style="dodger_blue1", no_wrap=True)
    table.add_column("Description", style="magenta", no_wrap=True)
    table.add_column("IP Address", style="white", no_wrap=True)
    table.add_column("Mask", style="white", no_wrap=True)
    table.add_column("VLAN", style="spring_green4", no_wrap=True)
    table.add_column("VRF", style="red", no_wrap=True)
    
    get_int_att_url = "/ServicesAPI/API//V1/CMDB/Interfaces/Attributes?hostname=" + query_device

    try:
        response = requests.get(nb_url + get_int_att_url, data=json.dumps(body), headers=headers, verify=False)
        if response.status_code == 200:
            int_result = response.json()
        elif response.status_code != 200:
            print ("Get Device Attributes Failed - " + str(response.text))

    except Exception as e: 
        print (str(e))

    for interface in dev_result['interfaces']:
        
        try:
            ip_addr = ipaddress.ip_address(int_result['attributes'][interface]['ips'][0]['ip']).__str__()
        except:
            ip_addr = "none"

        try:
            ip_mask = str(int_result['attributes'][interface]['ips'][0]['maskLen'])
        except:
            ip_mask = "none"
        
        try:
            int_desc = int_result['attributes'][interface]['descr']
        except:
            int_desc = "none"

        try:
            int_vrf = int_result['attributes'][interface]['mplsVrf']
        except:
            int_vrf = "none"

        try:
            int_vlan = int_result['attributes'][interface]['vlan']
        except:
            int_vlan = "none"


        
        table.add_row(interface, int_desc, ip_addr, ip_mask, int_vlan, int_vrf)

    console = Console()
    console.print(table)