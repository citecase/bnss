import os
import json
import re
from docx import Document

def convert_law_docx_to_json(input_file, output_file):
    """
    Parses a DOCX law document and splits it into sections based on '1.', '2.' numbering.
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    doc = Document(input_file)
    sections = []
    
    # Regex for "1.", "2.", "10." at the start of a paragraph
    section_pattern = re.compile(r'^(\d+)\.\s*(.*)')

    current_section_name = "Preamble"
    current_content = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        match = section_pattern.match(text)
        
        if match:
            # Save the previous section before moving to the next
            if current_content or current_section_name != "Preamble":
                sections.append({
                    "section_number": current_section_name.split('.')[0] if '.' in current_section_name else "0",
                    "title": current_section_name,
                    "content": "\n".join(current_content).strip()
                })
            
            # Start new section
            current_section_name = text
            current_content = []
        else:
            current_content.append(text)

    # Append the final section
    sections.append({
        "section_title": current_section_name,
        "content": "\n".join(current_content).strip()
    })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sections, f, indent=4, ensure_ascii=False)

    print(f"Successfully created {output_file} with {len(sections)} sections.")

if __name__ == "__main__":
    # Change 'my_law_document.docx' to your actual file name
    convert_law_docx_to_json("my_law_document.docx", "legal_data.json")
