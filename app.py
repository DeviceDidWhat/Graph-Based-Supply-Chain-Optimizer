import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from optimizer import (
    build_graph, 
    find_optimal_assignment, 
    find_shortest_path,
    find_k_shortest_paths,
    find_critical_nodes,
    analyze_network_resilience,
    calculate_route_efficiency,
    get_node_colors,
    compute_semantic_positions
)

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Supply Chain Optimizer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Title styling */
        .main-title {
            font-size: 2.8rem;
            font-weight: bold;
            background: linear-gradient(120deg, #1f77b4, #51cf66);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #6c757d;
            font-size: 1.1rem;
            margin-bottom: 2rem;
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
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚚 Advanced Graph-Based Supply Chain Optimizer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time optimization using Dijkstra\'s Algorithm, Hungarian Method & Network Flow Analysis</p>', unsafe_allow_html=True)

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
# All possible end nodes (stores, hubs, distributions)
end_nodes = sorted(stores + hubs + distributions)


# --- 2. Graph Drawing Helper ---
def draw_graph(G, pos, path_nodes=None, title="Supply Chain Network", highlight_nodes=None):
    """Draws graph with non-overlapping semantic layout."""
    fig, ax = plt.subplots(figsize=(22, 12))
    
    # Set background color
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8f9fa')

    # Colors and layout
    colors = get_node_colors(G, path=path_nodes)
    
    # Highlight special nodes if provided
    if highlight_nodes:
        for node in G.nodes():
            if node in highlight_nodes and node not in (path_nodes or []):
                idx = list(G.nodes()).index(node)
                colors[idx] = '#ffa94d'  # Orange for highlighted nodes
    
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
        Patch(facecolor='#ff922b', edgecolor='#2d2d2d', linewidth=2, label='Distribution (4)'),
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
if 'alternative_paths' not in st.session_state:
    st.session_state.alternative_paths = []
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'full_network'


# --- 4. Network Overview Statistics (Top Section) ---
st.markdown("---")
col_stat1, col_stat2, col_stat3, col_stat4, col_stat5, col_stat6, col_stat7 = st.columns(7)

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
    st.metric("🔗 Edges", G.number_of_edges())
with col_stat7:
    all_weights = [d['weight'] for u, v, d in G.edges(data=True)]
    st.metric("💰 Avg Cost", f"${sum(all_weights)/len(all_weights):.1f}")

st.markdown("---")


# --- 5. UI Layout ---
col_sidebar, col_main = st.columns([1, 3], gap="large")

# --- Sidebar Controls ---
with col_sidebar:
    st.header("⚙️ Operations Control Panel")
    
    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Assignment", "🗺️ Routing", "⚠️ Resilience", "📊 Analytics"])
    
    # --- TAB 1: Optimal Assignment ---
    with tab1:
        st.subheader("Hungarian Algorithm")
        st.caption("Optimal Supplier → Warehouse matching")
        
        if st.button("🔄 Compute Optimal Assignment", use_container_width=True, key="assign_btn"):
            with st.spinner("Running Hungarian Algorithm..."):
                assignments, total_cost = find_optimal_assignment(G)
                
                st.success(f"✅ **Total Cost: ${total_cost:.0f}**")
                
                # Display assignments in a DataFrame
                assignment_data = []
                for s, w in assignments:
                    if G.has_edge(s, w):
                        cost = G[s][w]['weight']
                        assignment_data.append({
                            'Supplier': s,
                            'Warehouse': w,
                            'Cost': f"${cost}"
                        })
                
                df_assignments = pd.DataFrame(assignment_data)
                st.dataframe(df_assignments, use_container_width=True, hide_index=True)
                
                # Calculate potential savings
                all_possible_costs = []
                for s in suppliers:
                    for w in warehouses:
                        if G.has_edge(s, w):
                            all_possible_costs.append(G[s][w]['weight'])
                
                if all_possible_costs:
                    avg_random = sum(all_possible_costs) / len(all_possible_costs) * len(suppliers)
                    savings = avg_random - total_cost
                    st.info(f"💡 **Savings vs Random Assignment:** ${savings:.0f} ({(savings/avg_random)*100:.1f}%)")
    
    # --- TAB 2: Routing ---
    with tab2:
        st.subheader("Dijkstra's Algorithm")
        st.caption("Shortest path optimization")
        
        start_node = st.selectbox(
            "📍 Start Node:", 
            options=start_nodes,
            index=start_nodes.index(st.session_state.start_node) if st.session_state.start_node in start_nodes else 0,
            key='start_select',
            help="Select origin point"
        )
        st.session_state.start_node = start_node
        
        end_node = st.selectbox(
            "🎯 End Node:", 
            options=end_nodes,
            index=end_nodes.index(st.session_state.end_node) if st.session_state.end_node in end_nodes else 0,
            key='end_select',
            help="Select destination"
        )
        st.session_state.end_node = end_node

        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔍 Find Shortest", use_container_width=True, key="shortest_btn"):
                with st.spinner("Computing optimal route..."):
                    path, cost = find_shortest_path(G, start_node, end_node)
                    if path:
                        st.session_state.current_path = path
                        st.session_state.current_cost = cost
                        st.session_state.view_mode = 'shortest_path'
                        st.success("✅ Path Found!")
                        st.metric("💵 Total Cost", f"${cost}")
                        st.caption(f"🛣️ {len(path)} nodes, {len(path)-1} hops")
                    else:
                        st.error(f"❌ No path exists")
        
        with col_btn2:
            if st.button("🔀 Find Alternatives", use_container_width=True, key="alt_btn"):
                with st.spinner("Finding alternative routes..."):
                    k_paths = find_k_shortest_paths(G, start_node, end_node, k=5)
                    if k_paths:
                        st.session_state.alternative_paths = k_paths
                        st.session_state.view_mode = 'alternatives'
                        st.success(f"✅ Found {len(k_paths)} routes")
                    else:
                        st.error("❌ No alternatives found")
        
        # Show alternative paths selector
        if st.session_state.alternative_paths:
            st.divider()
            st.write("**Select Route to Visualize:**")
            
            route_options = []
            for i, (path, cost) in enumerate(st.session_state.alternative_paths):
                route_options.append(f"Option {i+1}: ${cost} ({len(path)-1} hops)")
            
            selected_route = st.selectbox(
                "Routes:",
                options=range(len(route_options)),
                format_func=lambda x: route_options[x],
                key='route_selector'
            )
            
            if st.button("📍 Show Selected Route", use_container_width=True):
                path, cost = st.session_state.alternative_paths[selected_route]
                st.session_state.current_path = path
                st.session_state.current_cost = cost
                st.rerun()
    
    # --- TAB 3: Resilience Testing ---
    with tab3:
        st.subheader("Network Resilience")
        st.caption("Failure simulation & rerouting")
        
        broken_node = st.selectbox(
            "⚠️ Simulate Node Failure:", 
            options=all_nodes,
            key='broken_select',
            help="Test network resilience"
        )

        if st.button("🧭 Test Resilience", use_container_width=True, key="resilience_btn"):
            with st.spinner(f"Analyzing {broken_node} failure..."):
                # Get resilience metrics
                resilience = analyze_network_resilience(G, broken_node)
                
                st.write("**Impact Analysis:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Before", f"{resilience['connected_before']}")
                with col2:
                    st.metric("After", f"{resilience['connected_after']}", 
                             delta=f"-{resilience['connected_before']-resilience['connected_after']}")
                
                st.metric("Connectivity Loss", f"{resilience['connectivity_loss_pct']:.1f}%")
                
                # Try to find alternative route
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
                    st.session_state.view_mode = 'rerouted'
                    st.success("✅ Reroute successful!")
                    st.info(f"New Route: {' → '.join(path_new)}")
                    
                    # Cost comparison
                    original_path, original_cost = find_shortest_path(
                        G, 
                        st.session_state.start_node, 
                        st.session_state.end_node
                    )
                    
                    if original_path:
                        diff = cost_new - original_cost
                        pct = (diff/original_cost)*100
                        st.metric("Cost Impact", f"${diff:+.0f}", delta=f"{pct:+.1f}%", delta_color="inverse")
                else:
                    st.error(f"❌ Network disconnected!")
        
        st.divider()
        
        # Critical nodes analysis
        if st.button("🎯 Find Critical Nodes", use_container_width=True):
            with st.spinner("Analyzing network..."):
                critical = find_critical_nodes(G, top_n=5)
                st.write("**Most Critical Nodes:**")
                for i, (node, centrality) in enumerate(critical, 1):
                    node_type = G.nodes[node]['type'].title()
                    st.write(f"{i}. **{node}** ({node_type})")
                    st.progress(centrality, text=f"Criticality: {centrality:.3f}")
    
    # --- TAB 4: Analytics ---
    with tab4:
        st.subheader("Network Analytics")
        st.caption("Advanced metrics & insights")
        
        if st.button("📊 Generate Full Report", use_container_width=True):
            with st.spinner("Analyzing network..."):
                # Network connectivity
                reachable_count = 0
                total_pairs = len(suppliers) * len(stores)
                for s in suppliers:
                    for r in stores:
                        try:
                            nx.shortest_path(G, s, r)
                            reachable_count += 1
                        except:
                            pass
                
                connectivity_pct = (reachable_count / total_pairs) * 100
                
                st.metric("Supplier→Store Connectivity", f"{connectivity_pct:.1f}%")
                
                # Average path costs
                path_costs = []
                for s in suppliers[:3]:  # Sample subset
                    for r in stores[:5]:
                        try:
                            cost = nx.dijkstra_path_length(G, s, r, weight='weight')
                            path_costs.append(cost)
                        except:
                            pass
                
                if path_costs:
                    st.metric("Avg Path Cost", f"${sum(path_costs)/len(path_costs):.1f}")
                
                # Network density
                density = nx.density(G)
                st.metric("Network Density", f"{density:.3f}")
                
                st.success("✅ Report generated!")
        
        st.divider()
        
        # Route efficiency for current path
        if st.session_state.current_path:
            st.write("**Current Route Efficiency:**")
            efficiency = calculate_route_efficiency(G, st.session_state.current_path)
            if efficiency:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Hops", efficiency['num_hops'])
                    st.metric("Path Length", efficiency['path_length'])
                with col2:
                    st.metric("Avg Cost/Hop", f"${efficiency['avg_cost_per_hop']:.1f}")
                    st.metric("Node Types", efficiency['node_types_used'])
    
    st.divider()
    
    # Control buttons
    col_clear1, col_clear2 = st.columns(2)
    with col_clear1:
        if st.button("🗑️ Clear Path", use_container_width=True):
            st.session_state.current_path = None
            st.session_state.current_cost = 0
            st.session_state.alternative_paths = []
            st.session_state.view_mode = 'full_network'
            st.rerun()
    with col_clear2:
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.current_path = None
            st.session_state.current_cost = 0
            st.session_state.alternative_paths = []
            st.session_state.start_node = warehouses[0]
            st.session_state.end_node = stores[0]
            st.session_state.view_mode = 'full_network'
            st.rerun()


# --- 6. Main Visualization Area ---
with col_main:
    st.header("🌐 Network Visualization")

    current_path = st.session_state.get("current_path", None)
    
    if current_path:
        title = f"Optimal Route: {' → '.join(current_path)} | Cost: ${st.session_state.get('current_cost', 0)}"
        draw_graph(G, pos, path_nodes=current_path, title=title)
        
        # Detailed path analysis
        with st.expander("📊 Detailed Route Analysis", expanded=True):
            # Create tabs for different analyses
            analysis_tab1, analysis_tab2 = st.tabs(["Step-by-Step", "Performance Metrics"])
            
            with analysis_tab1:
                st.write("**🛣️ Route Breakdown:**")
                
                # Create a detailed path table
                path_data = []
                total = 0
                for i in range(len(current_path) - 1):
                    start = current_path[i]
                    end = current_path[i + 1]
                    if G.has_edge(start, end):
                        step_cost = G[start][end]['weight']
                        total += step_cost
                        
                        start_type = G.nodes[start]['type'].title()
                        end_type = G.nodes[end]['type'].title()
                        
                        path_data.append({
                            'Step': i+1,
                            'From': f"{start} ({start_type})",
                            'To': f"{end} ({end_type})",
                            'Cost': f"${step_cost}",
                            'Cumulative': f"${total}"
                        })
                
                df_path = pd.DataFrame(path_data)
                st.dataframe(df_path, use_container_width=True, hide_index=True)
                
                st.success(f"**🎯 Total Route Cost: ${total}**")
            
            with analysis_tab2:
                efficiency = calculate_route_efficiency(G, current_path)
                if efficiency:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Hops", efficiency['num_hops'])
                    with col2:
                        st.metric("Avg Cost/Hop", f"${efficiency['avg_cost_per_hop']:.1f}")
                    with col3:
                        st.metric("Node Types", efficiency['node_types_used'])
                    with col4:
                        st.metric("Path Length", efficiency['path_length'])
                    
                    # Show node type distribution in path
                    st.write("**Node Type Distribution:**")
                    type_counts = {}
                    for node in current_path:
                        node_type = G.nodes[node]['type'].title()
                        type_counts[node_type] = type_counts.get(node_type, 0) + 1
                    
                    for node_type, count in sorted(type_counts.items()):
                        st.progress(count / len(current_path), text=f"{node_type}: {count}")
    
    else:
        draw_graph(G, pos, title="Complete Supply Chain Network - Use Control Panel to Optimize Routes")
        
        # Network statistics in expandable section
        with st.expander("📈 Comprehensive Network Analysis", expanded=False):
            # Create tabs for different statistics
            stats_tab1, stats_tab2, stats_tab3 = st.tabs(["Network Overview", "Connectivity", "Critical Analysis"])
            
            with stats_tab1:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Node Distribution:**")
                    node_data = {
                        'Type': ['Suppliers', 'Warehouses', 'Distribution', 'Hubs', 'Stores'],
                        'Count': [len(suppliers), len(warehouses), len(distributions), len(hubs), len(stores)]
                    }
                    df_nodes = pd.DataFrame(node_data)
                    st.dataframe(df_nodes, use_container_width=True, hide_index=True)
                    st.metric("Total Nodes", G.number_of_nodes())
                
                with col2:
                    st.write("**Connection Statistics:**")
                    st.metric("Total Edges", G.number_of_edges())
                    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
                    st.metric("Avg Connections", f"{avg_degree:.2f}")
                    degrees = dict(G.degree())
                    max_node = max(degrees, key=degrees.get)
                    st.metric("Most Connected", f"{max_node} ({degrees[max_node]})")
                
                with col3:
                    st.write("**Cost Analysis:**")
                    all_weights = [d['weight'] for u, v, d in G.edges(data=True)]
                    st.metric("Min Cost", f"${min(all_weights)}")
                    st.metric("Max Cost", f"${max(all_weights)}")
                    st.metric("Avg Cost", f"${sum(all_weights)/len(all_weights):.1f}")
            
            with stats_tab2:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Connectivity percentage
                    reachable_count = 0
                    total_pairs = len(suppliers) * len(stores)
                    for s in suppliers:
                        for r in stores:
                            try:
                                nx.shortest_path(G, s, r)
                                reachable_count += 1
                            except:
                                pass
                    
                    connectivity_pct = (reachable_count / total_pairs) * 100
                    st.metric("Supplier→Store Reachability", f"{connectivity_pct:.1f}%")
                    st.progress(connectivity_pct/100)
                
                with col2:
                    # Network density
                    density = nx.density(G)
                    st.metric("Network Density", f"{density:.3f}")
                    st.caption("Ratio of actual to possible connections")
                
                # Redundancy check
                st.write("**Path Redundancy Test:**")
                sample_pairs = [(suppliers[0], stores[0]), (warehouses[0], stores[-1])]
                for start, end in sample_pairs:
                    try:
                        all_paths = list(nx.all_simple_paths(G, start, end, cutoff=10))
                        st.write(f"• {start} → {end}: **{len(all_paths)} alternative routes**")
                    except:
                        st.write(f"• {start} → {end}: **No path**")
            
            with stats_tab3:
                st.write("**🎯 Critical Nodes (Betweenness Centrality):**")
                critical = find_critical_nodes(G, top_n=8)
                
                if critical:
                    critical_data = []
                    for node, centrality in critical:
                        node_type = G.nodes[node]['type'].title()
                        critical_data.append({
                            'Node': node,
                            'Type': node_type,
                            'Criticality': f"{centrality:.4f}",
                            'Connections': G.degree(node)
                        })
                    
                    df_critical = pd.DataFrame(critical_data)
                    st.dataframe(df_critical, use_container_width=True, hide_index=True)
                    
                    st.info("💡 These nodes handle the most traffic. Monitor them closely!")
                
                st.write("**⚠️ Single Point of Failure Test:**")
                if st.button("Test Critical Node Removal", key="spof_test"):
                    if critical:
                        test_node = critical[0][0]
                        resilience = analyze_network_resilience(G, test_node)
                        st.warning(f"Removing {test_node} would disconnect {resilience['connectivity_loss_pct']:.1f}% of routes")

# --- Show alternative paths comparison ---
if st.session_state.alternative_paths and st.session_state.view_mode == 'alternatives':
    st.markdown("---")
    st.subheader("🔀 Alternative Routes Comparison")
    
    alt_data = []
    for i, (path, cost) in enumerate(st.session_state.alternative_paths, 1):
        efficiency = calculate_route_efficiency(G, path)
        alt_data.append({
            'Option': f"Route {i}",
            'Path': ' → '.join(path),
            'Cost': f"${cost}",
            'Hops': efficiency['num_hops'] if efficiency else 'N/A',
            'Avg Cost/Hop': f"${efficiency['avg_cost_per_hop']:.1f}" if efficiency else 'N/A'
        })
    
    df_alternatives = pd.DataFrame(alt_data)
    st.dataframe(df_alternatives, use_container_width=True, hide_index=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 20px;'>
        <p><strong>🚚 Advanced Supply Chain Optimizer</strong> | Built with NetworkX & Streamlit</p>
        <p style='font-size: 0.95em;'>Algorithms: Dijkstra's Shortest Path • Hungarian Assignment • Betweenness Centrality • Network Flow</p>
        <p style='font-size: 0.9em;'>📊 Network: 6 Suppliers • 5 Warehouses • 4 Distribution Centers • 4 Hubs • 10 Stores • 80+ Connections</p>
    </div>
""", unsafe_allow_html=True)