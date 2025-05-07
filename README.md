
# 🌾 Agricultural Knowledge Graph Construction and Visualization

This project constructs and visualizes a **Knowledge Graph (KG)** for the agricultural domain using advanced NLP techniques. It extracts entities and their relationships from agricultural texts using fine-tuned transformer models and displays the graph interactively using a **Streamlit** web app with **Pyvis**.

## 🚀 Features

- **Named Entity Recognition (NER)** using a fine-tuned **RoBERTa** model.
- **Relationship Extraction (RE)** using **BERT + CRF** method.
- **Knowledge Graph Construction** from extracted triples (entities and relationships).
- **Interactive Visualization** of the KG using **Pyvis**.
- **Streamlit Frontend** for a smooth, accessible user experience.

---

## 🧠 Architecture Overview


Agricultural Text
      |
      ▼
[NER: Fine-tuned RoBERTa]
      |
      ▼
Entities
      |
      ▼
[RE: BERT + CRF]
      |
      ▼
Entity Pairs + Relations
      |
      ▼
[Triple Construction]
      |
      ▼
[Pyvis + Streamlit]
      |
      ▼
Interactive Knowledge Graph


---

## 🛠️ Tech Stack

- **Python 3.8+**
- **HuggingFace Transformers** - RoBERTa, BERT
- **CRF Suite / sklearn-crfsuite** for sequence tagging
- **Streamlit** for frontend
- **Pyvis** for graph visualization
- **spaCy / NLTK / Scikit-learn** (optional for pre/post-processing)

---

## 📦 Installation

```bash
git clone https://github.com/Barath3012/KGConstructionForFarmersUsingDL.git
cd agri-kg-builder

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🚧 Project Structure

```text
KGConstructionForFarmersUsingDL/
│
├── .git/                          # Git metadata
├── data/                          # Additional data files or configs
├── scraped_data/                 # Saved outputs from scraping
│
├── README.md                      # Project documentation
├── Real-time-data-scrape.py      # Script to scrape real-time agricultural data
├── Real-time-ttl-integration.py  # Integrates real-time data into TTL format
├── extract_pdfs.py               # Extracts text from agricultural PDFs
├── extracted_text.txt            # Text extracted from documents
├── agriculture_info.txt          # Raw agricultural information
├── agriculture_kg_fixed.ttl      # Final TTL knowledge graph output
│
├── fine_tune_roberta.py          # RoBERTa fine-tuning for NER
├── relationship_extraction.py    # BERT + CRF for relationship extraction
├── knowledge_base_construction.py# Triple construction logic
│
├── front_end.py                  # Streamlit app (I/O version)
├── front_end_full_graph.py       # Streamlit app (full graph visualization)
│
├── scrape.py                     # Scrapes structured agricultural sources
├── scrape_wiki.py                # Scrapes Wikipedia for agri-domain info

```

---

## ▶️ Run the App

```bash
streamlit run front_end.py
```

Navigate to `http://localhost:8501` in your browser.

---

## 🧪 Example Use Case

Input a paragraph or a text file such as:

> "Wheat requires well-drained loamy soil and moderate rainfall. In Punjab, India, farmers prefer the PBW-343 variety for its resistance to rust."

The app will:

1. Extract entities like `Wheat`, `loamy soil`, `Punjab`, `PBW-343`, etc.
2. Detect relationships like `requires`, `grows in`, `preferred variety`, etc.
3. Visualize the resulting knowledge graph interactively.

---

## 📌 Notes

- NER and RE models are fine tuned using domain-specific datasets for best results.
- Blank nodes or nested relations are handled using extended triple structures.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for more details.

---

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, new features, or bug fixes.

---

## 🙌 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Pyvis](https://pyvis.readthedocs.io/)
- [Streamlit](https://streamlit.io/)
- Agricultural NER Datasets (e.g., AgriNER, AgriBERT corpora)

---

```
