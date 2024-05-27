CloudTunnelVis - Cisco Tunnel Monitor (README.md)
Project Overview

CloudTunnelVis is a Python-based tool that leverages Nornir to automate the collection and display of tunnel information from Cisco devices. This initial phase focuses on parsing GRE over IPSec tunnel details like status, uptime, and traffic.

Requirements

Python 3.x
Nornir (https://nornir.readthedocs.io/)
TextFSM (https://github.com/google/textfsm/wiki/TextFSM) (optional, for structured parsing)

Usage

Run the script using nornir --inventory inventory.yml parse_tunnel_info.py.
Output

The script will print the extracted tunnel information (name, status, uptime, traffic) for each device in your Nornir inventory.
