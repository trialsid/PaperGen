#!/usr/bin/env python3
"""
Test script for v2.json with enhanced MCQ generator
"""

import json
import os
from paper_generators.enhanced_mcq_generator import EnhancedMCQPaperGenerator, MCQConfig, SectionConfig

def load_questions_from_json(file_path: str):
    """Load questions from JSON file and convert to SectionConfig objects."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sections = []
    for section_data in data['sections']:
        section = SectionConfig(
            name=section_data['name'],
            description=section_data['description'],
            questions=section_data['questions']
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
            q_type = 'mcq'  # default
            question_text = question.get('question_text', [])
            if isinstance(question_text, list):
                for segment in question_text:
                    if segment == 'STATEMENT' or segment == 'STATEMENTS':
                        q_type = 's-mcq'
                        break
                    elif segment == 'LIST':
                        q_type = 'list-mcq'
                        break
                    elif segment == 'MTF_DATA':
                        q_type = 'mtf-mcq'
                        break
                    elif segment == 'PARAGRAPH':
                        q_type = 'p-mcq'
                        break
            
            type_counts[q_type] = type_counts.get(q_type, 0) + 1
            total_questions += 1
    
    return type_counts, total_questions

def main():
    """Generate test paper from v2.json with enhanced MCQ generator."""
    try:
        # Load questions from v2.json
        json_file = "questions_data/v2.json"
        if not os.path.exists(json_file):
            print(f"Error: {json_file} not found!")
            return
        
        sections = load_questions_from_json(json_file)
        
        # Analyze question types
        type_counts, total_questions = analyze_question_types(sections)
        
        # Display paper structure
        print("📋 Paper Structure from v2.json:")
        print(f"   Total Sections: {len(sections)}")
        print(f"   Total Questions: {total_questions}")
        print("   Question Types Distribution:")
        for q_type, count in sorted(type_counts.items()):
            print(f"     - {q_type}: {count} questions")
        print()
        
        print(f"✅ Loaded {len(sections)} sections")
        
        # Display section details
        for i, section in enumerate(sections):
            section_types = {}
            for q in section.questions:
                # Detect question type
                q_type = 'mcq'  # default
                question_text = q.get('question_text', [])
                if isinstance(question_text, list):
                    for segment in question_text:
                        if segment in ['STATEMENT', 'STATEMENTS']:
                            q_type = 's-mcq'
                            break
                        elif segment == 'LIST':
                            q_type = 'list-mcq'
                            break
                        elif segment == 'MTF_DATA':
                            q_type = 'mtf-mcq'
                            break
                        elif segment == 'PARAGRAPH':
                            q_type = 'p-mcq'
                            break
                
                section_types[q_type] = section_types.get(q_type, 0) + 1
            
            type_summary = ", ".join([f"{count} {q_type}" for q_type, count in sorted(section_types.items())])
            print(f"   Section {i+1} ({section.name}): {type_summary}")
        print()
        
        # Create configuration
        config = MCQConfig(
            title="Enhanced MCQ Paper",
            subtitle="Generated from v2.json", 
            exam_title="Multi-Format Question Paper",
            paper_format='A4',
            size_config='small'
        )
        
        # Create generator with enhanced support
        generator = EnhancedMCQPaperGenerator(
            config=config,
            show_answers=False,
            question_count=total_questions
        )
        
        # Set the paper set name
        generator.set_set_name("A")
        
        # Add first page
        generator.add_page()
        
        # Generate paper from sections
        total_marks = generator.generate_from_sections(sections)
        
        # Save the paper
        output_file = "v2_paper.pdf"
        generator.output(output_file)
        
        print(f"✅ Enhanced MCQ Paper generated successfully!")
        print(f"📄 Output: {output_file}")
        print(f"📊 Total Questions: {generator.question_count}")
        print(f"🎯 Total Marks: {total_marks}")
        print(f"📋 Sections: {len(sections)}")
        
        # Generate answer key
        answer_choice = input("Generate answer key? (y/n): ").lower()
        if answer_choice == 'y':
            answer_generator = EnhancedMCQPaperGenerator(
                config=config,
                show_answers=True,
                question_count=total_questions
            )
            answer_generator.set_set_name("A")
            answer_generator.add_page()
            answer_generator.generate_from_sections(sections)
            
            answer_file = "v2_paper_answers.pdf"
            answer_generator.output(answer_file)
            print(f"✅ Answer key generated: {answer_file}")
        
    except Exception as e:
        print(f"❌ Error generating paper: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()