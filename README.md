# PaperGen

A comprehensive Python-based tool for generating professional educational question papers in PDF format. Supports multiple question types including MCQ, Match the Following (MTF), Statements evaluation, and more with advanced formatting capabilities.

## Features

- **Enhanced MCQ Paper Generation**: Create sophisticated multiple choice question papers with various question types
- **Multiple Question Formats**: 
  - Basic Multiple Choice Questions
  - Match the Following (MTF) with optional headers
  - Statement evaluation (single and multiple statements)
  - List-based questions
  - Paragraph-based reading comprehension
  - Assertion and Reason questions
  - Sequencing questions
- **Professional PDF Output**: High-quality PDF generation with proper formatting and spacing
- **Flexible Font Sizing**: Four size configurations (x-small, small, medium, large) for different requirements
- **Multiple Paper Sets**: Generate multiple paper sets with shuffled questions
- **Answer Keys**: Automatic generation of answer keys with detailed explanations
- **Advanced Formatting**: Support for complex layouts, headers, and styling
- **Unicode Font Support**: Full Unicode support with Arial Unicode and Noto fonts

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Paper Generation

```bash
python enhanced_mcq_paper_builder.py --input-file questions_data/example.json
```

### Advanced Options

```bash
# Generate with custom settings
python enhanced_mcq_paper_builder.py --input-file questions_data/narayana2.json --size x-small --no-student-info --no-shuffle

# Generate with custom titles
python enhanced_mcq_paper_builder.py --input-file questions_data/example.json --title "Final Exam" --subtitle "Physics" --exam-title "Semester Test"
```

### Command Line Options

- `--input-file`: Path to questions JSON file (default: questions_data/mcq_questions.json)
- `--size`: Font and spacing size (x-small, small, medium, large) - default: medium
- `--title`: Paper title (max 60 characters)
- `--subtitle`: Paper subtitle (max 50 characters) 
- `--exam-title`: Exam title (max 50 characters)
- `--no-student-info`: Remove student information section from first page
- `--no-shuffle`: Disable question shuffling within sections
- `--layout`: Layout type (one-column, two-column) - default: two-column

## File Structure

- `enhanced_mcq_paper_builder.py`: Main enhanced script with full feature support
- `paper_generators/`: Core paper generation modules
  - `enhanced_mcq_generator.py`: Advanced MCQ generator with MTF and statement support
  - `mcq_generator.py`: Base MCQ generator class
  - `styles.py`: Font sizing and spacing configurations
- `questions_data/`: Question data files and documentation
  - `example.json`: Comprehensive example with all question types
  - `narayana2.json`: Sample question bank with 100 questions
  - `prompt.txt`: Documentation for AI-assisted question conversion
- `Generated_Papers/`: Output directory for generated PDFs (auto-created)

## Question Format

Questions are organized in sections within JSON files. The system supports multiple question types with flexible formatting.

### Basic Structure
```json
{
  "sections": [
    {
      "name": "Section Name",
      "description": "Section description or instructions",
      "questions": [...]
    }
  ]
}
```

### Basic MCQ Question
```json
{
  "question_text": ["What is the capital of France?"],
  "choices": ["London", "Berlin", "Paris", "Madrid"],
  "answer": "Paris",
  "reasoning": "Paris is the capital and largest city of France."
}
```

### Match the Following (MTF)
```json
{
  "question_text": ["Match the items:", "MTF_DATA"],
  "mtf_data": {
    "left_header": "Countries",
    "right_header": "Capitals",
    "left_column": ["A. France", "B. Germany", "C. Italy"],
    "right_column": ["Berlin", "Rome", "Paris"]
  },
  "choices": ["A-3, B-1, C-2", "A-1, B-2, C-3", "A-2, B-3, C-1", "A-3, B-2, C-1"],
  "answer": "A-3, B-1, C-2",
  "reasoning": "France-Paris, Germany-Berlin, Italy-Rome"
}
```

### Statement Evaluation
```json
{
  "question_text": ["STATEMENTS"],
  "statements": [
    {
      "label": "Statement-1",
      "text": "The Earth revolves around the Sun."
    },
    {
      "label": "Statement-2", 
      "text": "The Moon is a natural satellite of Earth."
    }
  ],
  "choices": ["1 only", "2 only", "Both 1 and 2", "Neither 1 nor 2"],
  "answer": "Both 1 and 2",
  "reasoning": "Both statements are scientifically accurate."
}
```

## Font Size Configurations

Choose from four predefined size configurations:

- **x-small**: Ultra-compact formatting for maximum content density
- **small**: Compact formatting for space efficiency  
- **medium**: Default balanced formatting
- **large**: Spacious formatting for better readability

Each configuration adjusts font sizes, spacing, and layout proportionally.

## Output

Generated papers are automatically saved with descriptive filenames:
- Papers include both question paper and answer key in single PDF
- Automatic page numbering and professional formatting
- Support for blank pages for rough work
- Generated in the current directory with timestamp-based naming

## Exam Duration

Default exam duration is set to **120 minutes** and appears in the paper header.

## Requirements

- Python 3.7+
- fpdf2 (for PDF generation)
- PyMuPDF (for PDF processing)
- Pillow (for image support)
- Other dependencies as listed in requirements.txt

## Contributing

See `questions_data/prompt.txt` for detailed documentation on question format specifications and guidelines for creating question banks.

## Examples

Check the `questions_data/` folder for:
- `example.json`: Demonstrates all supported question types
- `narayana2.json`: Real-world question bank with 100 diverse questions

Generate a sample paper:
```bash
python enhanced_mcq_paper_builder.py --input-file questions_data/example.json --size small
```