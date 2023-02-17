# PcapViz
PcapViz draws networks as device topologies and as information flows using the packet information in pcap files captured from a network
device using tcpcap or other capture software. It filters and optionally displays the captured packets at any one of 3 "layers". These are:

 - device level traffic topology, 
 - ip communication and 
 - tcp/udp communication 

Each yields a distinct network graph from the same set of network packets. This separation makies it much easier to see the data flows at each level rather than mixing them up 
as many other visualisation packages do. It should be possible to determine key topological nodes or to spot patterns of data exfiltration attempts more easily.


## Features
- Network topology graphs - 2 = device; conversation information flow graphs: 3 = ip, 4 = tcp/udp
- Communication graph node labels show country information and connection stats
- Lists the most frequently contacted and frequently sending machines
- Node labels include the host domain name if available from a reverse DNS lookup. 
- command line choice of Graphviz graph layout engine such as dot or sfdp.


## Usage

```
usage: main.py [-h] [-i [PCAPS [PCAPS ...]]] [-o OUT] [-g GRAPHVIZ] [--layer2]
               [--layer3] [--layer4] [-fi] [-fo] [-G GEOPATH] [-l GEOLANG]
               [-E LAYOUTENGINE] [-s SHAPE]

pcap topology and message mapper

optional arguments:
  -h, --help            show this help message and exit
  -i [PCAPS [PCAPS ...]], --pcaps [PCAPS [PCAPS ...]]
                        space delimited list of capture files to be analyzed
  -o OUT, --out OUT     topology will be stored in the specified file
  -g GRAPHVIZ, --graphviz GRAPHVIZ
                        graph will be exported to the specified file (dot
                        format)
  --layer2              device topology network graph
  --layer3              ip message graph. Default
  --layer4              tcp/udp message graph
  -fi, --frequent-in    print frequently contacted nodes to stdout
  -fo, --frequent-out   print frequent source nodes to stdout
  -G GEOPATH, --geopath GEOPATH
                        path to maxmind geodb data
  -l GEOLANG, --geolang GEOLANG
                        Language to use for geoIP names
  -E LAYOUTENGINE, --layoutengine LAYOUTENGINE
                        Graph layout method - dot, sfdp etc.
  -s SHAPE, --shape SHAPE
                        Graphviz node shape - circle, diamond, box etc.
```

## Examples from running tests/core.py on the test.pcap file

**Drawing a communication graph (layer 2), segment**
```
python main.py -i tests/test.pcap -o test2.png --layer2
```

![layer 2 sample](tests/test2.png)

**Layer3 with default sfdp layout**

![layer 3 sample](tests/test3.png)

**Layer4 with default sfdp layout**

![layer 4 sample](tests/test4.png)


Return hosts with largest numbers of incoming packets:

```
python3 main.py -i tests/test.pcap -fi --layer3
4 172.16.11.12
1 74.125.19.17
1 216.34.181.45 slashdot.org
1 172.16.11.1
1 96.17.211.172 a96-17-211-172.deploy.static.akamaitechnologies.com

```

## Installation

**Required:**
 
 * GraphViz
     See system notes below
     
 * Pip package requirements
    The Maxmind Python API and other dependencies will be installed when you run:
	
	```
	pip3 install -r requirements.txt
	```

	so of course, please run that! You are using a python virtual environment aren't you?
 
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

## Testing

Unit tests can be run from the tests directory:
```
python3 core.py
```
The sample images above are the test output graphs.

Note that there are at present 2 warnings about deprecated features in graphviz and for tests to work, you may need to adjust the fake args to point to your copy of the geoIP data file.
Without access to the geoIP data, two of the tests will always fail.

## Acknowledgement
Maxmind ask that this be included - even though we do not distribute the data here it is...

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.
