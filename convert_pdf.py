from markitdown import MarkItDown
import os

# Define paths
input_path = os.path.abspath("data/contoso_handbook.pdf")
output_path = os.path.abspath("data/contoso_handbook.md")

print(f"Converting {input_path} to {output_path}...")

try:
    md = MarkItDown()
    result = md.convert(input_path)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.text_content)
        
    print("Conversion successful!")
except Exception as e:
    print(f"Error during conversion: {e}")
