# Top 5 API to get started with Cisco DNA Center for Network Engineers

This repository contains a few simple scripts to get started with Cisco DNA Center API.

You will need the requests[secure] python module.

```buildoutcfg
pip install requests[secure]
```

You change the controller credentials either through environment variables or by editing the dnac_config.py file
## 01_network_device.py
This script will show all of the network devices in the inventory of Cisco DNA Center.
```buildoutcfg
./01_network_device.py
./01_network_device.py 10.10.22.70

```
## 02_interface_device.py
This script shows all of the interfaces connected to a specific device.
```buildoutcfg

./02_interface_device.py 10.10.22.70

```
## 03_device_license.py
Shows the software license information for a device.
```buildoutcfg

./03_device_license.py 10.10.22.70

```
## 04_find_host.py
Locates a host by IP address or mac address. Can also be extended to user lookup.
```buildoutcfg

./04_find_host.py --ip 10.10.22.114
./04_find_host.py --mac 00:1e:13:a5:b9:40
```
## 05_path_trace.py
Traces the path from host A to host B through the network
```buildoutcfg
./05_path_trace.py --srcip 10.10.22.114 --dstip 10.10.22.98
```
