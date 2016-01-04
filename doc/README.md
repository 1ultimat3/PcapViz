# Project Notes

## Objective
PcapViz aims to gather and visualize information from existing pcap files with respect to:
 
 * basic statistic information about nodes, connections and traffic
    
    * most frequently contacted nodes
    * most outgoing connections
    * most outgoing traffic
    * most incoming connections
    * most incoming traffic
  
 * information about protocols and content 
 * enrich nodes with further information such as
 	
 	  *  geo locations
 	  *  virus total IP information 
  * comparing samples against white listed ones
  * NEW timeline of traffic/network behaviour? (dynamic graph)
 	  

PcapViz is not suited for:
 
  * querying data or interacting with the results
  * perform real-time analysis
  * storing and merging multiple results
  * big datasets (single threaded etc.)
  
  
## Use Cases
A potential use case is

1. understanding how participating network peers communicate and which protocols are used.
2. quickly identifying malicious traffic or data leakage by comparing some samples against white listed ones.



