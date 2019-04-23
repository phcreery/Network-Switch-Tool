# Network-Switch-Tool
Automation tool to perform tasks on Network Switches and Routers

## Getting Started

This small script helps with wiping Cisco Network Switches to factory defaults and clearing any configs or vlans. It can also do ASA devices and routers.

It currently supports:
 - Cisco Catalyst 2900-3700 switches
 - Cisco 1800/1841 & 2900 Router
 - Cisco ASA 5515-5520

### Prerequisites

What things you need to install the software and how to install them
```
pip install pyserial
```
or for python3
```
pip3 install pyserial
```

### Installing

```
git clone "https://github.com/phcreery/Network-Switch-Tool.git"
```

## Running

```
sudo python switchwiper2.py
```
or
```
sudo python3 switchwiper2.py
```


### Usage

There are three options to choose from upon initial startup
```
1) Cisco Catalyst Switch	(29xx - 37xx)
2) Cisco router 		(2900)			    	(Beta)
3) Cisco ASA 			(5515/5520)		     	(Beta)
4) Cisco router 		(1800/1841)		      (Dev)
```
Simply select yours and follow instructions!

## ToDo
This is the list of future changes:

 - [ ] Autodetect Type/Model
 - [ ] Autodetect serial port
 - [ ] Multiple instances in one setting
 - [ ] Update Switches and IOS
 - [ ] Uplod Configuration


## Authors

* **Peyton Creery** - *Initial work* - [Twinsphotography](https://twinsphotography.net)
