import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from optimizer import (
    build_graph, 
    find_optimal_assignment, 
    find_shortest_path, 
    get_node_colors,
    compute_semantic_positions
)

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Supply Chain Optimizer", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Title styling */
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        /* Make sidebar scrollable */
        section[data-testid="stSidebar"] {
            overflow-y: auto;
        }
        /* Add spacing between widgets */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        /* Reduce button overlap and margin issues */
        div.stButton > button {
            width: 100%;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        /* Make matplotlib figures larger */
        .stImage {
            max-width: 100% !important;
        }
        /* Metrics styling */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚚 Advanced Graph-Based Supply Chain Optimizer</p>', unsafe_allow_html=True)

# --- 1. Initialize Graph ---
@st.cache_resource
def initialize_graph():
    G = build_graph()
    pos = compute_semantic_positions(G)
    return G, pos

G, pos = initialize_graph()

# Separate node types
all_nodes = sorted(list(G.nodes()))
suppliers = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'supplier'])
warehouses = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'warehouse'])
distributions = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'distribution'])
hubs = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'hub'])
stores = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'store'])

# All possible start nodes (suppliers, warehouses, distributions)
start_nodes = sorted(suppliers + warehouses + distributions)
# All possible end nodes (stores)
end_nodes = stores


# --- 2. Graph Drawing Helper ---
def draw_graph(G, pos, path_nodes=None, title="Supply Chain Network"):
    """Draws graph with non-overlapping semantic layout."""
    fig, ax = plt.subplots(figsize=(20, 11))
    
    # Set background color
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8f9fa')

    # Colors and layout
    colors = get_node_colors(G, path=path_nodes)
    
    # Draw edges first (so they appear behind nodes)
    nx.draw_networkx_edges(
        G, pos,
        edge_color='#d0d0d0',
        width=1.5,
        arrows=True,
        arrowsize=15,
        arrowstyle='->',
        connectionstyle="arc3,rad=0.05",
        ax=ax,
        alpha=0.5
    )
    
    # Highlight path edges if exists
    if path_nodes and len(path_nodes) > 1:
        path_edges = list(zip(path_nodes, path_nodes[1:]))
        nx.draw_networkx_edges(
            G, pos, 
            edgelist=path_edges, 
            width=5, 
            edge_color="#e63946",
            arrows=True,
            arrowsize=30,
            arrowstyle='->',
            connectionstyle="arc3,rad=0.05",
            ax=ax,
            alpha=0.9
        )
    
    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_color=colors,
        node_size=1800,
        ax=ax,
        edgecolors='#2d2d2d',
        linewidths=2.5
    )
    
    # Draw labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=10,
        font_weight="bold",
        font_color='#000000',
        ax=ax
    )

    # Show edge weights (only for path edges to reduce clutter)
    if path_nodes and len(path_nodes) > 1:
        path_edges = list(zip(path_nodes, path_nodes[1:]))
        path_edge_labels = {edge: G[edge[0]][edge[1]]['weight'] for edge in path_edges if G.has_edge(edge[0], edge[1])}
        nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels=path_edge_labels, 
            font_size=11,
            font_color='#c92a2a',
            font_weight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#c92a2a', linewidth=2, alpha=0.95),
            ax=ax
        )
    else:
        # Show all edge weights for full network view
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels=edge_labels, 
            font_size=7,
            font_color='#495057',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.7),
            ax=ax
        )

    ax.set_title(title, fontsize=18, fontweight='bold', pad=25, color='#2d3436')
    ax.axis("off")
    
    # Add enhanced legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#51cf66', edgecolor='#2d2d2d', linewidth=2, label='Supplier (6)'),
        Patch(facecolor='#4dabf7', edgecolor='#2d2d2d', linewidth=2, label='Warehouse (5)'),
        Patch(facecolor='#ff922b', edgecolor='#2d2d2d', linewidth=2, label='Distribution Center (4)'),
        Patch(facecolor='#cc5de8', edgecolor='#2d2d2d', linewidth=2, label='Hub (4)'),
        Patch(facecolor='#ffd43b', edgecolor='#2d2d2d', linewidth=2, label='Store (10)'),
        Patch(facecolor='#ff6b6b', edgecolor='#2d2d2d', linewidth=2, label='Active Path')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.95, 
              edgecolor='#2d2d2d', fancybox=True, shadow=True)
    
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()


# --- 3. Initialize Session State ---
if 'current_path' not in st.session_state:
    st.session_state.current_path = None
if 'current_cost' not in st.session_state:
    st.session_state.current_cost = 0
if 'start_node' not in st.session_state:
    st.session_state.start_node = warehouses[0]
if 'end_node' not in st.session_state:
    st.session_state.end_node = stores[0]


# --- 4. Network Overview Statistics (Top Section) ---
st.markdown("---")
col_stat1, col_stat2, col_stat3, col_stat4, col_stat5, col_stat6 = st.columns(6)

with col_stat1:
    st.metric("🏭 Suppliers", len(suppliers))
with col_stat2:
    st.metric("📦 Warehouses", len(warehouses))
with col_stat3:
    st.metric("🚛 Distribution", len(distributions))
with col_stat4:
    st.metric("🔄 Hubs", len(hubs))
with col_stat5:
    st.metric("🏪 Stores", len(stores))
with col_stat6:
    st.metric("🔗 Connections", G.number_of_edges())

st.markdown("---")


# --- 5. UI Layout ---
col_sidebar, col_main = st.columns([1, 3], gap="large")

# --- Sidebar Controls ---
with col_sidebar:
    st.header("⚙️ Operations Control Panel")

    # --- A. Optimal Assignment ---
    st.subheader("1️⃣ Optimal Assignment")
    st.caption("Find minimum cost assignment using Hungarian Algorithm")
    
    if st.button("🔄 Run Supplier → Warehouse Assignment", use_container_width=True):
        with st.spinner("Computing optimal assignment..."):
            assignments, total_cost = find_optimal_assignment(G)
            st.success(f"✅ **Total Assignment Cost: ${total_cost:.0f}**")
            
            # Display in a nice format
            st.write("**📋 Optimal Assignments:**")
            for s, w in assignments:
                if G.has_edge(s, w):
                    cost = G[s][w]['weight']
                    st.write(f"• **{s}** ➜ **{w}** | Cost: `${cost}`")
            
            # Show savings
            max_possible = sum([G[s][w]['weight'] for s, w in assignments])
            st.info(f"💰 This is the optimal solution among all possible assignments!")
    
    st.divider()

    # --- B. Shortest Path ---
    st.subheader("2️⃣ Find Shortest Route")
    st.caption("Optimal path calculation using Dijkstra's algorithm")
    
    start_node = st.selectbox(
        "📍 Start Node:", 
        options=start_nodes,
        index=start_nodes.index(st.session_state.start_node) if st.session_state.start_node in start_nodes else 0,
        key='start_select',
        help="Select any Supplier, Warehouse, or Distribution Center"
    )
    st.session_state.start_node = start_node
    
    end_node = st.selectbox(
        "🎯 End Node (Store):", 
        options=end_nodes,
        index=end_nodes.index(st.session_state.end_node),
        key='end_select',
        help="Select destination store"
    )
    st.session_state.end_node = end_node

    if st.button("🔍 Calculate Shortest Path", use_container_width=True):
        with st.spinner("Finding optimal route..."):
            path, cost = find_shortest_path(G, start_node, end_node)
            if path:
                st.session_state.current_path = path
                st.session_state.current_cost = cost
                st.success("✅ **Optimal Path Found!**")
                st.info(f"**📍 Route:** {' → '.join(path)}")
                st.metric("💵 Total Cost", f"${cost}", delta=None)
                
                # Show path length
                st.caption(f"🛣️ Path includes {len(path)} nodes and {len(path)-1} connections")
            else:
                st.session_state.current_path = None
                st.error(f"❌ No path exists from **{start_node}** to **{end_node}**")
    
    st.divider()

    # --- C. Dynamic Rerouting ---
    st.subheader("3️⃣ Dynamic Rerouting")
    st.caption("Simulate failures and find alternative routes")
    
    broken_node = st.selectbox(
        "⚠️ Select node to disable:", 
        options=all_nodes,
        key='broken_select',
        help="Simulate a node failure in the network"
    )

    if st.button("🧭 Find Alternative Route", use_container_width=True):
        with st.spinner(f"Rerouting around {broken_node}..."):
            G_broken = G.copy()
            G_broken.remove_node(broken_node)
            
            path_new, cost_new = find_shortest_path(
                G_broken, 
                st.session_state.start_node, 
                st.session_state.end_node
            )

            if path_new:
                st.session_state.current_path = path_new
                st.session_state.current_cost = cost_new
                st.warning(f"⚠️ **Node `{broken_node}` bypassed successfully**")
                st.success("✅ **Alternative Path Found!**")
                st.info(f"**🔄 New Route:** {' → '.join(path_new)}")
                
                # Show cost comparison
                original_path, original_cost = find_shortest_path(
                    G, 
                    st.session_state.start_node, 
                    st.session_state.end_node
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if original_path:
                        st.metric("Original Cost", f"${original_cost:.0f}")
                    else:
                        st.metric("Original Cost", "N/A")
                with col2:
                    st.metric("New Cost", f"${cost_new:.0f}")
                
                if original_path and original_cost != cost_new:
                    diff = cost_new - original_cost
                    pct = (diff/original_cost)*100
                    st.metric("Cost Impact", f"${diff:+.0f}", delta=f"{pct:+.1f}%", delta_color="inverse")
            else:
                st.session_state.current_path = None
                st.error(f"❌ **No alternative path exists!**")
                st.warning(f"The network is disconnected after removing `{broken_node}`")
    
    # Clear path button
    st.divider()
    col_clear1, col_clear2 = st.columns(2)
    with col_clear1:
        if st.button("🗑️ Clear Path", use_container_width=True):
            st.session_state.current_path = None
            st.session_state.current_cost = 0
            st.rerun()
    with col_clear2:
        if st.button("🔄 Reset View", use_container_width=True):
            st.session_state.current_path = None
            st.session_state.current_cost = 0
            st.session_state.start_node = warehouses[0]
            st.session_state.end_node = stores[0]
            st.rerun()


# --- 6. Graph Visualization ---
with col_main:
    st.header("🌐 Network Visualization")

    current_path = st.session_state.get("current_path", None)
    
    if current_path:
        title = f"Optimal Route: {' → '.join(current_path)} | Total Cost: ${st.session_state.get('current_cost', 0)}"
        draw_graph(G, pos, path_nodes=current_path, title=title)
        
        # Show detailed path analysis
        with st.expander("📊 Detailed Path Analysis", expanded=True):
            st.write("**🛣️ Step-by-Step Route Breakdown:**")
            
            total = 0
            for i in range(len(current_path) - 1):
                start = current_path[i]
                end = current_path[i + 1]
                if G.has_edge(start, end):
                    step_cost = G[start][end]['weight']
                    total += step_cost
                    
                    # Get node types
                    start_type = G.nodes[start]['type'].title()
                    end_type = G.nodes[end]['type'].title()
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**Step {i+1}:** {start} ({start_type}) → {end} ({end_type})")
                    with col2:
                        st.write(f"Cost: `${step_cost}`")
                    with col3:
                        st.write(f"Running: `${total}`")
            
            st.success(f"**🎯 Total Route Cost: ${total}**")
            
            # Network efficiency metrics
            st.write("**📈 Route Efficiency Metrics:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Hops", len(current_path) - 1)
            with col2:
                avg_cost = total / (len(current_path) - 1) if len(current_path) > 1 else 0
                st.metric("Avg Cost/Hop", f"${avg_cost:.1f}")
            with col3:
                node_types_in_path = set([G.nodes[n]['type'] for n in current_path])
                st.metric("Node Types Used", len(node_types_in_path))
    
    else:
        draw_graph(G, pos, title="Complete Supply Chain Network - Select Operations from Control Panel")
        
        # Show comprehensive network statistics
        with st.expander("📈 Network Statistics & Analysis", expanded=False):
            st.write("**🔍 Network Complexity Overview:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Node Distribution:**")
                st.write(f"• Suppliers: {len(suppliers)}")
                st.write(f"• Warehouses: {len(warehouses)}")
                st.write(f"• Distribution Centers: {len(distributions)}")
                st.write(f"• Hubs: {len(hubs)}")
                st.write(f"• Stores: {len(stores)}")
                st.write(f"• **Total: {G.number_of_nodes()} nodes**")
            
            with col2:
                st.write("**Connection Statistics:**")
                st.write(f"• Total Edges: {G.number_of_edges()}")
                avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
                st.write(f"• Avg Connections: {avg_degree:.2f}")
                
                # Find most connected node
                degrees = dict(G.degree())
                max_node = max(degrees, key=degrees.get)
                st.write(f"• Most Connected: {max_node} ({degrees[max_node]} connections)")
            
            with col3:
                st.write("**Cost Analysis:**")
                all_weights = [d['weight'] for u, v, d in G.edges(data=True)]
                st.write(f"• Min Cost: ${min(all_weights)}")
                st.write(f"• Max Cost: ${max(all_weights)}")
                st.write(f"• Avg Cost: ${sum(all_weights)/len(all_weights):.1f}")
                st.write(f"• Total Network Cost: ${sum(all_weights)}")
            
            st.divider()
            
            # Network connectivity analysis
            st.write("**🔗 Network Connectivity:**")
            col1, col2 = st.columns(2)
            
            with col1:
                # Check if all stores are reachable from all suppliers
                reachable_count = 0
                total_pairs = len(suppliers) * len(stores)
                
                for supplier in suppliers:
                    for store in stores:
                        try:
                            nx.shortest_path(G, supplier, store)
                            reachable_count += 1
                        except:
                            pass
                
                connectivity_pct = (reachable_count / total_pairs) * 100
                st.metric("Supplier→Store Connectivity", f"{connectivity_pct:.1f}%", 
                         help="Percentage of supplier-store pairs with a valid path")
            
            with col2:
                # Average shortest path length
                try:
                    avg_path_length = nx.average_shortest_path_length(G, weight='weight')
                    st.metric("Avg Shortest Path Cost", f"${avg_path_length:.1f}",
                             help="Average cost of shortest paths in the network")
                except:
                    st.metric("Avg Shortest Path Cost", "N/A",
                             help="Network may not be fully connected")
            
            st.divider()
            
            # Redundancy analysis
            st.write("**🛡️ Network Redundancy:**")
            st.caption("Shows how many alternative paths exist for key routes")
            
            # Check redundancy for a sample route
            sample_start = warehouses[0]
            sample_end = stores[0]
            
            try:
                # Find all simple paths (limit to avoid computation explosion)
                all_paths = list(nx.all_simple_paths(G, sample_start, sample_end, cutoff=10))
                st.info(f"**Example:** {sample_start} → {sample_end} has **{len(all_paths)} alternative routes**")
                
                if len(all_paths) > 1:
                    st.success("✅ Network has good redundancy - multiple paths available")
                else:
                    st.warning("⚠️ Limited redundancy - consider adding more connections")
            except:
                st.error("❌ No path exists between sample nodes")
            
            st.divider()
            
            # Critical nodes analysis
            st.write("**⚠️ Critical Nodes Analysis:**")
            st.caption("Nodes whose removal would most impact network connectivity")
            
            # Find nodes with highest betweenness centrality
            try:
                betweenness = nx.betweenness_centrality(G, weight='weight')
                sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
                
                st.write("**Top 5 Most Critical Nodes:**")
                for i, (node, centrality) in enumerate(sorted_nodes, 1):
                    node_type = G.nodes[node]['type'].title()
                    st.write(f"{i}. **{node}** ({node_type}) - Criticality: {centrality:.3f}")
                
                st.caption("💡 These nodes handle the most traffic. Their failure would significantly impact the network.")
            except:
                st.write("Unable to compute critical nodes")

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 20px;'>
        <p><strong>🚚 Advanced Supply Chain Optimizer</strong></p>
        <p>Powered by NetworkX, Dijkstra's Algorithm & Hungarian Algorithm</p>
        <p style='font-size: 0.9em;'>Network: 6 Suppliers • 5 Warehouses • 4 Distribution Centers • 4 Hubs • 10 Stores</p>
    </div>
""", unsafe_allow_html=True)