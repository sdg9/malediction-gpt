#!/usr/bin/env python3
"""
Malediction PDF to Text Converter

This script converts PDF files to text format with page markers.
It automatically detects all PDF files in the input directory and
processes them to the output directory with the same filename but
.txt extension.

Usage:
    python3 src/pdfToText.py

Requirements:
    - PyPDF2 (see requirements.txt)
    - PDF files in input/ directory
"""

from PyPDF2 import PdfReader
import os
import glob

def convert_pdf_to_text(pdf_filename, output_filename):
    """Convert a PDF file to text with page markers.
    
    Args:
        pdf_filename (str): Path to the input PDF file
        output_filename (str): Path to the output text file
        
    Returns:
        bool: True if conversion successful, False otherwise
    """
    print(f"Processing {pdf_filename}...")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    try:
        reader = PdfReader(pdf_filename)
        with open(output_filename, "w", encoding="utf-8") as out:
            for i, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                out.write(f"[Page {i}]\n")
                out.write(text or "")
                out.write("\n\n")
        
        print(f"Completed! Output written to {output_filename}")
        return True
    except Exception as e:
        print(f"Error processing {pdf_filename}: {e}")
        return False

    print(f"\nProcessing complete! Successfully converted {successful_conversions}/{total_files} files.")
    if successful_conversions > 0:
        print(f"Output files saved to: {output_dir}")


def main():
    """Main function to process all PDF files in input directory."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory (project root)
    project_root = os.path.dirname(script_dir)

    # Find all PDF files in the input directory
    input_dir = os.path.join(project_root, "input")
    output_dir = os.path.join(project_root, "output")

    # Use glob to find all PDF files (case-insensitive)
    pdf_pattern = os.path.join(input_dir, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)

    # Also check for uppercase PDF extension
    pdf_pattern_upper = os.path.join(input_dir, "*.PDF")
    pdf_files.extend(glob.glob(pdf_pattern_upper))

    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        print("Please place your PDF files in the input/ directory.")
        return

    successful_conversions = 0
    total_files = len(pdf_files)
    
    print(f"Found {total_files} PDF file(s) to process:")
    for pdf_file in pdf_files:
        print(f"  - {os.path.basename(pdf_file)}")
    print()
    
    # Process each PDF file
    for pdf_path in pdf_files:
        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        # Create output filename with .txt extension
        output_filename = f"{base_name}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        # Convert the PDF
        if convert_pdf_to_text(pdf_path, output_path):
            successful_conversions += 1
    
    print(f"\nProcessing complete! Successfully converted {successful_conversions}/{total_files} files.")
    if successful_conversions > 0:
        print(f"Output files saved to: {output_dir}")


if __name__ == "__main__":
    main()