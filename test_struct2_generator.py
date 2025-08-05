#!/usr/bin/env python3
"""
Test script for struct2.json with multiple MCQ question types
Note: Only 'mcq' and 'mtf-mcq' types are currently implemented in the enhanced generator.
Other types (s-mcq, ms-mcq, seq-mcq, p-mcq) will be treated as standard MCQ.
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
            q_type = question.get('question_type', 'mcq')
            type_counts[q_type] = type_counts.get(q_type, 0) + 1
            total_questions += 1
    
    return type_counts, total_questions

def main():
    """Generate test paper from struct2.json with multiple question types."""
    try:
        # Load questions from struct2.json
        struct_file = "questions_data/struct2.json"
        if not os.path.exists(struct_file):
            print(f"Error: {struct_file} not found!")
            return
        
        sections = load_questions_from_json(struct_file)
        
        # Analyze question types
        type_counts, total_questions = analyze_question_types(sections)
        
        # Display paper structure
        print("📋 Paper Structure from struct2.json:")
        print(f"   Total Sections: {len(sections)}")
        print(f"   Total Questions: {total_questions}")
        print("   Question Types Distribution:")
        for q_type, count in sorted(type_counts.items()):
            print(f"     - {q_type}: {count} questions")
        print()
        
        # Display implementation status
        print("⚠️  Implementation Status:")
        print("   ✅ Fully Supported: mcq, mtf-mcq")
        print("   ⚠️  Treated as standard MCQ: s-mcq, ms-mcq, seq-mcq, p-mcq")
        print("   Note: Unsupported types will render as standard MCQ questions")
        print()
        
        print(f"✅ Loaded {len(sections)} sections")
        
        # Analyze question types in each section
        for i, section in enumerate(sections):
            section_types = {}
            for q in section.questions:
                q_type = q.get('question_type', 'mcq')
                section_types[q_type] = section_types.get(q_type, 0) + 1
            
            type_summary = ", ".join([f"{count} {q_type}" for q_type, count in sorted(section_types.items())])
            print(f"   Section {i+1} ({section.name}): {type_summary}")
        print()
        
        # Create configuration
        config = MCQConfig(
            title="ABC International School",
            subtitle="Class X - Multi-Type MCQ Paper", 
            exam_title="6 Different MCQ Question Types",
            paper_format='A4',
            size_config='medium'
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
        output_file = "struct2_paper.pdf"
        generator.output(output_file)
        
        print(f"✅ Multi-Type MCQ Paper generated successfully!")
        print(f"📄 Output: {output_file}")
        print(f"📊 Total Questions: {generator.question_count}")
        
        # Display type breakdown
        supported_count = type_counts.get('mcq', 0) + type_counts.get('mtf-mcq', 0)
        unsupported_count = total_questions - supported_count
        print(f"   - Fully supported types: {supported_count}")
        print(f"   - Rendered as standard MCQ: {unsupported_count}")
        
        print(f"🎯 Total Marks: {total_marks}")
        print(f"📋 Sections: {len(sections)}")
        
        # Generate answer key
        if input("Generate answer key? (y/n): ").lower() == 'y':
            answer_generator = EnhancedMCQPaperGenerator(
                config=config,
                show_answers=True,
                question_count=total_questions
            )
            answer_generator.set_set_name("A")
            answer_generator.add_page()
            answer_generator.generate_from_sections(sections)
            
            answer_file = "struct2_paper_answers.pdf"
            answer_generator.output(answer_file)
            print(f"✅ Answer key generated: {answer_file}")
            print(f"   Contains explanations for all question types")
        
    except Exception as e:
        print(f"❌ Error generating paper: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()