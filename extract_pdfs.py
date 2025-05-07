import os
import PyPDF2

# Define the directory where PDFs are stored
PDF_DIR = r"scraped_data/pdfs/"

def extract_text_from_pdfs(directory):
    """Extracts text from all PDFs in the given directory."""
    pdf_texts = {}  # Dictionary to store extracted text per file

    for pdf_file in os.listdir(directory):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(directory, pdf_file)
            text = ""
            try:
                
                with open(pdf_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
    
                pdf_texts[pdf_file] = text  # Store extracted text
            except: 
                print(f"Error for file: {pdf_file}")
    return pdf_texts

if __name__ == "__main__":
    # Extract text from all PDFs
    pdf_data = extract_text_from_pdfs(PDF_DIR)
    
    # Save extracted text to a file (Optional)
    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        for pdf_name, text in pdf_data.items():
            f.write(f"\n\n--- {pdf_name} ---\n{text}")
    
    print("PDF text extraction complete!")
