import argparse
import json
import os
import traceback
import fitz  # PyMuPDF for PDF manipulation
from typing import List, Dict, Optional

from paper_generators import (
    MixedPaperGenerator,
    MixedConfig,
    MixedSectionConfig
)

class BlankPageGenerator(MixedPaperGenerator):
    """Generator for blank pages with consistent header, footer, and specific page number."""
    
    def __init__(self, config: Optional[MixedConfig] = None, paper_format: str = 'A4', 
                 page_number: Optional[int] = None, show_student_info: bool = True):
        super().__init__(config=config, show_student_info=show_student_info)
        self.specified_page_number = page_number
        self.paper_format = paper_format
        
    def header(self) -> None:
        # Custom header for empty pages
        header_y = 5
        
        self.set_y(header_y)
        self.set_font('Noto', 'B', self.config.font_sizes['header'])  # Use config font size
        self.cell(self.w - 20, 10, "Empty page for rough work", 0, 1, 'C')
        
        self.line(10, header_y + 10, self.w - 10, header_y + 10)
        self.line(self.w/2, header_y + 10, self.w/2, self.h - 12)
        self.set_xy(10, header_y + 15)

    def footer(self) -> None:
        self.line(10, self.h - 12, self.w - 10, self.h - 12)
        self.set_y(-10)
        self.set_font('Noto', 'I', self.config.font_sizes['footer'])  # Use config font size
        # Use specified page number if provided, otherwise fall back to current page_no()
        page_text = f'Page {self.specified_page_number if self.specified_page_number is not None else self.page_no()}'
        self.cell(0, 5, page_text, 0, 0, 'C')

def ensure_directories_exist():
    """Create necessary output directories if they don't exist."""
    directories = [
        'Generated_Papers',
        'Generated_Papers/Mixed',
        'Generated_Papers/Mixed/Questions',
        'Generated_Papers/Mixed/Answers',
        'Generated_Papers/Mixed/Booklets'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def create_a3_booklet_pdf(input_pdf_path: str, output_pdf_path: str) -> None:
    """
    Convert an A4 PDF in booklet order into an A3-sized booklet PDF with two A4 pages per A3 page.
    """
    try:
        doc = fitz.open(input_pdf_path)
        n = len(doc)

        if n == 0:
            print(f"Warning: Input PDF {input_pdf_path} has no pages. Skipping booklet creation.")
            return

        # Calculate the total number of pages needed (multiple of 4)
        pad_n = ((n + 3) // 4) * 4
        
        # Create A3 pages with A4 page pairs
        a3_doc = fitz.open()
        pairs = [(i, i+1) for i in range(0, pad_n, 2)]
        
        # Pre-define standard rectangles for left and right pages
        rect_left = fitz.Rect(0, 0, 595, 842)
        rect_right = fitz.Rect(595, 0, 1191, 842)
        
        for i, j in pairs:
            a3_page = a3_doc.new_page(width=1191, height=842)
            try:
                if i < n:
                    a3_page.show_pdf_page(rect_left, doc, i)
            except ValueError as e:
                print(f"Warning: Could not add page {i} to booklet: {e}")
                
            try:
                if j < n:
                    a3_page.show_pdf_page(rect_right, doc, j)
            except ValueError as e:
                print(f"Warning: Could not add page {j} to booklet: {e}")

        a3_doc.save(output_pdf_path)
        a3_doc.close()
        doc.close()
        print(f"Successfully created A3 booklet: {output_pdf_path}")
    except Exception as e:
        print(f"Error creating A3 booklet: {e}")
        traceback.print_exc()

def rearrange_for_booklet(input_pdf_path: str, output_pdf_path: str, config: Optional[MixedConfig] = None) -> None:
    """
    Rearrange pages of an input A4 PDF into booklet order.
    """
    try:
        doc = fitz.open(input_pdf_path)
        n = len(doc)  # Number of pages in the original document

        if n == 0:
            print(f"Warning: Input PDF {input_pdf_path} has no pages. Skipping booklet rearrangement.")
            # Create an empty PDF with a styled blank page
            if config:
                blank_generator = BlankPageGenerator(config=config, paper_format='A4', page_number=1)
                blank_generator.add_page()
                blank_generator.output(output_pdf_path)
            else:
                empty_doc = fitz.open()
                empty_doc.new_page()
                empty_doc.save(output_pdf_path)
                empty_doc.close()
            doc.close()
            return

        # Calculate the total number of pages needed (multiple of 4)
        pad_n = ((n + 3) // 4) * 4
        num_blank_pages = pad_n - n  # Number of blank pages to add

        # Create all blank pages at once if needed
        blank_pages = []
        if num_blank_pages > 0 and config:
            for i in range(num_blank_pages):
                page_num = n + i + 1
                blank_path = f'temp_blank_mixed_{i}.pdf'
                blank_generator = BlankPageGenerator(config=config, paper_format='A4', page_number=page_num)
                blank_generator.add_page()
                blank_generator.output(blank_path)
                blank_pages.append(blank_path)
                
            # Add blank pages to the document
            for blank_path in blank_pages:
                blank_doc = fitz.open(blank_path)
                doc.insert_pdf(blank_doc)
                blank_doc.close()

        # Generate booklet sequence
        sequence = []
        for i in range(0, pad_n // 2, 2):
            sequence.extend([
                pad_n - i - 1,  # Back page
                i,              # Front page
                i + 1,          # Inside front
                pad_n - i - 2   # Inside back
            ])

        # Create booklet-ordered PDF
        booklet_doc = fitz.open()
        for idx in sequence:
            if idx < doc.page_count:
                try:
                    booklet_doc.insert_pdf(doc, from_page=idx, to_page=idx)
                except Exception as e:
                    print(f"Warning: Could not insert page {idx}: {e}")
                    # Add a blank page instead
                    booklet_doc.new_page()
            else:
                # Add a blank page
                booklet_doc.new_page()

        booklet_doc.save(output_pdf_path)
        booklet_doc.close()
        doc.close()
        
        # Clean up temporary files
        for blank_path in blank_pages:
            if os.path.exists(blank_path):
                os.remove(blank_path)
                
        print(f"Successfully rearranged pages for booklet: {output_pdf_path}")
    except Exception as e:
        print(f"Error rearranging pages for booklet: {e}")
        traceback.print_exc()

def generate_mixed_paper(sections_data: List[Dict], output_path: str, config: MixedConfig = None, show_student_info: bool = True) -> None:
    """Generate a mixed question paper from sections data."""
    # Create sections
    sections = []
    for section_dict in sections_data:
        section = MixedSectionConfig(
            name=section_dict['name'],
            description=section_dict['description'],
            section_type=section_dict['section_type'],
            questions=section_dict['questions']
        )
        sections.append(section)
    
    # Create and generate the paper
    generator = MixedPaperGenerator(config=config, show_student_info=show_student_info)
    generator.generate_paper(sections)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the paper
    generator.output(output_path)
    
    # Create booklet version if this is a question paper
    if '/Questions/' in output_path:
        # Create paths for booklet
        booklet_dir = os.path.dirname(output_path).replace('/Questions/', '/Booklets/')
        os.makedirs(booklet_dir, exist_ok=True)
        booklet_path = os.path.join(booklet_dir, os.path.basename(output_path).replace('.pdf', '_booklet.pdf'))
        
        # Create temporary file for booklet arrangement
        temp_booklet_path = f'temp_mixed_booklet.pdf'
        
        # Rearrange pages for booklet
        rearrange_for_booklet(output_path, temp_booklet_path, config)
        
        # Convert to A3 booklet
        create_a3_booklet_pdf(temp_booklet_path, booklet_path)
        
        # Clean up temporary file
        if os.path.exists(temp_booklet_path):
            os.remove(temp_booklet_path)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate mixed question papers')
    parser.add_argument('--input-file', type=str, default='mixed_questions.json',
                      help='Input JSON file with sections data (default: mixed_questions.json)')
    parser.add_argument('--output-file', type=str, 
                      default='Generated_Papers/Mixed/Questions/mixed_paper.pdf',
                      help='Output PDF file path')
    parser.add_argument('--title', type=str, help='School name (max 60 characters)')
    parser.add_argument('--subtitle', type=str, help='Subtitle (max 50 characters)')
    parser.add_argument('--exam-title', type=str, help='Exam title (max 50 characters)')
    parser.add_argument('--size', type=str, default='medium', choices=['small', 'medium', 'large'],
                      help='Font and spacing size configuration (default: medium)')
    parser.add_argument('--no-student-info', action='store_true',
                      help='Remove student information and instructions from the first page')
    args = parser.parse_args()
    
    try:
        # Get user input for titles if not provided via command line
        title = args.title if args.title else input("Enter school name (max 60 chars): ")
        subtitle = args.subtitle if args.subtitle else input("Enter subtitle (max 50 chars): ")
        exam_title = args.exam_title if args.exam_title else input("Enter exam title (max 50 chars): ")
        
        # Create configuration
        config = MixedConfig(
            title=title,
            subtitle=subtitle,
            exam_title=exam_title,
            paper_format='A4',
            size_config=args.size
        )
        
        # Load sections data
        with open(args.input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            sections_data = data['sections']
        
        # Generate the paper
        generate_mixed_paper(sections_data, args.output_file, config, show_student_info=not args.no_student_info)
        
        print(f"\nPaper generated successfully at: {args.output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found!")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {args.input_file}!")
    except ValueError as ve:
        print(f"Error: {str(ve)}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 