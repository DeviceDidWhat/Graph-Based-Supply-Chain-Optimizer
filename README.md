# 🚚 Advanced Graph-Based Supply Chain Optimizer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.0%2B-orange.svg)](https://networkx.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)

A powerful, interactive supply chain optimization system that demonstrates real-world applications of graph theory and optimization algorithms. This project showcases how classical algorithms solve complex logistics problems through an intuitive web interface.

![Supply Chain Network](https://img.shields.io/badge/Network-29_Nodes_|_80+_Edges-brightgreen)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Algorithms Implemented](#algorithms-implemented)
- [Network Architecture](#network-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Real-World Applications](#real-world-applications)
- [Technical Details](#technical-details)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project models a **complex multi-tier supply chain network** and provides tools to optimize routing, assignment, and resilience. It's designed to demonstrate how graph theory concepts taught in computer science courses apply to real-world logistics challenges.

### Why This Project?

- **Educational**: Clear implementation of Dijkstra's, Hungarian, and Network Flow algorithms
- **Practical**: Solves real supply chain problems like route optimization and failure recovery
- **Interactive**: Streamlit-based UI makes complex algorithms accessible
- **Scalable**: Modular design allows easy expansion of the network

---

## ✨ Key Features

### 🔄 **1. Optimal Assignment (Hungarian Algorithm)**
- Minimizes total cost of supplier-to-warehouse assignments
- Solves the classic assignment problem in O(n³) time
- Shows cost savings vs. random assignment

### 🗺️ **2. Shortest Path Routing (Dijkstra's Algorithm)**
- Finds optimal routes between any two nodes
- Supports multi-tier routing (Supplier → Warehouse → Distribution → Hub → Store)
- Real-time path visualization with cost breakdown

### 🔀 **3. Alternative Route Analysis**
- Discovers up to K shortest paths between nodes
- Provides backup routes for operational flexibility
- Side-by-side cost comparison

### ⚠️ **4. Network Resilience Testing**
- Simulates node failures (equipment breakdown, natural disasters)
- Automatic rerouting around failed nodes
- Quantifies connectivity loss percentage

### 🎯 **5. Critical Node Identification**
- Uses betweenness centrality to find network bottlenecks
- Identifies single points of failure
- Helps prioritize infrastructure investments

### 📊 **6. Comprehensive Analytics**
- Network connectivity metrics
- Path efficiency analysis
- Cost distribution statistics
- Node importance rankings

---

## 🧮 Algorithms Implemented

### 1. **Dijkstra's Shortest Path Algorithm**
```python
def find_shortest_path(G, start_node, end_node):
    """
    Finds minimum cost path using Dijkstra's algorithm.
    Time Complexity: O((V + E) log V)
    """
    path = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
    cost = nx.dijkstra_path_length(G, source=start_node, target=end_node, weight='weight')
    return path, cost
```

**Use Case**: Finding the cheapest route to transport goods from supplier to store.

---

### 2. **Hungarian Algorithm (Kuhn-Munkres)**
```python
def find_optimal_assignment(G):
    """
    Solves minimum cost bipartite matching.
    Time Complexity: O(n³)
    """
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return assignments, total_cost
```

**Use Case**: Optimally pairing suppliers with warehouses to minimize total shipping cost.

---

### 3. **Yen's K-Shortest Paths**
```python
def find_k_shortest_paths(G, start_node, end_node, k=3):
    """
    Finds K shortest simple paths.
    Useful for backup routing.
    """
    for path in nx.shortest_simple_paths(G, start_node, end_node, weight='weight'):
        # Returns top K paths
```

**Use Case**: Providing alternative routes when primary path is congested or blocked.

---

### 4. **Betweenness Centrality**
```python
def find_critical_nodes(G, top_n=5):
    """
    Identifies nodes that appear in most shortest paths.
    Reveals network bottlenecks.
    """
    betweenness = nx.betweenness_centrality(G, weight='weight')
    return sorted_nodes
```

**Use Case**: Identifying which warehouses/hubs are most critical to network function.

---

### 5. **Maximum Flow (Ford-Fulkerson)**
```python
def calculate_network_flow(G, source_nodes, sink_nodes):
    """
    Computes maximum throughput capacity.
    Time Complexity: O(V * E²)
    """
    flow_value = nx.maximum_flow_value(G_flow, 'super_source', 'super_sink')
    return flow_value
```

**Use Case**: Determining maximum daily shipment capacity through the network.

---

## 🏗️ Network Architecture

### Network Structure (5-Tier Supply Chain)

```
Suppliers (6 nodes)
    ↓
Warehouses (5 nodes)
    ↓
Distribution Centers (4 nodes)
    ↓
Hubs (4 nodes)
    ↓
Stores (10 nodes)
```

### Network Statistics
- **Total Nodes**: 29
- **Total Edges**: 80+
- **Direct Routes**: 6 (for redundancy)
- **Cross-Connections**: 7 (alternative paths)
- **Average Node Degree**: ~5.5

### Edge Weights
- Represent **cost** of transportation between nodes
- Range: $4 - $28
- Based on distance, shipping fees, and handling costs

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/supply-chain-optimizer.git
cd supply-chain-optimizer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

#### Option A: Streamlit Web App (Recommended)
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

#### Option B: Command Line Interface
```bash
python optimizer.py
```

---

## 📦 Requirements

Create a `requirements.txt` file:

```txt
networkx>=3.0
matplotlib>=3.5.0
numpy>=1.21.0
scipy>=1.7.0
streamlit>=1.28.0
pandas>=1.3.0
```

---

## 💻 Usage

### 1. **Web Interface (Streamlit)**

#### Finding Optimal Routes
1. Navigate to **"Routing"** tab
2. Select start node (Supplier/Warehouse/Distribution Center)
3. Select end node (Store/Hub/Distribution Center)
4. Click **"Find Shortest"** to compute optimal path
5. View cost breakdown and visualization

#### Testing Network Resilience
1. Go to **"Resilience"** tab
2. Select a node to simulate failure
3. Click **"Test Resilience"**
4. System automatically reroutes and shows impact metrics

#### Assignment Optimization
1. Open **"Assignment"** tab
2. Click **"Compute Optimal Assignment"**
3. View supplier-warehouse pairings with costs
4. See total savings vs random assignment

---

### 2. **Command Line Interface**

```python
from optimizer import build_graph, find_shortest_path

# Build network
G = build_graph()

# Find shortest path
path, cost = find_shortest_path(G, "S1", "R10")
print(f"Path: {' → '.join(path)}")
print(f"Cost: ${cost}")
```

---

## 📁 Project Structure

```
supply-chain-optimizer/
│
├── optimizer.py              # Core algorithms & graph building
├── app.py                    # Streamlit web interface
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── assets/                   # Screenshots & diagrams (optional)
│   ├── network_viz.png
│   └── dashboard.png
│
└── tests/                    # Unit tests (optional)
    ├── test_algorithms.py
    └── test_graph.py
```

---

## 🌍 Real-World Applications

### 1. **E-Commerce Logistics**
Companies like Amazon use similar graph-based systems to:
- Route packages through fulfillment centers
- Optimize warehouse-to-delivery-station assignments
- Handle delivery failures with automatic rerouting

### 2. **Manufacturing Supply Chain**
- Raw material sourcing optimization
- Factory-to-distributor cost minimization
- Production scheduling based on network capacity

### 3. **Disaster Response**
- Emergency supply distribution
- Hospital-to-patient routing during crises
- Identifying critical infrastructure for protection

### 4. **Transportation Networks**
- Airline route optimization
- Trucking fleet management
- Railway cargo scheduling

---

## 🔧 Technical Details

### Graph Representation
- **Type**: Directed Weighted Graph (DiGraph)
- **Implementation**: NetworkX library
- **Storage**: Adjacency list for O(1) edge lookups

### Node Attributes
```python
{
    'node_id': 'W1',
    'type': 'warehouse',  # supplier, warehouse, distribution, hub, store
    'capacity': 1000,     # Optional: max throughput
    'location': (x, y)    # Optional: geographic coordinates
}
```

### Edge Attributes
```python
{
    'weight': 15,         # Transportation cost
    'capacity': 100,      # Optional: max flow
    'distance': 250       # Optional: physical distance
}
```

### Visualization Layout
- **Algorithm**: Semantic Layered Layout
- **Approach**: Nodes grouped by type in vertical layers
- **Spacing**: Prevents overlap with dynamic gap calculation

---

## 📊 Performance Metrics

### Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Use Case |
|-----------|----------------|------------------|----------|
| Dijkstra | O((V+E) log V) | O(V) | Shortest path |
| Hungarian | O(n³) | O(n²) | Assignment |
| Betweenness | O(V·E) | O(V+E) | Critical nodes |
| Max Flow | O(V·E²) | O(V+E) | Capacity |
| K-Shortest | O(K·V·(E+V log V)) | O(V+E) | Alternatives |

### Network Size Limits
- **Current**: 29 nodes, 80 edges
- **Tested**: Up to 100 nodes, 500 edges
- **Recommended**: < 500 nodes for real-time visualization

---

## 📸 Screenshots

### Main Dashboard
![Dashboard](assets/dashboard.png)
*Interactive control panel with 4 operation modes*

### Network Visualization
![Network](assets/network_viz.png)
*Layered graph showing optimal route from S1 to R10*

### Resilience Testing
![Resilience](assets/resilience.png)
*Impact analysis of D2 node failure*

---

## 🎓 Educational Value

### Concepts Demonstrated

1. **Graph Theory**
   - Directed graphs
   - Weighted edges
   - Path finding
   - Network flow

2. **Algorithm Design**
   - Greedy algorithms (Dijkstra)
   - Dynamic programming (Hungarian)
   - Centrality measures
   - Optimization techniques

3. **Data Structures**
   - Priority queues
   - Adjacency lists
   - Cost matrices
   - Path tracking

4. **Software Engineering**
   - Modular design
   - Separation of concerns
   - Interactive visualization
   - Error handling

---

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

### Ideas for Enhancement
- [ ] Add time-based routing (considering traffic/delays)
- [ ] Implement genetic algorithms for global optimization
- [ ] Add machine learning for demand prediction
- [ ] Create 3D visualization with geographic mapping
- [ ] Support for multi-commodity flow problems
- [ ] Real-time data integration (live traffic, weather)

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **NetworkX**: For excellent graph algorithms library
- **Streamlit**: For making interactive web apps simple
- **SciPy**: For optimization algorithms
- Course materials from [Your University/Course Name]

---

## 📚 References

### Academic Papers
1. Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
2. Kuhn, H. W. (1955). "The Hungarian method for the assignment problem"
3. Freeman, L. C. (1977). "A set of measures of centrality based on betweenness"

### Books
- "Introduction to Algorithms" - Cormen, Leiserson, Rivest, Stein
- "Network Science" - Albert-László Barabási
- "Supply Chain Management" - Sunil Chopra, Peter Meindl

### Online Resources
- [NetworkX Documentation](https://networkx.org/documentation/)
- [Graph Theory Tutorial](https://www.tutorialspoint.com/graph_theory/)
- [Supply Chain Optimization Guide](https://www.supplychainbrain.com/)

---

## 🐛 Known Issues

- Large networks (>200 nodes) may cause slow visualization rendering
- Edge label overlapping in dense graph regions
- Path finding may timeout on disconnected subgraphs

See [Issues](https://github.com/yourusername/supply-chain-optimizer/issues) for full list.

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Geographic mapping with real coordinates
- [ ] Time-window constraints for deliveries
- [ ] Multi-objective optimization (cost + time + emissions)
- [ ] Historical data analysis and forecasting
- [ ] REST API for external integration

### Version 3.0 (Future)
- [ ] Machine learning for demand prediction
- [ ] Real-time IoT sensor integration
- [ ] Blockchain for supply chain transparency
- [ ] Mobile app for field operators

---

## 💡 Tips & Best Practices

### For Students
- Start with `optimizer.py` to understand the core algorithms
- Modify edge weights to see how routes change
- Add new nodes to expand the network
- Try implementing Bellman-Ford as an alternative to Dijkstra

### For Developers
- Use the modular structure to add new optimization algorithms
- Extend node attributes for domain-specific features
- Implement caching for frequently computed paths
- Add unit tests for reliability

### For Researchers
- Integrate real supply chain datasets
- Compare different routing algorithms
- Study network resilience under various failure scenarios
- Publish findings using this framework

---

## ❓ FAQ

**Q: Can I use this for my company's actual supply chain?**
A: This is an educational prototype. For production use, consider enterprise solutions or extensive testing.

**Q: How do I add more nodes?**
A: Edit the `build_graph()` function in `optimizer.py` to add nodes and edges.

**Q: What if I want to optimize for time instead of cost?**
A: Change edge weights to represent time. The algorithms work the same way!

**Q: Can this handle cyclic routes?**
A: Yes, Dijkstra's algorithm handles cycles correctly. However, K-shortest paths finds only simple paths (no cycles).

**Q: How accurate is the resilience testing?**
A: It accurately models static network disruption. Real-world factors like partial capacity loss aren't modeled.

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/supply-chain-optimizer&type=Date)](https://star-history.com/#yourusername/supply-chain-optimizer&Date)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/supply-chain-optimizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/supply-chain-optimizer/discussions)
- **Email**: support@yourproject.com

---

<div align="center">

**Built with ❤️ for the supply chain optimization community**
[⬆ Back to Top](#-advanced-graph-based-supply-chain-optimizer)

</div>
