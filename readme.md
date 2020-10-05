# Get Interface Information from NetBrain

## Getting Started

This script will get all devices from a NetBrain Domain and then list each device with it's interfaces, IP, Mask, VLAN, and VRF.

### Prerequisites

* NetBrain Account
* Python 3
* Rich

### Running

>*This script will run against all devices in a domain*

Rename config-example.py to config.py and enter the following details: NetBrain URL, username, password, NetBrain DomainID, NetBrain TenantID.

Run the script from the CLI.

![Output Example](https://github.com/terryfera/NetBrain-Get-Interface-Details/blob/main/images/device_output.png "Example output for device")