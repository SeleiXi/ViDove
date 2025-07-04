# input = C:\TEMP2\coding\0_Recent\vidove\ViDove\evaluation\test_data\dovebench\ref
# output = C:\TEMP2\coding\0_Recent\vidove\ViDove\evaluation\test_data\dovebench_gt.zh

# 先用remove_timestamp.py把srt文件转txt文件

# 再用combine_multiple_line_txt_to_single_line.py把txt文件合并到一行

# 然后用generate_eval_gt_file.py生成gt文件

from pathlib import Path
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from remove_timestamp import RemoveTimestampConverter
from combine_multiple_line_txt_to_single_line import MultipleLinesConverter
from generate_eval_gt_file import EvalGroundTruthGenerator


class DoveBenchParser:
    """Complete pipeline for processing DoveBench data from SRT to ground truth"""
    
    def __init__(self, input_dir=None, output_file=None, id_file=None):
        """
        Initialize the parser
        
        Args:
            input_dir: Directory containing SRT files (ref directory)
            output_file: Path to final ground truth file
            id_file: Path to ID file for processing order
        """
        self.input_dir = Path(input_dir) if input_dir else None
        self.output_file = Path(output_file) if output_file else None
        self.id_file = Path(id_file) if id_file else None
        
        # Create intermediate directories
        self.base_dir = self.input_dir.parent if self.input_dir else None
        self.remove_timestamp_dir = self.base_dir / "remove_timestamp" if self.base_dir else None
        self.single_line_dir = self.base_dir / "single_line" if self.base_dir else None
        
    def step1_remove_timestamp(self):
        """Step 1: Convert SRT files to TXT files by removing timestamps"""
        print("=" * 50)
        print("Step 1: Converting SRT files to TXT files (removing timestamps)")
        print("=" * 50)
        
        if not self.input_dir or not self.input_dir.exists():
            print(f"Error: Input directory not found: {self.input_dir}")
            return False
            
        if not self.id_file or not self.id_file.exists():
            print(f"Error: ID file not found: {self.id_file}")
            return False
        
        # Create output directory
        self.remove_timestamp_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize converter
        converter = RemoveTimestampConverter(
            id_list=str(self.id_file),
            target_srt_dir=str(self.input_dir),
            output_dir=str(self.remove_timestamp_dir)
        )
        
        # Process files
        try:
            processed_files = converter.process_id_list_to_separate_files()
            if processed_files:
                print(f"Step 1 completed successfully. Processed {len(processed_files)} files.")
                return True
            else:
                print("Step 1 failed: No files were processed.")
                return False
        except Exception as e:
            print(f"Step 1 failed with error: {e}")
            return False
    
    def step2_combine_multiple_lines(self):
        """Step 2: Combine multiple lines in TXT files to single line"""
        print("=" * 50)
        print("Step 2: Combining multiple lines to single line")
        print("=" * 50)
        
        if not self.remove_timestamp_dir or not self.remove_timestamp_dir.exists():
            print(f"Error: Remove timestamp directory not found: {self.remove_timestamp_dir}")
            return False
        
        # Create output directory
        self.single_line_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize converter
        converter = MultipleLinesConverter(
            input_dir=str(self.remove_timestamp_dir),
            output_dir=str(self.single_line_dir),
            overwrite=False
        )
        
        # Process files
        try:
            processed_files = converter.batch_convert_directory()
            if processed_files:
                print(f"Step 2 completed successfully. Processed {len(processed_files)} files.")
                return True
            else:
                print("Step 2 failed: No files were processed.")
                return False
        except Exception as e:
            print(f"Step 2 failed with error: {e}")
            return False
    
    def step3_generate_ground_truth(self):
        """Step 3: Generate ground truth file by combining all files in order"""
        print("=" * 50)
        print("Step 3: Generating ground truth file")
        print("=" * 50)
        
        if not self.single_line_dir or not self.single_line_dir.exists():
            print(f"Error: Single line directory not found: {self.single_line_dir}")
            return False
        
        # Create output directory
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize generator
        generator = EvalGroundTruthGenerator(
            id_file=str(self.id_file),
            input_dir=str(self.single_line_dir),
            output_file=str(self.output_file)
        )
        
        # Generate ground truth file
        try:
            result_file = generator.generate_ground_truth_file()
            if result_file:
                print(f"Step 3 completed successfully. Generated: {result_file}")
                return True
            else:
                print("Step 3 failed: Ground truth file was not generated.")
                return False
        except Exception as e:
            print(f"Step 3 failed with error: {e}")
            return False
    
    def run_complete_pipeline(self):
        """Run the complete pipeline"""
        print("Starting DoveBench processing pipeline...")
        print(f"Input directory: {self.input_dir}")
        print(f"Output file: {self.output_file}")
        print(f"ID file: {self.id_file}")
        print()
        
        # Step 1: Remove timestamps
        if not self.step1_remove_timestamp():
            print("Pipeline failed at Step 1")
            return False
        
        # Step 2: Combine multiple lines
        if not self.step2_combine_multiple_lines():
            print("Pipeline failed at Step 2")
            return False
        
        # Step 3: Generate ground truth
        if not self.step3_generate_ground_truth():
            print("Pipeline failed at Step 3")
            return False
        
        print("=" * 50)
        print("🎉 DoveBench processing pipeline completed successfully!")
        print(f"📄 Final output: {self.output_file}")
        print("=" * 50)
        return True


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process DoveBench data from SRT to ground truth')
    parser.add_argument('--input_dir', '-i', required=True, help='Directory containing SRT files')
    parser.add_argument('--output_file', '-o', required=True, help='Output ground truth file')
    parser.add_argument('--id_file', '-id', required=True, help='ID file for processing order')
    
    args = parser.parse_args()
    
    processor = DoveBenchParser(
        input_dir=args.input_dir,
        output_file=args.output_file,
        id_file=args.id_file
    )
    
    success = processor.run_complete_pipeline()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # For direct execution - process dovebench files
    processor = DoveBenchParser(
        input_dir=r"evaluation\test_data\dovebench\ref",  # Changed from ref to dovebench since that's where SRT files are
        output_file=r"evaluation\test_data\dovebench_gt.zh",
        id_file=r"evaluation\test_data\dovebench.id"
    )
    
    processor.run_complete_pipeline()
    
    # Uncomment the line below if you want to use command line arguments instead
    # main()
    








