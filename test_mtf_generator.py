#!/usr/bin/env python3
"""
Test script for Enhanced MCQ Paper Generator
Demonstrates generation of papers with both Normal MCQs and MTF (Match the Following) MCQs
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

def main():
    """Generate test paper with both Normal MCQs and MTF MCQs."""
    try:
        # Load questions from enhanced struct.json
        struct_file = "questions_data/struct.json"
        if not os.path.exists(struct_file):
            print(f"Error: {struct_file} not found!")
            return
        
        sections = load_questions_from_json(struct_file)
        
        # Calculate statistics dynamically
        total_sections = len(sections)
        total_questions = sum(len(s.questions) for s in sections)
        total_mcq = sum(sum(1 for q in s.questions if q.get('question_type', 'mcq') == 'mcq') for s in sections)
        total_mtf = sum(sum(1 for q in s.questions if q.get('question_type') == 'mtf-mcq') for s in sections)
        questions_per_section = total_questions // total_sections if total_sections > 0 else 0
        
        # Display paper structure
        print("📋 Paper Structure:")
        print(f"   Description: Mixed MCQ Question Paper with Normal MCQs and MTF (Match the Following) MCQs")
        print(f"   Total Sections: {total_sections}")
        print(f"   Questions per Section: {questions_per_section}")
        print(f"   Distribution: {total_mtf} MTF-MCQ + {total_mcq} Normal MCQ total")
        print()
        
        print(f"✅ Loaded {len(sections)} sections")
        
        # Analyze question types in each section
        for i, section in enumerate(sections):
            mcq_count = sum(1 for q in section.questions if q.get('question_type', 'mcq') == 'mcq')
            mtf_count = sum(1 for q in section.questions if q.get('question_type') == 'mtf-mcq')
            print(f"   Section {i+1}: {mtf_count} MTF-MCQ + {mcq_count} Normal MCQ = {len(section.questions)} total")
        print()
        
        # Create configuration
        config = MCQConfig(
            title="ABC International School",
            subtitle="Class X - Mixed Question Paper",
            exam_title="Normal MCQs + MTF (Match the Following) MCQs",
            paper_format='A4',
            size_config='medium'
        )
        
        # Create generator with enhanced MTF support
        generator = EnhancedMCQPaperGenerator(
            config=config,
            show_answers=False,  # Set to True to see answer key
            question_count=sum(len(s.questions) for s in sections)
        )
        
        # Set the paper set name
        generator.set_set_name("A")
        
        # Add first page
        generator.add_page()
        
        # Generate paper from sections
        total_marks = generator.generate_from_sections(sections)
        
        # Save the paper
        output_file = "mixed_mcq_paper.pdf"
        generator.output(output_file)
        
        print(f"✅ Mixed MCQ Paper generated successfully!")
        print(f"📄 Output: {output_file}")
        print(f"📊 Total Questions: {generator.question_count}")
        print(f"   - Normal MCQs: {total_mcq}")
        print(f"   - MTF MCQs: {total_mtf}")
        print(f"🎯 Total Marks: {total_marks}")
        print(f"📋 Sections: {len(sections)}")
        
        # Generate answer key
        if input("Generate answer key? (y/n): ").lower() == 'y':
            answer_generator = EnhancedMCQPaperGenerator(
                config=config,
                show_answers=True,
                question_count=sum(len(s.questions) for s in sections)
            )
            answer_generator.set_set_name("A")
            answer_generator.add_page()
            answer_generator.generate_from_sections(sections)
            
            answer_file = "mixed_mcq_paper_answers.pdf"
            answer_generator.output(answer_file)
            print(f"✅ Answer key generated: {answer_file}")
            print(f"   Contains explanations for both Normal MCQs and MTF MCQs")
        
    except Exception as e:
        print(f"❌ Error generating paper: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()