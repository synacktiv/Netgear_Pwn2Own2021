# Netgear R6700v3 WAN RCE - Pwn2Own 2021

This is the code used during Pwn2Own 2021 to get a remote shell
on the Netgear R6700v3.

Blogpost: https://synacktiv.com/publications/pwn2own-austin-2021-defeating-the-netgear-r6700v3

## Requirements

- `python3` with `flask`
- `dnsmasq`

## Usage

1. Run as root `./play.sh ifname` with `ifname` equal to the interface name which is connected to the router (e.g. `eth0`)
2. Boot the router
3. Wait for remote shell

