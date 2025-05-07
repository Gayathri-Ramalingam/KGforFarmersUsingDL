import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import os
from knowledge_base_construction import get_triples

def visualize_graph(triples):
    G = nx.DiGraph()

    for subj, pred, obj in triples:
        G.add_node(subj)
        G.add_node(obj)
        G.add_edge(subj, obj, label=pred)

    # Add enhanced hover info
    for node in G.nodes():
        degree = G.degree(node)
        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)
        G.nodes[node]['title'] = (
            f"<b>{node}</b><br>"
            f"Total connections: {degree}<br>"
            f"Incoming: {in_deg}<br>"
            f"Outgoing: {out_deg}"
        )

    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    #net.show_buttons(filter_=['physics'])

    # Save to a temporary HTML file
    temp_dir = tempfile.gettempdir()
    path = os.path.join(temp_dir, "graph.html")
    net.write_html(path, open_browser=False)

    return path

def main():
    st.title("🧠 Knowledge Graph Construction and Visualization")

    st.header("📄 Upload Text Files")
    uploaded_files = st.file_uploader("Choose one or more text files", type=["txt"], accept_multiple_files=True)

    if uploaded_files:
        if st.button("📈 Build Knowledge Graph"):
            all_triples = []

            for file in uploaded_files:
                content = file.read().decode("utf-8")
                triples = get_triples(content)
                all_triples.extend(triples)

            if all_triples:
                st.subheader("🌐 Interactive Knowledge Graph")
                graph_path = visualize_graph(all_triples)

                with open(graph_path, 'r', encoding='utf-8') as f:
                    html_string = f.read()
                    st.components.v1.html(html_string, height=700, scrolling=True)
            else:
                st.warning("No triples found in the uploaded files.")

if __name__ == "__main__":
    main()
