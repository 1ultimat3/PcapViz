# PcapViz
Visualize network topologies and collect graph statistics based on pcap files

## Features
- Draw network topology (Layer2)
- Draw communication graph (Layer3)
- Print frequently contacted machines

## Example
Example pcap: [smallFlows.pcap](http://tcpreplay.appneta.com/wiki/captures.html#bigflows-pcap)

```python
python main.py -i smallFlows.pcap -o small_tcp.png --layer3
```

![](http://sungli.de/static/pcapviz/0_small_tcp.png)