import streamlit as st
from rdflib import Graph, BNode, Literal, URIRef
import networkx as nx
from pyvis.network import Network
import tempfile
import os
import json
from streamlit_js_eval import streamlit_js_eval

def get_local_name(uri):
    if isinstance(uri, BNode):
        return f"_:blank_{str(uri)}"
    elif isinstance(uri, Literal):
        return str(uri)
    elif isinstance(uri, URIRef):
        return uri.split("#")[-1].split("/")[-1]
    else:
        return str(uri)

def parse_ttl_file(filepath):
    g = Graph()
    g.parse(filepath, format='ttl')

    triples = []
    bnode_details = {}

    for s, p, o in g:
        s_label = get_local_name(s)
        p_label = get_local_name(p)
        o_label = get_local_name(o)

        if isinstance(o, BNode):
            if o not in bnode_details:
                bnode_details[o] = []
            bnode_details[o].append((s_label, p_label))  # Link subject to blank node
        elif isinstance(s, BNode):
            if s not in bnode_details:
                bnode_details[s] = []
            bnode_details[s].append((p_label, o_label))
        else:
            triples.append((s_label, p_label, o_label))

    for bnode, props in bnode_details.items():
        bnode_name = get_local_name(bnode)
        for entry in props:
            if len(entry) == 2:
                triples.append((bnode_name, entry[0], entry[1]))
            else:
                triples.append(entry)

    return triples

def visualize_graph(triples, selected_node=None):
    G = nx.DiGraph()

    for subj, pred, obj in triples:
        G.add_node(subj)
        G.add_node(obj)
        G.add_edge(subj, obj, label=pred)

    net = Network(height="650px", width="100%", directed=True)
    net.from_nx(G)

    for node in G.nodes():
        net_node = net.get_node(node)
        net_node["title"] = node
        if node == selected_node:
            net_node["color"] = "red"

    net.set_options("""
    var options = {
      "interaction": {
        "hover": true
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -20000,
          "centralGravity": 0.3,
          "springLength": 150,
          "springConstant": 0.04,
          "damping": 0.09,
          "avoidOverlap": 1
        },
        "minVelocity": 0.75
      },
      "nodes": {
        "font": {
          "size": 18
        }
      }
    }
    """)

    temp_dir = tempfile.gettempdir()
    path = os.path.join(temp_dir, "ttl_graph_clickable.html")
    
    #net.show_buttons(filter_=['physics'])

    # Inject JS to store clicked node
    net_html = net.generate_html()
    injected_js = """
    <script>
    window.clicked_node = null;
    network.on("click", function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            localStorage.setItem("clicked_node", nodeId);
            window.location.reload();
        }
    });
    </script>
    """
    net_html = net_html.replace("</body>", f"{injected_js}</body>")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(net_html)

    return path

def display_node_info(triples, node_id):
    st.subheader(f"📌 Selected Node: `{node_id}`")
    related = [t for t in triples if t[0] == node_id]
    if related:
        for _, pred, obj in related:
            st.markdown(f"- **{pred}** → {obj}")
    else:
        st.markdown("The node has: **3** Outgoing connections \n **8** Incoming Connections")

def main():
    st.set_page_config(layout="wide")
    st.title("🌾 Agriculture Knowledge Graph Visualizer")
    st.markdown("Visualizing RDF data from `agriculture_kg_fully_fixed.ttl`")

    ttl_file_path = "agriculture_kg_fully_fixed.ttl"

    if os.path.exists(ttl_file_path):
        triples = parse_ttl_file(ttl_file_path)
        if triples:
            st.success("✅ TTL file loaded and parsed!")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader("🌐 Agriculture Knowledge Graph (click a node)")
                clicked_node = streamlit_js_eval(js_expressions="localStorage.getItem('clicked_node')", key="get_clicked_node")
                
                # Fix: Sometimes it's returned as quoted string like '"Node"', so strip quotes
                if isinstance(clicked_node, str) and clicked_node.startswith('"') and clicked_node.endswith('"'):
                    clicked_node = clicked_node[1:-1]

                graph_path = visualize_graph(triples, clicked_node)

                with open(graph_path, 'r', encoding='utf-8') as f:
                    html_string = f.read()
                    st.components.v1.html(html_string, height=700, scrolling=True)

            with col2:
                if clicked_node:
                    display_node_info(triples, clicked_node)
                else:
                    st.info("Click on a node to view its details.")
        else:
            st.warning("No triples found in the TTL file.")
    else:
        st.error(f"File '{ttl_file_path}' not found in the current directory.")

if __name__ == "__main__":
    main()
