# 用来生成text_data_test.en / text_data_test.zh文件的
from pathlib import Path
import argparse


class EvalGroundTruthGenerator:
    """Class for generating evaluation ground truth files"""
    
    def __init__(self, id_file=None, input_dir=None, output_file=None):
        """
        Initialize the generator
        
        Args:
            id_file: Path to file containing IDs in order
            input_dir: Directory containing txt files to process
            output_file: Path to output file
        """
        self.id_file = Path(id_file) if id_file else None
        self.input_dir = Path(input_dir) if input_dir else None
        self.output_file = Path(output_file) if output_file else None
    
    def generate_ground_truth_file(self):
        """
        Generate ground truth file by combining txt files in ID order
        """
        if not self.id_file or not self.id_file.exists():
            print(f"Error: ID file not found: {self.id_file}")
            return
        
        if not self.input_dir or not self.input_dir.exists():
            print(f"Error: Input directory not found: {self.input_dir}")
            return
        
        # Read IDs from file
        with open(self.id_file, 'r', encoding='utf-8') as f:
            ids = [line.strip() for line in f if line.strip()]
        
        print(f"Found {len(ids)} IDs to process")
        
        # Create output directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Process each ID in order
        all_texts = []
        missing_files = []
        
        for file_id in ids:
            txt_path = self.input_dir / f"{file_id}.txt"
            
            if not txt_path.exists():
                print(f"Warning: File not found for ID: {file_id}")
                missing_files.append(file_id)
                continue
            
            # Read the content of the txt file
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                if content:
                    all_texts.append(content)
                    print(f"Added: {file_id}")
                else:
                    print(f"Warning: Empty file: {file_id}")
                    
            except Exception as e:
                print(f"Error reading {txt_path}: {e}")
                missing_files.append(file_id)
        
        # Write all texts to output file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_texts))
        
        print(f"\nGenerated ground truth file: {self.output_file}")
        print(f"Total entries: {len(all_texts)}")
        
        if missing_files:
            print(f"Warning: {len(missing_files)} files were missing: {', '.join(missing_files)}")
        
        return self.output_file


def main():
    parser = argparse.ArgumentParser(description='Generate evaluation ground truth files')
    parser.add_argument('--id_file', '-i', required=True, help='Path to ID file')
    parser.add_argument('--input_dir', '-d', required=True, help='Directory containing txt files')
    parser.add_argument('--output_file', '-o', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    generator = EvalGroundTruthGenerator(
        id_file=args.id_file,
        input_dir=args.input_dir,
        output_file=args.output_file
    )
    
    generator.generate_ground_truth_file()


if __name__ == "__main__":
    # For direct execution - process dovebench files
    generator = EvalGroundTruthGenerator(
        id_file=r"evaluation\test_data\dovebench.id",
        input_dir=r"evaluation\test_data\dovebench\single_line",
        output_file=r"evaluation\test_data\cs2_dovebench.zh"
    )
    
    print("Generating CS2 DoveBench ground truth file...")
    generator.generate_ground_truth_file()
    
    # Uncomment the line below if you want to use command line arguments instead
    # main()