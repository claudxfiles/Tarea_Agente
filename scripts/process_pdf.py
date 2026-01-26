import os
import pypdf
import math

def process_pdf():
    pdf_path = "data/PDF/Ley-21442_13-ABR-2022.pdf"
    output_dir = "data/Doc"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    print(f"Opening PDF: {pdf_path}")
    try:
        reader = pypdf.PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        print(f"Extracted {len(full_text)} characters.")
        
        # Split into 20 parts
        num_parts = 20
        part_size = math.ceil(len(full_text) / num_parts)
        
        for i in range(num_parts):
            start = i * part_size
            end = min((i + 1) * part_size, len(full_text))
            part_content = full_text[start:end]
            
            filename = f"documento_{i+1:02d}.txt"
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(part_content)
            
            print(f"Saved {filename} ({len(part_content)} chars)")
            
        print("Extraction and splitting complete.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_pdf()
