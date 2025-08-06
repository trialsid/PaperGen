#!/usr/bin/env python3
"""
Enhanced Paper Builder - Universal MCQ Paper Generator
Supports all question types with flexible configuration
"""

import json
import os
import sys
import argparse
import random
import string
import csv
import traceback
from typing import Dict, List, Optional
from pathlib import Path
import fitz  # PyMuPDF for PDF manipulation

from paper_generators.enhanced_mcq_generator import EnhancedMCQPaperGenerator, MCQConfig, SectionConfig

class BlankPageGenerator(EnhancedMCQPaperGenerator):
    """Generator for blank pages with consistent header, footer, and specific page number."""
    
    def __init__(self, config: Optional[MCQConfig] = None, show_answers: bool = False, 
                 paper_format: str = 'A4', page_number: Optional[int] = None, 
                 show_student_info: bool = True):
        super().__init__(config=config, show_answers=show_answers, paper_format=paper_format,
                        show_student_info=show_student_info)
        self.specified_page_number = page_number
        
    def header(self) -> None:
        # Custom header for empty pages
        header_y = 5
        self.first_page_offset = 0
        
        self.set_y(header_y)
        self.set_font('Noto', 'B', self.config.font_sizes['header'])
        self.cell(self.w - 20, 10, "Empty page for rough work", 0, 1, 'C')
        
        self.line(10, header_y + 10, self.w - 10, header_y + 10)
        self.line(self.w/2, header_y + 10, self.w/2, self.h - 12)
        self.set_xy(10, header_y + 15)

    def footer(self) -> None:
        self.line(10, self.h - 12, self.w - 10, self.h - 12)
        self.set_y(-10)
        self.set_font('Noto', 'I', self.config.font_sizes['footer'])
        # Use specified page number if provided, otherwise fall back to current page_no()
        page_text = f'Page {self.specified_page_number if self.specified_page_number is not None else self.page_no()}'
        self.cell(0, 5, page_text, 0, 0, 'C')

def ensure_directories_exist():
    """Create necessary output directories if they don't exist."""
    directories = [
        'Generated_Papers',
        'Generated_Papers/MCQ',
        'Generated_Papers/MCQ/Enhanced',
        'Generated_Papers/MCQ/Enhanced/Questions',
        'Generated_Papers/MCQ/Enhanced/Answers',
        'Generated_Papers/MCQ/Enhanced/Booklets'
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

def rearrange_for_booklet(input_pdf_path: str, output_pdf_path: str, config: Optional[MCQConfig] = None) -> None:
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
                blank_path = f'temp_blank_{i}.pdf'
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

def load_questions_from_json(file_path: str):
    """Load questions from JSON file and convert to SectionConfig objects."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'sections' not in data:
        raise ValueError("JSON file must contain 'sections' array")
    
    sections = []
    for section_data in data['sections']:
        section = SectionConfig(
            name=section_data.get('name', 'Unnamed Section'),
            description=section_data.get('description', ''),
            questions=section_data.get('questions', [])
        )
        sections.append(section)
    
    return sections

def analyze_question_types(sections):
    """Analyze and display question type distribution."""
    type_counts = {}
    total_questions = 0
    
    for section in sections:
        for question in section.questions:
            # Detect question type from special keywords in question_text
            q_type = 'standard-mcq'  # default
            question_text = question.get('question_text', [])
            
            if isinstance(question_text, list):
                for segment in question_text:
                    if segment == 'STATEMENT':
                        q_type = 'statement-mcq'
                        break
                    elif segment == 'STATEMENTS':
                        q_type = 'multi-statement-mcq'
                        break
                    elif segment == 'LIST':
                        q_type = 'list-mcq'
                        break
                    elif segment == 'MTF_DATA':
                        q_type = 'match-the-following'
                        break
                    elif segment == 'PARAGRAPH':
                        q_type = 'paragraph-mcq'
                        break
            
            type_counts[q_type] = type_counts.get(q_type, 0) + 1
            total_questions += 1
    
    return type_counts, total_questions

def display_analysis(sections, type_counts, total_questions):
    """Display comprehensive analysis of the paper structure."""
    print("=" * 60)
    print("📋 PAPER ANALYSIS")
    print("=" * 60)
    print(f"Total Sections: {len(sections)}")
    print(f"Total Questions: {total_questions}")
    print()
    
    print("Question Types Distribution:")
    for q_type, count in sorted(type_counts.items()):
        percentage = (count / total_questions * 100) if total_questions > 0 else 0
        print(f"  • {q_type}: {count} questions ({percentage:.1f}%)")
    print()
    
    print("Section Breakdown:")
    for i, section in enumerate(sections, 1):
        print(f"  {i}. {section.name}")
        print(f"     Description: {section.description}")
        print(f"     Questions: {len(section.questions)}")
    print()

def get_paper_config(json_filename, custom_title=None, custom_subtitle=None, 
                    custom_exam_title=None, size_config='medium', layout='two-column'):
    """Create paper configuration based on input file and user preferences."""
    base_name = Path(json_filename).stem
    
    title = custom_title or f"Enhanced MCQ Paper"
    subtitle = custom_subtitle or f"Generated from {base_name}.json"
    exam_title = custom_exam_title or f"Multi-Format Question Paper"
    
    return MCQConfig(
        title=title,
        subtitle=subtitle,
        exam_title=exam_title,
        paper_format='A4',
        size_config=size_config,
        layout=layout
    )

def generate_paper(json_file, output_name=None, show_answers=False, paper_set="A", 
                  title=None, subtitle=None, exam_title=None, size_config='medium',
                  layout='two-column', no_student_info=False, interactive=True):
    """Generate MCQ paper from JSON file."""
    try:
        # Load questions
        sections = load_questions_from_json(json_file)
        type_counts, total_questions = analyze_question_types(sections)
        
        if interactive:
            display_analysis(sections, type_counts, total_questions)
        
        # Generate output filename if not provided
        if not output_name:
            base_name = Path(json_file).stem
            suffix = "_answers" if show_answers else ""
            output_name = f"{base_name}_paper{suffix}.pdf"
        
        # Create configuration
        config = get_paper_config(json_file, title, subtitle, exam_title, size_config, layout)
        
        # Create generator
        generator = EnhancedMCQPaperGenerator(
            config=config,
            show_answers=show_answers,
            question_count=total_questions,
            show_student_info=not no_student_info
        )
        
        # Set paper set name
        generator.set_set_name(paper_set)
        
        # Generate paper
        generator.add_page()
        total_marks = generator.generate_from_sections(sections)
        
        # Save the paper
        generator.output(output_name)
        
        # Display results
        paper_type = "Answer Key" if show_answers else "Question Paper"
        print(f"✅ {paper_type} generated successfully!")
        print(f"📄 Output: {output_name}")
        print(f"📊 Questions: {total_questions}")
        print(f"🎯 Total Marks: {total_marks}")
        print(f"📋 Sections: {len(sections)}")
        
        return output_name, total_questions, total_marks
        
    except Exception as e:
        print(f"❌ Error generating paper: {e}")
        if interactive:
            import traceback
            traceback.print_exc()
        raise

def generate_enhanced_mcq_sets_with_keys(
    sections_data: List[Dict],
    num_sets: int,
    output_prefix: str = 'enhanced_mcq_set',
    paper_format: str = 'A4',
    config: Optional[MCQConfig] = None,
    no_shuffle: bool = False,
    no_student_info: bool = False
) -> Dict:
    """Generate Enhanced MCQ sets with sections and answer keys."""
    set_names = list(string.ascii_uppercase[:num_sets])
    set_data = {}
    
    # Ensure output directories exist upfront
    ensure_directories_exist()
    
    # Define output directories for different file types
    question_papers_dir = 'Generated_Papers/MCQ/Enhanced/Questions'
    answer_papers_dir = 'Generated_Papers/MCQ/Enhanced/Answers'
    booklets_dir = 'Generated_Papers/MCQ/Enhanced/Booklets'
    keys_dir = 'Generated_Papers/MCQ/Enhanced'

    # Convert sections data to SectionConfig objects
    base_sections = []
    for section_dict in sections_data:
        section = SectionConfig(
            name=section_dict['name'],
            description=section_dict['description'],
            questions=section_dict['questions']
        )
        base_sections.append(section)
    
    # Calculate total questions
    total_questions = sum(section.required_questions for section in base_sections)
    
    # Process each set
    for set_name in set_names:
        try:
            # Create copies of sections with shuffled questions and options for this set
            set_sections = []
            shuffled_set_data = []  # Store the shuffled data for this set
            
            for section in base_sections:
                # Deep copy questions and prepare shuffled version
                shuffled_questions = []
                for q in section.questions:
                    question_copy = q.copy()
                    # Get all choices including the answer
                    all_choices = question_copy['choices'].copy()
                    correct_answer = q['answer']
                    
                    if not no_shuffle:
                        # Store original indices before shuffling to track answer position
                        original_indices = list(range(len(all_choices)))
                        # Shuffle both choices and indices together
                        combined = list(zip(all_choices, original_indices))
                        random.shuffle(combined)
                        shuffled_choices, shuffled_indices = zip(*combined)
                        
                        # Update the question with shuffled choices
                        question_copy['choices'] = list(shuffled_choices)
                        # Find new position of correct answer
                        correct_index = all_choices.index(correct_answer)
                        new_answer_index = shuffled_indices.index(correct_index)
                        question_copy['answer'] = shuffled_choices[new_answer_index]
                    
                    shuffled_questions.append(question_copy)
                
                # Shuffle questions and store their order
                if not no_shuffle:
                    question_indices = list(range(len(shuffled_questions)))
                    random.shuffle(question_indices)
                    ordered_questions = [shuffled_questions[i] for i in question_indices]
                else:
                    ordered_questions = shuffled_questions
                
                section_copy = SectionConfig(
                    name=section.name,
                    description=section.description,
                    questions=ordered_questions,
                    required_questions=section.required_questions
                )
                set_sections.append(section_copy)
                
                # Store the shuffled data
                shuffled_set_data.append({
                    'section_name': section.name,
                    'questions': ordered_questions.copy()
                })
            
            # Generate question PDF
            pdf = EnhancedMCQPaperGenerator(config=config, show_answers=False, paper_format=paper_format, 
                                           question_count=total_questions, show_student_info=not no_student_info,
                                           strict_ordering=no_shuffle)
            pdf.set_set_name(set_name)
            pdf.add_page()
            total_marks = pdf.generate_from_sections(set_sections)
            
            # Generate answers PDF using same data and ordering
            pdf_answers = EnhancedMCQPaperGenerator(config=config, show_answers=True, paper_format=paper_format, 
                                                   question_count=total_questions, show_student_info=not no_student_info,
                                                   strict_ordering=no_shuffle)
            pdf_answers.set_set_name(set_name)
            pdf_answers.add_page()
            pdf_answers.generate_from_sections(set_sections)
            
            # Generate A3 booklet format
            pdf_booklet = EnhancedMCQPaperGenerator(config=config, show_answers=False, paper_format='A3', 
                                                   question_count=total_questions, show_student_info=not no_student_info,
                                                   strict_ordering=no_shuffle)
            pdf_booklet.set_set_name(set_name)
            pdf_booklet.add_page()
            pdf_booklet.generate_from_sections(set_sections)
            
            # Define file paths
            question_pdf_path = f'{question_papers_dir}/enhanced_mcq_set_{set_name}.pdf'
            answer_pdf_path = f'{answer_papers_dir}/enhanced_mcq_set_{set_name}_answers.pdf'
            booklet_pdf_path = f'{booklets_dir}/enhanced_mcq_set_{set_name}_booklet.pdf'
            
            pdf.output(question_pdf_path)
            pdf_answers.output(answer_pdf_path)
            
            # Create booklet version with proper page ordering
            temp_booklet_path = f'temp_booklet_{set_name}.pdf'
            rearrange_for_booklet(question_pdf_path, temp_booklet_path, config)
            
            # Convert to A3 booklet format
            create_a3_booklet_pdf(temp_booklet_path, booklet_pdf_path)
            
            # Clean up temporary file
            if os.path.exists(temp_booklet_path):
                os.remove(temp_booklet_path)
            
            # Store answer key data
            set_data[f"Set {set_name}"] = {
                'total_marks': total_marks,
                'sections': [
                    {
                        'name': section_data['section_name'],
                        'questions': [
                            {
                                'number': i + 1,
                                'answer': question['answer']
                            }
                            for i, question in enumerate(section_data['questions'][:section.required_questions])
                        ]
                    }
                    for section_data in shuffled_set_data
                ]
            }
            
        except Exception as e:
            print(f"Error generating Set {set_name}: {e}")
            traceback.print_exc()
            continue

    # Generate answer key files
    try:
        # Prepare CSV data
        csv_rows = [['Section', 'Question Number'] + [f'Set {name}' for name in set_names]]
        
        for section_idx, section in enumerate(base_sections):
            for q_num in range(1, section.required_questions + 1):
                row = [section.name, q_num]
                for set_name in set_names:
                    try:
                        section_data = next(
                            s for s in set_data[f"Set {set_name}"]['sections']
                            if s['name'] == section.name
                        )
                        answer = section_data['questions'][q_num - 1]['answer']
                        row.append(answer)
                    except (KeyError, IndexError, StopIteration):
                        row.append('?')
                csv_rows.append(row)
        
        # Write CSV
        with open(f'{keys_dir}/enhanced_mcq_answer_keys.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_rows)
            
        # Write JSON
        with open(f'{keys_dir}/enhanced_mcq_answer_keys_detailed.json', 'w') as f:
            json.dump(set_data, f, indent=2)
            
    except Exception as e:
        print(f"Error generating answer key files: {e}")
        raise
    
    return set_data

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description='Enhanced MCQ Paper Builder - Generate enhanced MCQ papers with multiple question types',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_mcq_paper_builder.py --input-file questions_data/v2.json
  python enhanced_mcq_paper_builder.py --input-file struct2.json --title "Final Exam"
  python enhanced_mcq_paper_builder.py --input-file data.json --size large
  python enhanced_mcq_paper_builder.py --input-file test.json --no-student-info
        """
    )
    
    parser.add_argument('--num-sets', type=int, help='Number of sets to generate (default: 2)')
    parser.add_argument('--title', type=str, help='School name (max 60 characters)')
    parser.add_argument('--subtitle', type=str, help='Subtitle (max 50 characters)')
    parser.add_argument('--exam-title', type=str, help='Exam title (max 50 characters)')
    parser.add_argument('--input-file', type=str, default='questions_data/mcq_questions.json',
                      help='Input JSON file with sections data (default: questions_data/mcq_questions.json)')
    parser.add_argument('--size', type=str, default='medium', choices=['small', 'medium', 'large'],
                      help='Font and spacing size configuration (default: medium)')
    parser.add_argument('--no-student-info', action='store_true',
                      help='Remove student information and instructions from the first page')
    parser.add_argument('--layout', choices=['one-column', 'two-column'], default='two-column',
                      help='Layout type for the paper (one-column or two-column). NOTE: This feature is not fully implemented yet.')
    parser.add_argument('--no-shuffle', action='store_true',
                      help='Do not shuffle questions and options. Questions and answer options will appear in the same order as in the input file, even across multiple sets.')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"❌ Error: File '{args.input_file}' not found!")
        sys.exit(1)
    
    try:
        # Configuration parameters
        NUM_SETS = 2                # Number of sets to generate

        # Override defaults with command line arguments if provided
        if args.num_sets is not None:
            NUM_SETS = args.num_sets
        
        # Get user input for titles if not provided via command line
        title = args.title if args.title else input("Enter school name (max 60 chars): ")
        subtitle = args.subtitle if args.subtitle else input("Enter subtitle (max 50 chars): ")
        exam_title = args.exam_title if args.exam_title else input("Enter exam title (max 50 chars): ")
        
        # Ensure all required directories exist
        ensure_directories_exist()
        
        # Load sections data
        with open(args.input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            sections_data = data['sections']
            
        # Calculate total questions across all sections
        total_questions = sum(len(section['questions']) for section in sections_data)
        
        print(f"Loaded {len(sections_data)} sections with {total_questions} total questions")
        for section in sections_data:
            print(f"  - {section['name']}: {len(section['questions'])} questions")
        
        print(f"\nGenerating {NUM_SETS} enhanced MCQ sets...")
        
        config = MCQConfig(
            title=title,
            subtitle=subtitle,
            exam_title=exam_title,
            paper_format='A4',
            size_config=args.size,
            layout=args.layout  # Note: Layout setting is stored but not fully implemented in paper generation logic yet
        )
        
        # Generate all sets
        answer_keys = generate_enhanced_mcq_sets_with_keys(
            sections_data=sections_data,
            num_sets=NUM_SETS,
            output_prefix='Generated_Papers/MCQ/Enhanced/Questions/enhanced_mcq_set',
            paper_format='A4',
            config=config,
            no_shuffle=args.no_shuffle,
            no_student_info=args.no_student_info
        )
        
        print("\nGeneration complete!")
        print("Files generated:")
        print("  - Question papers: Generated_Papers/MCQ/Enhanced/Questions/")
        print("  - Answer keys: Generated_Papers/MCQ/Enhanced/Answers/")
        print("  - Booklets (A3): Generated_Papers/MCQ/Enhanced/Booklets/")
        print("  - Answer key CSV: Generated_Papers/MCQ/Enhanced/enhanced_mcq_answer_keys.csv")
        print("  - Detailed JSON: Generated_Papers/MCQ/Enhanced/enhanced_mcq_answer_keys_detailed.json")
        
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