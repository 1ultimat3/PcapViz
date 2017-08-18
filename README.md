# PcapViz
PcapViz visualizes network topologies and provides graph statistics based on pcap files.
It should be possible to determine key topological nodes or data exfiltration attempts more easily.

## Features
- Draw network topologies (Layer 2) and communication graphs (Layer 3 and 4)
- Network topologies contain country information and connection stats
- Collect statistics such as most frequently contacted machines

## Usage
```
usage: main.py [-h] [-i [PCAPS [PCAPS ...]]] [-o OUT] [-g GRAPHVIZ] [--layer2]
               [--layer3] [--layer4] [-fi] [-fo]

pcap topology drawer

optional arguments:
  -h, --help            show this help message and exit
  -i [PCAPS [PCAPS ...]], --pcaps [PCAPS [PCAPS ...]]
                        capture files
  -o OUT, --out OUT     topology will be stored in the specified file
  -g GRAPHVIZ, --graphviz GRAPHVIZ
                        graph will be exported to the specified file (dot
                        format)
  --layer2              derive layer2 topology
  --layer3              derive layer3 topology
  --layer4              derive layer4 topology
  -fi, --frequent-in    print frequently contacted nodes to stdout
  -fo, --frequent-out   print frequent source nodes to stdout
```

## Example
Example pcap: [smallFlows.pcap](http://tcpreplay.appneta.com/wiki/captures.html#smallflows-pcap)

Drawing a communication graph (layer 2), segment:
```
python main.py -i smallFlows.pcap -o small_tcp_l2.png --layer2
```
![](https://gentle-wave-6212.herokuapp.com/static/pcapviz/layer2.png)

Drawing a communication graph (layer 3), segment:
```
python main.py -i smallFlows.pcap -o small_tcp.png --layer3
```
![](https://gentle-wave-6212.herokuapp.com/static/pcapviz/layer3.png)

Drawing a communication graph (layer 4), segment:
```
python main.py -i smallFlows.pcap -o small_tcp_l4.png --layer4
```
![](https://gentle-wave-6212.herokuapp.com/static/pcapviz/layer4.png)

Return most frequently contacted hosts:
```
python main.py -i smallFlows.pcap --layer3 --frequent-in

115 172.16.255.1
70 192.168.3.131
21 10.0.2.15
2 65.55.15.244
2 224.0.0.252
2 192.168.3.90
2 239.255.255.250
2 255.255.255.255
1 178.144.253.171
1 92.247.222.20
1 72.14.213.103
1 67.170.187.174
...
````

## Installation

Required:
 
 * GraphViz
 * Download GeoIP database to ~/GeoIP.dat (http://dev.maxmind.com/geoip/legacy/install/country/)

In case you are using python3 install the following requirements:

```
pip install -r requirements.txt
```

Python2.x requirements can be installed as follows:

```
pip install -r requirements_python2.txt
```

### Installation Debian

For Debian-based distros you have to install GraphViz with some additional dependencies:

```
apt-get install python3-dev
apt-get install graphviz libgraphviz-dev pkg-config
```

### Installation OSX

Scapy does not work out-of-the-box on OSX. Follow the platform specific instruction from the [scapy website](http://scapy.readthedocs.io/en/latest/installation.html#platform-specific-instructions)

```
brew install graphviz
brew install --with-python libdnet
brew install https://raw.githubusercontent.com/secdev/scapy/master/.travis/pylibpcap.rb
```


