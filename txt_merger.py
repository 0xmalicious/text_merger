import os
import sys
import subprocess

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import chardet, install if it is not available
try:
    import chardet
except ImportError:
    print("chardet not found, installing...")
    install_package("chardet")
    import chardet

# Try to import tqdm, install if it is not available
try:
    import tqdm
except ImportError:
    print("tqdm not found, installing...")
    install_package("tqdm")
    from tqdm import tqdm
else:
    from tqdm import tqdm

def get_unique_filename(base_name, extension, directory):
    # Generate a unique filename in the given directory.
    counter = 0
    filename = f"{base_name}{extension}"
    while os.path.exists(os.path.join(directory, filename)):
        counter += 1
        filename = f"{base_name}{counter}{extension}"
    return os.path.join(directory, filename)

def detect_encoding(file_path):
    # Detect the encoding of a file using chardet.
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def try_multiple_encodings(file_path, encodings=['utf-8', 'latin1', 'iso-8859-1']):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read(), encoding
        except Exception as e:
            continue
    return None, None

def fuse_text_files(directory):
    # Get the unique filename for the final output file
    output_file_path = get_unique_filename("fused", ".txt", directory)
    
    # List all .txt files in the directory
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    failed_files = []
    # Merge the txt files in the final output file
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for idx, txt_file in enumerate(tqdm(txt_files, desc="Merging files")):
            txt_file_path = os.path.join(directory, txt_file)
            try:
                content, encoding_used = try_multiple_encodings(txt_file_path)
                if content is None:
                    raise Exception("Failed to decode with all tested encodings")
                outfile.write(content)
                outfile.write("\n\n")  # Add a blank line between files for readability
                tqdm.write(f"Processed file {idx+1}/{len(txt_files)}: {txt_file} (encoding: {encoding_used})")
            except Exception as e:
                print(f"Failed to process file {txt_file_path}: {e}")
                failed_files.append(txt_file_path)
    
    print(f"All files have been fused into: {output_file_path}")
    if failed_files:
        print("The following files could not be added to the final output file due to errors:")
        for file in failed_files:
            print(file)

if __name__ == "__main__":
    # Ask the user for the directory path
    directory = input("Please enter the path to the directory containing the .txt files: ")
    
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist.")
    else:
        # Fuse the text files in the specified directory
        fuse_text_files(directory)
