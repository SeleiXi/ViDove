from pathlib import Path
import argparse
import os

class MultipleLinesConverter:
    """Class for converting multiple lines in txt files to single line"""
    
    def __init__(self, input_dir=None, output_dir=None, overwrite=False):
        """
        Initialize the converter
        
        Args:
            input_dir: Directory containing txt files to process
            output_dir: Directory to save processed files (if None, overwrite original files)
            overwrite: Whether to overwrite original files
        """
        self.input_dir = Path(input_dir) if input_dir else None
        self.output_dir = Path(output_dir) if output_dir else None
        self.overwrite = overwrite
        
    def convert_txt_file(self, txt_path, output_path=None):
        """
        Convert a txt file from multiple lines to single line
        
        Args:
            txt_path: Path to input txt file
            output_path: Path to output file (if None, overwrite original)
            
        Returns:
            Path to output file
        """
        txt_path = Path(txt_path)
        
        if not txt_path.exists():
            print(f"Error: File not found: {txt_path}")
            return None
        
        # Read the file
        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Remove line breaks and join all lines into one
        single_line = ' '.join(line.strip() for line in lines if line.strip())
        
        # Determine output path
        if output_path is None:
            if self.output_dir:
                output_path = self.output_dir / txt_path.name
            else:
                output_path = txt_path  # Overwrite original
        else:
            output_path = Path(output_path)
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write single line to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(single_line)
        
        return output_path
        
    def batch_convert_directory(self):
        """
        Batch convert all txt files in the input directory
        """
        if not self.input_dir or not self.input_dir.exists():
            print(f"Error: Input directory not found: {self.input_dir}")
            return
        
        # Get all txt files
        txt_files = list(self.input_dir.glob("*.txt"))
        
        if not txt_files:
            print(f"No txt files found in {self.input_dir}")
            return
        
        # Create output directory if specified
        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
        processed_files = []
        
        for txt_file in txt_files:
            print(f"Processing: {txt_file}")
            
            # Convert file
            output_path = self.convert_txt_file(txt_file)
            
            if output_path:
                processed_files.append(output_path)
                print(f"Converted: {txt_file} -> {output_path}")
            else:
                print(f"Failed to convert: {txt_file}")
        
        print(f"\nProcessed {len(processed_files)} files successfully")
        return processed_files


def main():
    parser = argparse.ArgumentParser(description='Convert multiple lines in txt files to single line')
    parser.add_argument('--input_dir', '-i', required=True, help='Directory containing txt files to process')
    parser.add_argument('--output_dir', '-o', help='Directory to save processed files (if not specified, overwrite original files)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite original files')
    
    args = parser.parse_args()
    
    # Create converter
    converter = MultipleLinesConverter(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        overwrite=args.overwrite
    )
    
    # Process files
    converter.batch_convert_directory()


if __name__ == "__main__":
    # For direct execution - process dovebench remove_timestamp files
    converter = MultipleLinesConverter(
        input_dir=r"evaluation\test_data\dovebench\remove_timestamp",
        output_dir=r"evaluation\test_data\dovebench\single_line",  # Save to a new directory
        overwrite=False
    )
    
    print("Converting multiple lines to single line...")
    converter.batch_convert_directory()
    
    # Uncomment the line below if you want to use command line arguments instead
    # main()
