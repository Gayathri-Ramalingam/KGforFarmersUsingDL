import pandas as pd
import re

# File paths
ttl_file_path = "agriculture_kg_general-3.ttl"  # Input TTL file
csv_file_path = "All-India-Production.csv"      # Input CSV file
output_ttl_file_path = "agriculture_kg_updated.ttl"  # Output TTL file

# Read the TTL file
with open(ttl_file_path, "r", encoding="utf-8") as file:
    ttl_data = file.read()

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Function to clean entity names for TTL syntax
def clean_ttl_name(name):
    """Ensure valid TTL entity names by replacing spaces and special characters."""
    return re.sub(r"[^a-zA-Z0-9]", "_", name)

# Define a template for production data
production_template = """
agri:{crop} rel:has_production [
    agri:season "{season}" ;
    agri:production "{production}"
] .
"""

# Process each row in the CSV and integrate it into the TTL data
for _, row in df.iterrows():
    crop = clean_ttl_name(row["Crop"])  # Clean crop name
    season = row["Season"]
    production = row["Production-2024-25"]

    if pd.notna(production):  # Only add valid production values
        new_entry = production_template.format(crop=crop, season=season, production=production)

        # Check if the crop node already exists in the TTL file
        if f"agri:{crop}" not in ttl_data:
            ttl_data += f"\nagri:{crop} a agri:Crop .\n"  # Add crop definition
        
        ttl_data += new_entry  # Append production data

# Save the updated TTL content to a file
with open(output_ttl_file_path, "w", encoding="utf-8") as file:
    file.write(ttl_data)

print(f"Updated TTL file saved as: {output_ttl_file_path}")
