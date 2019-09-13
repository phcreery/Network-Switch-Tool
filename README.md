# Network-Switch-Tool
Automation tool to perform tasks on Network Switches and Routers

## Getting Started

This small script helps with wiping Cisco Network Switches to factory defaults and clearing any configs or vlans. It can also do ASA devices and routers.

It currently supports:
 - Cisco Catalyst 2900-3700 switches
 - Cisco 1800/1841 & 2900 Router
 - Cisco ASA 5515-5520
 
 with the following actions:
  - Wipe/Factory Reset

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
 - [ ] Upload Configuration

## Disclaimer

THE SAMPLE CODE ON https://github.com/phcreery/Network-Switch-Tool IS PROVIDED “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL phcreery OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ARISING IN ANY WAY OUT OF THE USE OF THIS SAMPLE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Authors

* **Peyton Creery** - *Initial work* - [Twinsphotography](https://twinsphotography.net)
