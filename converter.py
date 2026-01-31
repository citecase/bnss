import os
import json
import re
from docx import Document

def convert_all_docx():
    # Look for any .docx file in the current directory
    files = [f for f in os.listdir('.') if f.endswith('.docx')]
    
    if not files:
        print("No .docx files found to convert.")
        return

    section_pattern = re.compile(r'^(\d+)\.\s*(.*)')

    for input_file in files:
        output_file = input_file.replace('.docx', '.json')
        doc = Document(input_file)
        sections = []
        current_section_name = "Preamble"
        current_content = []

        for para in doc.paragraphs:
            text = para.text.strip()
            if not text: continue
            
            match = section_pattern.match(text)
            if match:
                if current_content or current_section_name != "Preamble":
                    sections.append({
                        "title": current_section_name,
                        "content": "\n".join(current_content).strip()
                    })
                current_section_name = text
                current_content = []
            else:
                current_content.append(text)

        # Final section
        sections.append({"title": current_section_name, "content": "\n".join(current_content).strip()})

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sections, f, indent=4, ensure_ascii=False)
        
        print(f"Converted {input_file} -> {output_file}")

if __name__ == "__main__":
    convert_all_docx()
