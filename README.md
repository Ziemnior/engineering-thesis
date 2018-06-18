# Engineering Thesis


__Thesis itself:__ use of RFID reader in the system for recording and monitoring work time


In this repository, one can find three main componenents: website that acts as user-friendly interface for employers and can be used to monitor employees worktime and their salary, code, that deployed on Raspberry Pi, transforms it into RFID sensor and gateway, which is used as access point for group of sensors, coupling them as one logical unit (With scope being one room, one floor, one building, etc, depending on deployment).

Pieces of code for mentioned componenents are scatered across multiple branches, with following being newest revisions:
* *introduce-rfid-reader* for **sensor**
* *introduce-mqtt-connection* for **gateway**
* and *preferences* for **website**


The thesis was written in Python **entirely**, as far as the code goes. For network part, I also used _dnsmasq_ and _hostapd_.

Note: function used for calculating business hours comes from [this](https://github.com/dnel/BusinessHours) repository and was only slightly modified to suit my needs.
