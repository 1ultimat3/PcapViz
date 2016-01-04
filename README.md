# PcapViz
PcapViz visualizes network topologies and provides graph statistics based on pcap files.

## Features
- Draw network topologies (Layer 2) and communication graphs (Layer 3)
- Collect statistics such as most frequently contacted machines

## Example
Example pcap: [smallFlows.pcap](http://tcpreplay.appneta.com/wiki/captures.html#smallflows-pcap)

Drawing a communication graph (Layer 3):
```python
python main.py -i smallFlows.pcap -o small_tcp.png --layer3
```
![](https://gentle-wave-6212.herokuapp.com/static/pcapviz/0_small_tcp.png)

Return most frequently contacted hosts:
```python
python main.py -i smallFlows.pcap --layer3 --frequent

242 172.16.255.1
144 192.168.3.131
43 10.0.2.15
4 65.55.15.244
4 192.168.3.90
2 65.55.25.60
2 95.86.252.198
2 24.192.137.36
2 184.24.133.32
...
````

## 