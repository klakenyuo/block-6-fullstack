import os
import pandas as pd
from tika import parser
import warnings
import re
warnings.filterwarnings('ignore')

def clean_text(text):
    """Clean the extracted text by removing commas and unnecessary whitespace."""
    if not text:
        return ""
    # Replace commas with spaces
    text = text.replace(',', ' ')
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove any non-printable characters
    text = ''.join(char for char in text if char.isprintable())
    return text.strip()

def extract_text_from_file(file_path):
    """Extract text from a document file using Apache Tika."""
    try:
        parsed = parser.from_file(file_path)
        if parsed["content"]:
            # Clean the extracted text
            return clean_text(parsed["content"])
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
    return ""

def create_dataset():
    """Create a dataset from CV files."""
    base_dir = "resumes"
    data = []
    
    # Walk through all CV directories
    for dir_name in os.listdir(base_dir):
        if dir_name.startswith("CV "):
            # Extract category name
            category = dir_name.replace("CV ", "")
            dir_path = os.path.join(base_dir, dir_name)
            
            if os.path.isdir(dir_path):
                # Walk through all files in the directory and its subdirectories
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        # Skip hidden files and non-document files
                        if not file.startswith('.'):
                            file_path = os.path.join(root, file)
                            # Extract text from the file
                            text = extract_text_from_file(file_path)
                            if text:
                                data.append({
                                    'category': category,
                                    'resume': text
                                })
                                print(f"Processed: {file_path}")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV with proper escaping and encoding
    output_file = "cv_dataset.csv"
    df.to_csv(output_file, index=False, quoting=1, escapechar='\\')
    print(f"\nDataset created successfully with {len(df)} entries")
    print(f"Saved to: {output_file}")
    
    return df

if __name__ == "__main__":
    print("Starting to create dataset...")
    df = create_dataset()
    print("\nSample of the dataset:")
    print(df.head())
