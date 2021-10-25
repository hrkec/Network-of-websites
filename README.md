## Network of websites

This repository contains solution for Memgraph <i>solutions engineering task</i> <b>Network of Websites</b>.

### Task
The task is to build a command-line script in Python that will be able to get all website page links from starting website ```START_URL``` with a max depth of ```DEPTH```. The network of all website URLs should be stored in the Memgraph database. The script should also be able to find the shortest path from ```START_URL``` to ```END_URL``` from a scraped network of websites in the Memgraph database.

#### a) Definition
```$ python main.py network START_URL [--depth | -d DEPTH]```

```$ python main.py path START_URL END_URL```

#### Example
```$ python main.py network https://memgraph.com --depth 3```

```$ python main.py path https://memgraph.com https://www.facebook.com/memgraph/videos/231540888355508/```
```
Shortest Path: 2
0 - https://memgraph.com
1 - https://www.facebook.com/memgraph/
2 - https://www.facebook.com/memgraph/videos/231540888355508/
```
#### Service
- Default ```DEPTH``` is 2
- ```WebsiteNotFoundError(URL)``` error is raised if ```START_URL``` doesn't exist when scraping for network
- ```WebsiteNotFoundError(URL)``` error is raised if ```START_URL``` or ```END_URL``` doesn't exist in Memgraph database when fetching shortest path
- ```ShortestPathNotFoundError``` error is raised if there is no path between ```START_URL``` and ```END_URL```

#### Prerequisites
- Memgraph package that can be downloaded <a href="https://memgraph.com/download"> here</a>.
- To run this solution you will need <b>Python, Make, CMake</b>.
- Memgraph's Python library, <b><a href="https://github.com/memgraph/pymgclient">pymgclient</a></b>, which currently only works on Linux-based system.
- Additional Python dependencies and version requirements can be seen in ```requirements.txt```.

To install and build mgclient library:
```
apt-get install cmake

git clone https://github.com/memgraph/mgclient.git /mgclient
cd mgclient && \
  mkdir build && \
  cd build && \
  cmake .. && \
  make && \
  make install
```

To install additional Python dependencies:
```pip install -r requirements.txt```
