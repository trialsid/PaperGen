#!/usr/bin/env python3
"""
Enhanced Paper Builder - Universal MCQ Paper Generator
Supports all question types with flexible configuration
"""

import json
import os
import sys
import argparse
from pathlib import Path
from paper_generators.enhanced_mcq_generator import EnhancedMCQPaperGenerator, MCQConfig, SectionConfig

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
    
    parser.add_argument('--input-file', type=str, default='questions_data/mcq_questions.json',
                       help='Input JSON file with questions data (default: questions_data/mcq_questions.json)')
    parser.add_argument('--title', type=str,
                       help='School name (max 60 characters)')
    parser.add_argument('--subtitle', type=str,
                       help='Subtitle (max 50 characters)')
    parser.add_argument('--exam-title', type=str,
                       help='Exam title (max 50 characters)')
    parser.add_argument('--size', type=str, default='medium', choices=['small', 'medium', 'large'],
                       help='Font and spacing size configuration (default: medium)')
    parser.add_argument('--no-student-info', action='store_true',
                       help='Remove student information and instructions from the first page')
    parser.add_argument('--layout', choices=['one-column', 'two-column'], default='two-column',
                       help='Layout type for the paper (one-column or two-column). NOTE: This feature is not fully implemented yet.')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"❌ Error: File '{args.input_file}' not found!")
        sys.exit(1)
    
    try:
        # Get user input for titles if not provided via command line (same as mcq_paper_builder.py)
        title = args.title if args.title else input("Enter school name (max 60 chars): ")
        subtitle = args.subtitle if args.subtitle else input("Enter subtitle (max 50 chars): ")
        exam_title = args.exam_title if args.exam_title else input("Enter exam title (max 50 chars): ")
        
        # Load and analyze questions
        sections = load_questions_from_json(args.input_file)
        type_counts, total_questions = analyze_question_types(sections)
        
        display_analysis(sections, type_counts, total_questions)
        
        # Generate auto-named output files based on input filename
        base_name = Path(args.input_file).stem
        question_output = f"{base_name}_paper.pdf"
        answer_output = f"{base_name}_paper_answers.pdf"
        
        # Create configuration
        config = get_paper_config(args.input_file, title, subtitle, exam_title, args.size, args.layout)
        
        print("Generating question paper...")
        # Generate question paper
        generator = EnhancedMCQPaperGenerator(
            config=config,
            show_answers=False,
            question_count=total_questions,
            show_student_info=not args.no_student_info
        )
        generator.set_set_name("A")
        generator.add_page()
        total_marks = generator.generate_from_sections(sections)
        generator.output(question_output)
        
        print("Generating answer key...")
        # Generate answer key
        answer_generator = EnhancedMCQPaperGenerator(
            config=config,
            show_answers=True,
            question_count=total_questions,
            show_student_info=not args.no_student_info
        )
        answer_generator.set_set_name("A")
        answer_generator.add_page()
        answer_generator.generate_from_sections(sections)
        answer_generator.output(answer_output)
        
        print("\nGeneration complete!")
        print(f"✅ Question Paper: {question_output}")
        print(f"✅ Answer Key: {answer_output}")
        print(f"📊 Total Questions: {total_questions}")
        print(f"🎯 Total Marks: {total_marks}")
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()