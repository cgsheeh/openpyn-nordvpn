# openpyn
A python3 script/systemd service, to easily connect to and switch between, OpenVPN servers hosted by NordVPN. Quickly Connect to the least busy servers (using current data from Nordvpn's website) with lowest latency from you. Find servers in a specific country or even a city. It Tunnels DNS traffic through the VPN which normally (when using OpenVPN with NordVPN) goes through your ISP's DNS (still unencrypted, even if you use a third party) and completely compromises Privacy!

## Features
* Automatically connect to least busy, low latency servers in a given country.
* Systemd inegration, easy to check VPN status, autostart at startup.
* Find and connect to servers in a specific city or state.
* Uses NordVPN's DNS servers and tunnels DNS queries through the VPN Tunnel.
* Use Iptables rules to prevent IP leakage if tunnel breaks (Experimental).
* Quickly Connect to any specific server. i.e au10 or us20.
* Downloads and Updates (modifications) the latest config files from NordVPN.
* Option to run the script in background (openvpn daemon mode).
* Options to finetune server selection based on "Server Load" or "Ping Latency".
* Auto excludes the servers if ping to them fails or if they don't support OpenVPN \
  (TCP or UDP depending upon which one you are trying to use).
* Finds and displays nord vpn servers (with extra info) in a given country.
* Now list and connect to servers with "Netflix" --netflix, "Peer To Peer" --p2p, "Dedicated IP" --dedicated, \
"Tor Over VPN" --tor, "Double VPN" --double, "Anti DDos" --anti-ddos support.
* Desktop notification are shown when VPN connects and disconnects. (needs to run without sudo)
* Auto retry if [soft,auth-failure] received, auto failover to next best server if connection dies. (not in daemon mode)
* NVRAM write support for Asuswrt-merlin
* Pass through openvpn options, e.g. openpyn uk -o '--status /var/log/status.log --log /var/log/log.log'

## Dependencies

Requires OpenVPN, Ubuntu 17.10, Python 3.6

### Installation Methods

```bash
$ sudo apt install openvpn
(venv) $ python setup.py install 
```

Click requires setuptools integration.

### Usage

Run

```bash
$ nordvpn --help
```

for a list of commands. Read more about each command and it's options with

```bash
$ nordvpn command --help
```

Add subcommands and append ```--help``` to see more about subcommands.

## Completed
- Connect via OpenVPN
- Kill running OpenVPN process
- See list of available countries
- See information about servers


## To Do
- TESTS (Docker and Python tests)
- Try and break, handle exceptions
- Filter servers by special features (display as well)
- LastPass integration
- Desktop notifications
- Re-examine "config" module
- create a combined config of multiple servers (on the fly) for auto failover
- Find optimal server by default
- Find closest servers (ie do something with the lat and long values)
- systemd integration
- i3pystatus module (or maybe just add vpn module if it exists)
- Store profiles
