import spacy
from itertools import combinations
from relationship_extraction import extract_relationship, perform_ner
from xml.dom.minidom import Entity
# Load spaCy for sentence segmentation
nlp = spacy.load("en_core_web_sm")

def process_paragraph_with_transformers(paragraph: str):
    """
    Processes a paragraph to extract entity pairs for each sentence using a transformer-based NER pipeline.
    
    Args:
        paragraph (str): The input paragraph text.
    
    Returns:
        dict: Dictionary with sentences as keys and a list of entity pairs as values.
              Each entity pair is a tuple: ((entity1, label1), (entity2, label2)).
    """
    doc = nlp(paragraph)
    sentence_entity_pairs = {}

    for sent in doc.sents:
        sent_text = sent.text.strip()
        # Use transformer NER pipeline on the sentence
        ner_results = list(perform_ner(sent_text).items())
        
        # Each result is a dict with keys like 'word' and 'entity_group'
        # We use a list comprehension to get (entity, label) tuples.
        entities = [(result[0], result[1]) for result in ner_results]
        
        # Generate all possible pairs of entities in the sentence
        entity_pairs = list(combinations(entities, 2))
        sentence_entity_pairs[sent_text] = entity_pairs

    return sentence_entity_pairs

def get_triples(paragraph):
    results = process_paragraph_with_transformers(paragraph)
    
    triples = []
    for sent, entity_pairs in results.items():
        for entity_pair in entity_pairs:
            e1, e2 = entity_pair
            relation = extract_relationship(sent,e1,e2)
            if relation:
                triples.append((e1[0],relation[0].replace(" ","_"),e2[0]))
    return triples
            
def generate_ttl(triples, filename="output.ttl"):
    ttl_prefixes = (
        "@prefix agri: <http://example.org/agriculture#> .\n"
        "@prefix rel: <http://example.org/relationship#> .\n\n"
    )
    
    ttl_statements = []
    for entity1, relationship, entity2 in triples:
        ttl_statements.append(f"agri:{entity1} rel:{relationship} agri:{entity2} .")
    
    ttl_content = ttl_prefixes + "\n".join(ttl_statements)
    
    with open(filename, "w") as file:
        file.write(ttl_content)
    
    print(f"TTL file '{filename}' generated successfully.")   




if __name__ == "__main__":
    with open("test.txt") as f:
        paragraph = f.read()
        results = get_triples(paragraph)
        generate_ttl(results)
