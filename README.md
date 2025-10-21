# 🚚 Advanced Graph-Based Supply Chain Optimizer

A powerful, interactive supply chain network optimization tool built with Python, NetworkX, and Streamlit. This application demonstrates advanced graph algorithms for real-world logistics and supply chain management problems.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![NetworkX](https://img.shields.io/badge/NetworkX-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Network Architecture](#network-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithms](#algorithms)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a comprehensive supply chain optimization system using graph theory and advanced algorithms. It provides an interactive web interface for visualizing complex supply networks, finding optimal routes, calculating minimum-cost assignments, and simulating dynamic rerouting scenarios.

### Key Capabilities:
- **29-node complex network** with 80+ connections
- **Real-time path optimization** using Dijkstra's algorithm
- **Optimal supplier-warehouse assignment** using Hungarian algorithm
- **Dynamic failure recovery** and rerouting
- **Interactive visualization** with layer-based network layout
- **Comprehensive network analytics** and metrics

## ✨ Features

### 1. **Optimal Assignment Problem**
- Solves the supplier-to-warehouse assignment problem
- Uses the Hungarian Algorithm for minimum cost matching
- Displays optimal assignments with cost breakdown
- Time complexity: O(n³)

### 2. **Shortest Path Finding**
- Finds the minimum cost path between any two nodes
- Implements Dijkstra's algorithm with weighted edges
- Supports routing from Suppliers, Warehouses, or Distribution Centers
- Visual path highlighting on the network graph

### 3. **Dynamic Rerouting**
- Simulates node failures in the network
- Automatically finds alternative routes
- Shows cost impact and efficiency metrics
- Demonstrates network resilience and redundancy

### 4. **Network Visualization**
- Clean, non-overlapping 5-layer layout
- Color-coded nodes by type:
  - 🟢 **Green** - Suppliers
  - 🔵 **Blue** - Warehouses
  - 🟠 **Orange** - Distribution Centers
  - 🟣 **Purple** - Hubs
  - 🟡 **Yellow** - Stores
  - 🔴 **Red** - Active Path
- Interactive legend and cost labels
- Real-time graph updates

### 5. **Advanced Analytics**
- Network connectivity analysis
- Critical node identification (betweenness centrality)
- Redundancy and alternative path analysis
- Cost statistics (min, max, average)
- Route efficiency metrics

## 🏗️ Network Architecture

```
Layer 1: Suppliers (6)
    ↓
Layer 2: Warehouses (5)
    ↓
Layer 3: Distribution Centers (4)
    ↓
Layer 4: Hubs (4)
    ↓
Layer 5: Stores (10)
```

**Total Network:**
- **Nodes:** 29
- **Edges:** 80+
- **Connectivity:** ~95% supplier-to-store reachability
- **Redundancy:** Multiple alternative paths for most routes

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/supply-chain-optimizer.git
cd supply-chain-optimizer
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📦 Requirements

Create a `requirements.txt` file with:

```txt
streamlit>=1.28.0
networkx>=3.0
matplotlib>=3.7.0
numpy>=1.24.0
scipy>=1.10.0
```

## 💻 Usage

### Running the Standalone Optimizer
```bash
python optimizer.py
```

This will:
- Build the supply chain network
- Run optimal assignment calculations
- Find shortest paths
- Simulate node failures
- Display network visualization

### Running the Interactive Web App
```bash
streamlit run app.py
```

### Basic Workflow:

1. **View the Network**
   - Open the app to see the full supply chain visualization
   - Review network statistics in the top metrics panel

2. **Optimal Assignment**
   - Click "Run Supplier → Warehouse Assignment"
   - View optimal pairings and total cost

3. **Find Shortest Path**
   - Select a start node (Supplier/Warehouse/Distribution Center)
   - Select an end node (Store)
   - Click "Calculate Shortest Path"
   - View the highlighted route and cost breakdown

4. **Simulate Failures**
   - Select a node to disable
   - Click "Find Alternative Route"
   - Compare costs before and after failure

5. **Analyze Network**
   - Expand "Network Statistics & Analysis"
   - Review connectivity, redundancy, and critical nodes

## 🧮 Algorithms

### 1. Hungarian Algorithm (Optimal Assignment)
- **Purpose:** Minimum cost bipartite matching
- **Complexity:** O(n³)
- **Use Case:** Assigning suppliers to warehouses optimally
- **Implementation:** `scipy.optimize.linear_sum_assignment`

### 2. Dijkstra's Algorithm (Shortest Path)
- **Purpose:** Single-source shortest path with non-negative weights
- **Complexity:** O((V + E) log V) with binary heap
- **Use Case:** Finding minimum cost routes in the supply chain
- **Implementation:** `networkx.dijkstra_path`

### 3. Betweenness Centrality (Critical Nodes)
- **Purpose:** Identify nodes that are most critical to network flow
- **Complexity:** O(VE) for unweighted graphs
- **Use Case:** Finding bottlenecks and critical infrastructure
- **Implementation:** `networkx.betweenness_centrality`

## 📁 Project Structure

```
supply-chain-optimizer/
│
├── app.py                 # Streamlit web application
├── optimizer.py           # Core optimization logic and algorithms
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── assets/               # (Optional) Screenshots and images
│   ├── network_view.png
│   ├── path_finding.png
│   └── rerouting.png
│
└── tests/                # (Optional) Unit tests
    ├── test_optimizer.py
    └── test_algorithms.py
```

### File Descriptions:

**`optimizer.py`**
- Graph construction and network design
- Algorithm implementations
- Helper functions for layout and visualization
- Standalone testing and CLI interface

**`app.py`**
- Streamlit web interface
- Interactive controls and widgets
- Real-time graph visualization
- Analytics and metrics dashboard

## 📸 Screenshots

### Main Network View
*Full supply chain network with 5-layer architecture*

### Shortest Path Visualization
*Highlighted optimal route with cost breakdown*

### Dynamic Rerouting
*Alternative path after node failure simulation*

### Network Analytics
*Comprehensive statistics and critical node analysis*

## 🔧 Technical Details

### Graph Representation
- **Type:** Directed Weighted Graph (`DiGraph`)
- **Nodes:** Categorized by type (supplier, warehouse, distribution, hub, store)
- **Edges:** Weighted by transportation/logistics costs
- **Storage:** Adjacency list representation (NetworkX default)

### Layout Algorithm
- **Method:** Semantic layer-based positioning
- **Layers:** 5 horizontal layers with vertical spreading
- **Benefits:** No overlapping, clear flow visualization
- **Customizable:** Adjustable spacing and positioning

### Visualization
- **Library:** Matplotlib with NetworkX drawing functions
- **Figure Size:** 20x11 inches (optimized for wide displays)
- **Node Size:** 1800 units (scaled for visibility)
- **Edge Styling:** Arc-based curves with arrows
- **Color Scheme:** High-contrast, accessible colors

### Performance
- **Graph Building:** O(V + E) = O(29 + 80) = O(109)
- **Shortest Path:** O((V + E) log V) ≈ O(300)
- **Assignment:** O(n³) ≈ O(216) for 6 suppliers
- **Visualization:** O(V + E) for drawing
- **Total Runtime:** < 1 second for all operations

## 🎓 Use Cases

This project is ideal for:

### Education
- Teaching graph algorithms
- Demonstrating optimization problems
- Learning supply chain concepts
- Understanding network theory

### Research
- Supply chain modeling
- Logistics optimization
- Network resilience studies
- Algorithm comparison

### Industry Applications
- Distribution network planning
- Route optimization
- Failure recovery planning
- Cost analysis and reduction

## 🛠️ Customization

### Adding More Nodes
In `optimizer.py`, modify the `build_graph()` function:

```python
# Add more suppliers
[G.add_node(f"S{i}", type='supplier') for i in range(1, 10)]  # 9 suppliers

# Add custom edges
G.add_edge("S7", "W1", weight=25)
```

### Changing Costs
Modify edge weights in the graph construction:

```python
edges_s_w = [
    ("S1", "W1", 15),  # Changed from 10 to 15
    # ... more edges
]
```

### Adjusting Layout
In `compute_semantic_positions()`, modify spacing:

```python
spread(suppliers, x_pos=0, y_gap=3.0)  # Increase vertical spacing
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- Additional algorithms (A*, Bellman-Ford, Floyd-Warshall)
- More network metrics and analytics
- Export functionality (PDF, JSON, CSV)
- Multi-objective optimization
- Machine learning integration
- Performance optimizations
- Unit tests and documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- NetworkX library for graph algorithms
- Streamlit for the web framework
- SciPy for optimization functions
- Matplotlib for visualization
- The open-source community

## 📧 Contact

For questions or feedback:
- **Email:** your.email@example.com
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **LinkedIn:** [Your Name](https://linkedin.com/in/yourprofile)

## 🔗 Links

- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Hungarian Algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm)
- [Supply Chain Management](https://en.wikipedia.org/wiki/Supply_chain_management)

---

⭐ If you found this project helpful, please consider giving it a star!

**Made with ❤️ and Python**
