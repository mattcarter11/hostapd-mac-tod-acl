# A brief explanation
This script provides a quick way to setup a Time-of-day (Tod) Access Control List (ACL) for a Hostapd Wifi Access Point.

It uses the *hostapd-cli*'s whitelist to only allow certain MAC addresses to join the AP.

# Setup
The following

	1. Install python 3 or above & *hostapd*
	2. Make a Wifi AP with *hostapd*, enable *hostapd_cli* and MAC whitelist by adding to the config:
	
	        macaddr_acl=0
	        accept_mac_file=/etc/hostapd/hostapd.accept
	        ctrl_interface=/var/run/hostapd
	        ctrl_interface_group=0
	
	3. Place the following files inside */etc/hostapd/*:
		- hostapd.accept
		- mac-time-of-day-acces.py
	
	4. Configure crontab (`$ sudo crontab -u root -e`) with the following rule:
		
	        * * * * * python /etc/hostapd/mac-time-of-day-access.py
	
	5. Set your time of day MAC based filters with the file *mac-time-filter.json*
		
# mac-time-filter.json 
## Format
```json
{
	"mac": [
		["start (H:M:S)", "end (H:M:S)"],
		…
	],
	…
}
```

## Example
```json
{
	"48:01:C5:76:14:53": [
		["10:00:00","12:00:00"],
		["16:00:00","21:30:00"]
	]
}
```