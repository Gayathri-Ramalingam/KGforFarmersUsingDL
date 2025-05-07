from llama_cpp import Llama
import base64

model_path = base64.b64decode("bW9kZWxfcGF0aCA9ICJtaXN0cmFsLTdiLWluc3RydWN0LXYwLjIuUTVfS19NLmdndWYiCg==")
model_path = model_path.decode("utf-8")
exec(model_path)


model = Llama(model_path=model_path, n_gpu_layers=40,verbose=False)

def extract_relationship(sentence: str, entity1: str, entity2: str):
    """
    Extracts relationships between entity1 and entity2 from a given sentence.
    
    Args:
        sentence (str): The input sentence.
        entity1 (str): The first entity.
        entity2 (str): The second entity.
        
    Returns:
        list: A list of relationships between entity1 and entity2, or an empty list if none found.
    """

    
    output = model(sentence, max_tokens=100, temperature=0.2)
    response = output["choices"][0]["text"].strip()

    # Convert response to list format safely
    if "none" in response.lower():
        return []
    try:
        relationships = eval(response)  # Ensure output is a list
        return relationships if isinstance(relationships, list) else []
    except:
        try:
            return eval(response.split("]")[0]+"]")
        except:
            return [response]  # Fallback if not a proper list

def perform_ner(sentence):


    # Generate the response with stop sequences
    output = model(sentence, max_tokens=300)    # Parsing the output into a dictionary
    entities = {}
    for line in output.split("\n"):
        if "->" in line:
            try:
                
                entity, category = line.split("->")
            except:
                
                entity = line.split("->")[0]
                category = "NIL"
            entity = entity.replace("[", "").replace("]", "")
            entities[entity.strip()] = category.strip()

    # Post-process vague terms
    refined_entities = {}
    vague_terms = {
        # General vague terms
        "Thing": "Object",
        "Concept": "Idea",
        "Entity": "Item",
        "Item": "Object",
        "Location": "Geographical Place",
        "Product": "Crop",
        "Material": "Substance",
        
        # Geographical terms
        "Country": "Nation",
        "Region": "Province",
        "State": "Province",
        "Province": "Administrative Division",
        "City": "Urban Area",
        "Town": "Urban Area",
        "Village": "Rural Area",
        "Place": "Geographical Place",
        "Area": "Zone",
        
        # Biological terms
        "Animal": "Species",
        "Plant": "Crop",
        "Organism": "Living Entity",
        "Food": "Edible Item",
        "Bacteria": "Microorganism",
        "Virus": "Pathogen",
        "Fruit": "Produce",
        "Vegetable": "Produce",
        "Crop": "Agricultural Product",
        
        # Scientific and technical terms
        "Scientific Term": "Scientific Concept",
        "Theory": "Scientific Theory",
        "Law": "Scientific Law",
        "Formula": "Mathematical Formula",
        "Technology": "Software",
        "Device": "Hardware",
        "Equipment": "Tool",
        "Instrument": "Measurement Tool",
        "Process": "Methodology",
        "System": "Framework",
        
        # Organizations and institutions
        "Organization": "Company",
        "Institution": "University",
        "Company": "Corporation",
        "Firm": "Business",
        "NGO": "Non-profit Organization",
        "Agency": "Government Agency",
        
        # People and professions
        "Person": "Individual",
        "Scientist": "Researcher",
        "Athlete": "Sportsperson",
        "Politician": "Government Official",
        "Author": "Writer",
        "Actor": "Performer",
        "Musician": "Artist",
        "Teacher": "Educator",
        "Doctor": "Physician",
        "Engineer": "Technologist",
        "Farmer": "Agricultural Worker",
        "Lawyer": "Legal Professional",
        
        # Events and occurrences
        "Event": "Historical Event",
        "Incident": "Accident",
        "Festival": "Celebration",
        "Ceremony": "Ritual",
        "Occasion": "Gathering",
        "Conflict": "War",
        "Agreement": "Treaty",
        "Discovery": "Scientific Finding",
        
        # Abstract and conceptual terms
        "Action": "Activity",
        "Activity": "Process",
        "Process": "Operation",
        "Movement": "Trend",
        "Trend": "Pattern",
        "Phenomenon": "Occurrence",
        "Behavior": "Conduct",
        "Emotion": "Feeling",
        "Idea": "Concept",
        
        # Time-related terms
        "Time": "Temporal Concept",
        "Date": "Calendar Date",
        "Period": "Time Frame",
        "Era": "Historical Period",
        "Epoch": "Geological Time Frame",
        "Decade": "Ten-year Period",
        "Century": "Hundred-year Period",
        
        # Technological terms
        "Software": "Program",
        "Application": "Software Tool",
        "Platform": "Service",
        "Service": "Online Service",
        "Tool": "Utility",
        "Machine": "Device",
        
        # Art and cultural terms
        "Art": "Artwork",
        "Painting": "Visual Art",
        "Sculpture": "3D Art",
        "Music": "Musical Composition",
        "Song": "Musical Piece",
        "Literature": "Written Work",
        "Book": "Publication",
        "Film": "Movie",
        "Theater": "Stage Performance",
        
        # Economic and financial terms
        "Money": "Currency",
        "Price": "Cost",
        "Market": "Economic Sector",
        "Stock": "Equity",
        "Bond": "Debt Instrument",
        "Investment": "Financial Asset",
        "Revenue": "Income",
        "Profit": "Net Income",
        "Expense": "Cost",
        
        # Miscellaneous
        "Structure": "Building",
        "Container": "Vessel",
        "Color": "Shade",
        "Flavor": "Taste",
        "Sound": "Noise",
        "Light": "Illumination",
        "Energy": "Power",
    }


    for entity, category in entities.items():
        
        refined_entities[entity] = vague_terms.get(category)  # Map vague terms

    return refined_entities

if __name__ == "__main__":
    # Example Usage
    sentence = """At the International Agriculture Conference held in Nairobi, researchers from the Food and Agriculture Organization (FAO) and scientists from Wageningen University discussed the impact of climate change on wheat and rice production in countries like India, Brazil, and the United States, while agricultural technology companies such as John Deere and Bayer announced new partnerships with the Bill & Melinda Gates Foundation to develop AI-driven precision farming techniques aimed at improving soil health, optimizing irrigation in drought-prone regions like California and sub-Saharan Africa, and reducing dependence on chemical fertilizers, a move that was welcomed by organic farming advocates from the International Federation of Organic Agriculture Movements (IFOAM) and policymakers from the European Union, who are working on subsidies for sustainable farming practices to help smallholder farmers in developing nations access better resources and training."""
    entity1 = "major agricultural products"
    entity2 = "foods"
    
    output = extract_relationship(sentence, entity1, entity2)
    print(output)  
